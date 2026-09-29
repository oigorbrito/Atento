# -*- coding: utf-8 -*-
"""
向量存储模块
基于ChromaDB实现向量存储和检索功能
"""

import chromadb
from chromadb.config import Settings
import hashlib
import json
import os
import uuid
from pathlib import Path
from typing import List, Dict, Any
from config import *

ATENTO_INDEX_SCHEMA_VERSION = "rag-cosine-v1"
ATENTO_DEFAULT_CORPUS_IDENTITY = "psychat@5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4"

class VectorStore:
    def __init__(
        self,
        embedding_gateway,
        corpus_identity=ATENTO_DEFAULT_CORPUS_IDENTITY,
    ):
        self.embedding_gateway = embedding_gateway
        embedding_identity = str(embedding_gateway.index_identity).strip()
        corpus_identity = str(corpus_identity).strip()
        if not embedding_identity:
            raise ValueError("embedding_gateway.index_identity must be non-empty")
        if not corpus_identity:
            raise ValueError("corpus_identity must be non-empty")
        index_identity = f"{embedding_identity}|{corpus_identity}"
        identity_hash = hashlib.sha256(
            index_identity.encode("utf-8")
        ).hexdigest()[:12]
        self.embedding_identity = embedding_identity
        self.corpus_identity = corpus_identity
        self.logical_collection_name = (
            f"{COLLECTION_NAME}__{ATENTO_INDEX_SCHEMA_VERSION}__{identity_hash}"
        )
        self.pointer_path = (
            Path(CHROMA_DB_PATH)
            / f".atento-active-{identity_hash}.json"
        )
        self.collection_name = self._read_active_collection_name()
        self.expected_collection_metadata = {
            "description": "MCP知识库向量存储",
            "hnsw:space": "cosine",
            "atento:index_schema": ATENTO_INDEX_SCHEMA_VERSION,
            "atento:embedding_identity": self.embedding_identity,
            "atento:corpus_identity": self.corpus_identity,
        }

        # 初始化ChromaDB客户端
        self.client = chromadb.PersistentClient(
            path=CHROMA_DB_PATH,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # 获取或创建集合
        if self.pointer_path.exists():
            self.collection = self.client.get_collection(
                name=self.collection_name,
            )
        else:
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata=self.expected_collection_metadata,
            )
        self._validate_collection_contract()
        
        print(f"向量存储初始化完成: {CHROMA_DB_PATH}")
    
    def _read_active_collection_name(self) -> str:
        if not self.pointer_path.exists():
            return self.logical_collection_name
        try:
            payload = json.loads(self.pointer_path.read_text(encoding="utf-8"))
        except Exception as exc:
            raise RuntimeError(f"invalid vector index pointer: {exc}") from exc
        active = str(payload.get("active_collection", "")).strip()
        if not active.startswith(self.logical_collection_name + "__gen-"):
            raise RuntimeError(f"invalid active vector collection: {active!r}")
        return active

    def _write_active_collection_name(self, name: str) -> None:
        self.pointer_path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.pointer_path.with_suffix(
            self.pointer_path.suffix + f".{uuid.uuid4().hex}.tmp"
        )
        payload = {
            "logical_collection": self.logical_collection_name,
            "active_collection": name,
        }
        temp.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
        os.replace(temp, self.pointer_path)

    def _refresh_active_collection(self) -> None:
        active_name = self._read_active_collection_name()
        if active_name == self.collection_name:
            return
        collection = self.client.get_collection(name=active_name)
        previous_collection = self.collection
        previous_name = self.collection_name
        self.collection = collection
        self.collection_name = active_name
        try:
            self._validate_collection_contract()
        except Exception:
            self.collection = previous_collection
            self.collection_name = previous_name
            raise

    def rebuild_documents(self, documents: List[Dict[str, Any]]) -> bool:
        generation = uuid.uuid4().hex[:12]
        staging_name = f"{self.logical_collection_name}__gen-{generation}"
        staging_metadata = dict(self.expected_collection_metadata)
        staging_metadata["atento:generation"] = generation
        previous_collection = self.collection
        previous_name = self.collection_name
        staging = None
        try:
            staging = self.client.create_collection(
                name=staging_name,
                metadata=staging_metadata,
            )
            self.collection = staging
            self.collection_name = staging_name
            success = self.add_documents(documents)
            complete = success and staging.count() == len(documents)
            if not complete:
                self.collection = previous_collection
                self.collection_name = previous_name
                self.client.delete_collection(staging_name)
                return False
            self._validate_collection_contract()
            self.collection = previous_collection
            self.collection_name = previous_name
            self._write_active_collection_name(staging_name)
            self.collection = staging
            self.collection_name = staging_name
            return True
        except Exception as exc:
            self.collection = previous_collection
            self.collection_name = previous_name
            if staging is not None:
                try:
                    self.client.delete_collection(staging_name)
                except Exception:
                    pass
            print(f"原子重建向量索引失败: {exc}")
            return False

    def _validate_collection_contract(self) -> Dict[str, Any]:
        metadata = dict(getattr(self.collection, 'metadata', {}) or {})
        mismatches = {
            key: {'expected': expected, 'actual': metadata.get(key)}
            for key, expected in self.expected_collection_metadata.items()
            if metadata.get(key) != expected
        }
        if mismatches:
            raise RuntimeError(
                f"vector collection metadata mismatch: {mismatches}"
            )
        return metadata

    def get_embedding(self, text: str) -> List[float]:
        """Generate embeddings through the injected gateway."""
        try:
            return list(self.embedding_gateway.embed(text=text))
        except Exception as e:
            print(f"生成嵌入向量时出错: {e}")
            return []

    def add_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """将文档添加到向量存储"""
        try:
            print(f"开始添加 {len(documents)} 个文档到向量存储...")
            
            # 准备数据
            ids = []
            texts = []
            embeddings = []
            metadatas = []
            
            for i, doc in enumerate(documents):
                # 生成唯一ID
                doc_id = f"doc_{i}_{doc['source']}"
                
                # 生成嵌入向量
                embedding = self.get_embedding(doc['content'])
                if not embedding:
                    print(f"跳过文档 {doc_id}，无法生成嵌入向量")
                    continue
                
                # 准备元数据 - 确保所有值都不为None
                metadata = {
                    'source': str(doc['source']),
                    'size': int(doc['size']),
                    'type': str(doc.get('type', 'unknown'))
                }
                
                # 添加心理学相关元数据，确保不为None
                if 'topic' in doc and doc['topic'] is not None:
                    metadata['topic'] = str(doc['topic'])
                else:
                    metadata['topic'] = 'unknown'
                    
                if 'qa_id' in doc and doc['qa_id'] is not None:
                    metadata['qa_id'] = str(doc['qa_id'])
                else:
                    metadata['qa_id'] = 'unknown'
                    
                if 'header' in doc and doc['header'] is not None:
                    metadata['header'] = str(doc['header'])
                else:
                    metadata['header'] = 'none'
                
                ids.append(doc_id)
                texts.append(doc['content'])
                embeddings.append(embedding)
                metadatas.append(metadata)
                
                if (i + 1) % 10 == 0:
                    print(f"已处理 {i + 1}/{len(documents)} 个文档")
            
            # 分批添加到ChromaDB（避免批量大小限制）
            if ids:
                batch_size = 1000  # ChromaDB建议的批量大小
                total_batches = (len(ids) + batch_size - 1) // batch_size
                
                for i in range(0, len(ids), batch_size):
                    end_idx = min(i + batch_size, len(ids))
                    batch_ids = ids[i:end_idx]
                    batch_texts = texts[i:end_idx]
                    batch_embeddings = embeddings[i:end_idx]
                    batch_metadatas = metadatas[i:end_idx]
                    
                    self.collection.upsert(
                        ids=batch_ids,
                        documents=batch_texts,
                        embeddings=batch_embeddings,
                        metadatas=batch_metadatas
                    )
                    
                    current_batch = (i // batch_size) + 1
                    print(f"已添加批次 {current_batch}/{total_batches} ({len(batch_ids)} 个文档)")
                
                print(f"✅ 成功添加 {len(ids)} 个文档到向量存储")
                return True
            else:
                print("没有有效的文档可以添加")
                return False
                
        except Exception as e:
            print(f"添加文档到向量存储时出错: {e}")
            return False
    
    def search(self, query: str, top_k: int = TOP_K_RESULTS, threshold: float = SIMILARITY_THRESHOLD, topics: List[str] = None) -> List[Dict[str, Any]]:
        """搜索相关文档"""
        try:
            self._refresh_active_collection()
            # 生成查询的嵌入向量
            query_embedding = self.get_embedding(query)
            if not query_embedding:
                print("无法生成查询的嵌入向量")
                return []
            
            # 构建过滤条件（支持多主题）
            where_filter = None
            if topics and len(topics) > 0:
                if len(topics) == 1:
                    where_filter = {"topic": topics[0]}
                    print(f"按主题过滤: {topics[0]}")
                else:
                    # 多主题检索：分别检索每个主题，然后合并结果
                    print(f"将分别检索多个主题: {', '.join(topics)}")
                    all_docs = []
                    
                    for topic in topics:
                        topic_filter = {"topic": topic}
                        topic_search_params = {
                            "query_embeddings": [query_embedding],
                            "n_results": top_k // len(topics) + 2,  # 每个主题分配部分结果
                            "include": ['documents', 'metadatas', 'distances'],
                            "where": topic_filter
                        }
                        
                        topic_results = self.collection.query(**topic_search_params)
                        
                        if topic_results['documents'] and topic_results['documents'][0]:
                            print(f"主题 '{topic}' 找到 {len(topic_results['documents'][0])} 个文档")
                            for i, (doc, metadata, distance) in enumerate(zip(
                                topic_results['documents'][0],
                                topic_results['metadatas'][0], 
                                topic_results['distances'][0]
                            )):
                                similarity = 1 - distance
                                if similarity >= threshold:
                                    all_docs.append({
                                        'content': doc,
                                        'metadata': metadata,
                                        'similarity': similarity,
                                        'distance': distance
                                    })
                        else:
                            print(f"主题 '{topic}' 未找到文档")
                    
                    # 按相似度排序并返回top_k个结果
                    all_docs.sort(key=lambda x: x['similarity'], reverse=True)
                    final_docs = all_docs[:top_k]
                    print(f"多主题检索合并后共找到 {len(final_docs)} 个相关文档")
                    return final_docs
            
            # 在ChromaDB中搜索
            search_params = {
                "query_embeddings": [query_embedding],
                "n_results": top_k,
                "include": ['documents', 'metadatas', 'distances']
            }
            
            if where_filter:
                search_params["where"] = where_filter
            
            results = self.collection.query(**search_params)
            
            # 处理结果
            documents = []
            if results['documents'] and results['documents'][0]:
                print(f"原始搜索结果数量: {len(results['documents'][0])}")
                for i, (doc, metadata, distance) in enumerate(zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                )):
                    # 计算相似度分数（距离越小，相似度越高）
                    similarity = 1 - distance
                    
                    print(f"文档 {i+1}: 相似度={similarity:.3f}, 阈值={threshold:.3f}, 距离={distance:.3f}")
                    
                    if similarity >= threshold:
                        documents.append({
                            'content': doc,
                            'metadata': metadata,
                            'similarity': similarity,
                            'distance': distance
                        })
                    else:
                        print(f"  文档 {i+1} 相似度低于阈值，已过滤")
            else:
                print("ChromaDB返回空结果")
            
            print(f"找到 {len(documents)} 个相关文档")
            return documents
            
        except Exception as e:
            print(f"搜索文档时出错: {e}")
            return []
    
    def get_collection_info(self) -> Dict[str, Any]:
        """获取集合信息"""
        try:
            self._refresh_active_collection()
            metadata = self._validate_collection_contract()
            count = self.collection.count()
            return {
                'name': self.collection_name,
                'document_count': count,
                'path': CHROMA_DB_PATH,
                'index_schema': metadata['atento:index_schema'],
                'embedding_identity': metadata['atento:embedding_identity'],
                'corpus_identity': metadata['atento:corpus_identity'],
            }
        except RuntimeError:
            raise
        except Exception as e:
            print(f"获取集合信息时出错: {e}")
            return {}
    
    def clear_collection(self) -> bool:
        """清空集合"""
        try:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata=self.expected_collection_metadata,
            )
            self._validate_collection_contract()
            print("集合已清空")
            return True
        except Exception as e:
            print(f"清空集合时出错: {e}")
            return False


if __name__ == "__main__":
    # 测试向量存储
    vector_store = VectorStore()
    
    # 显示集合信息
    info = vector_store.get_collection_info()
    print(f"集合信息: {info}")
    
    # 测试搜索
    test_query = "什么是MCP？"
    results = vector_store.search(test_query)
    
    for i, result in enumerate(results):
        print(f"\n=== 结果 {i+1} ===")
        print(f"相似度: {result['similarity']:.3f}")
        print(f"来源: {result['metadata']['source']}")
        print(f"内容预览: {result['content'][:200]}...")

