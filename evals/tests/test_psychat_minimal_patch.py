import tempfile
import unittest
from pathlib import Path

from evals.spikes.psychat.minimal_fork_patch import patch_data_processor, patch_rag_system, patch_vector_store


PROCESSOR_FIXTURE = '''from typing import List, Dict, Any

class DataProcessor:
    def split_psychology_qa_pairs(self, text: str, source: str) -> List[Dict[str, Any]]:
        chunks = []
        sections = text.split('##')
        for i, section in enumerate(sections):
            section = section.strip()
            if not section:
                continue
            if i == 0 and ('心理咨询对话' in section or '==' in section):
                continue
            lines = section.split('\\n')
            qa_id = None
            content_lines = []
            for line in lines:
                line = line.strip()
                if line.startswith('ID:'):
                    qa_id = line.replace('ID:', '').strip()
                elif line and not line.startswith('ID:'):
                    content_lines.append(line)
            if content_lines:
                chunks.extend(
                    self._split_dialogue_by_turns(
                        content_lines,
                        source,
                        qa_id,
                    )
                )
        return chunks

    def _split_dialogue_by_turns(self, content_lines, source, qa_id):
        return [{
            "content": "\\n".join(content_lines),
            "source": source,
            "qa_id": qa_id if qa_id is not None else "unknown",
        }]
'''


VECTOR_STORE_FIXTURE = '''import chromadb
from chromadb.config import Settings
import requests
from typing import List, Dict, Any
from config import *

class VectorStore:
    def __init__(self):
        # 初始化阿里云百炼Embedding API配置
        self.api_key = ALIBABA_API_KEY
        self.embedding_url = "https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings"
        
        # 初始化ChromaDB客户端
        self.client = chromadb.PersistentClient(
            path=CHROMA_DB_PATH,
            settings=Settings()
        )
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"description": "MCP知识库向量存储"}
        )

    def get_embedding(self, text: str) -> List[float]:
        response = requests.post(self.embedding_url, json={"input": text})
        result = response.json()
        return result["data"][0]["embedding"]

    def add_documents(self, documents: List[Dict[str, Any]]) -> bool:
        return True

    def get_collection_info(self) -> Dict[str, Any]:
        return {
            'name': COLLECTION_NAME,
            'document_count': self.collection.count(),
            'path': CHROMA_DB_PATH
        }

    def clear_collection(self) -> bool:
        try:
            self.client.delete_collection(COLLECTION_NAME)
            self.collection = self.client.create_collection(
                name=COLLECTION_NAME,
                metadata={"description": "MCP知识库向量存储"}
            )
            return True
        except Exception:
            return False
'''


RAG_SYSTEM_FIXTURE = '''import os
import requests
from typing import List, Dict, Any
from config import *

class RAGSystem:
    def __init__(self):
        self.data_processor = DataProcessor()
        self.vector_store = VectorStore()
        self.psychology_agent = PsychologyAgent()
        self.deepseek_api_key = DEEPSEEK_API_KEY
        self.llm_url = f"{DEEPSEEK_BASE_URL}/chat/completions"

        # 对话历史
        self.conversation_history = []

    def generate_response(self, query: str, max_tokens: int = 1000) -> Dict[str, Any]:
        analysis = self.psychology_agent.analyze_user_input(query, self.conversation_history, self.vector_store)
        return {"analysis": analysis}

    def _generate_response(self, system_prompt: str, user_query: str, include_history: bool = True) -> str:
        try:
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json"
            }

            messages = []
            messages.append({
                "role": "system",
                "content": system_prompt
            })
            if include_history and self.conversation_history:
                recent_history = self.conversation_history[-12:]
                messages.extend(recent_history)
            messages.append({
                "role": "user",
                "content": user_query
            })

            data = {
                "model": DEEPSEEK_MODEL,
                "messages": messages,
                "max_tokens": 1000,
                "temperature": 0.6,
                "top_p": 0.9
            }

            response = requests.post(self.llm_url, headers=headers, json=data)
            response.raise_for_status()

            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            else:
                print(f"LLM API响应格式错误: {result}")
                return "抱歉，我无法生成有效的回答。"

        except Exception as e:
            return f"处理查询时出错: {str(e)}"
'''


class PsyChatMinimalPatchGeneratorTest(unittest.TestCase):
    def test_data_processor_patch_preserves_ids_and_emits_valid_python(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "processor.py"
            path.write_text(PROCESSOR_FIXTURE, encoding="utf-8")

            patch_data_processor(path)
            patched = path.read_text(encoding="utf-8")

            compile(patched, str(path), "exec")
            namespace = {}
            exec(compile(patched, str(path), "exec"), namespace)
            processor = namespace["DataProcessor"]()

            corpus = (
                "心理咨询对话 - 测试\n"
                "==================\n"
                "ID: 1\n"
                "##\n"
                "用户: first\n"
                "助手: first reply\n"
                "##\n"
                "ID: 2\n"
                "##\n"
                "用户: second\n"
                "助手: second reply\n"
            )
            chunks = processor.split_psychology_qa_pairs(corpus, "测试.txt")

            self.assertEqual(
                [chunk["qa_id"] for chunk in chunks],
                ["1", "2"],
            )
            self.assertNotIn("unknown", [chunk["qa_id"] for chunk in chunks])
            self.assertIn("section.splitlines()", patched)



    def test_vector_patch_preserves_versioned_cosine_contract_on_clear(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "vector_store.py"
            path.write_text(VECTOR_STORE_FIXTURE, encoding="utf-8")

            patch_vector_store(path)
            patched = path.read_text(encoding="utf-8")

            compile(patched, str(path), "exec")
            self.assertIn("import hashlib", patched)
            self.assertIn("embedding_gateway.index_identity", patched)
            self.assertIn("identity_hash = hashlib.sha256(", patched)
            self.assertIn("name=self.collection_name", patched)
            self.assertIn("self.client.delete_collection(self.collection_name)", patched)
            self.assertIn('"hnsw:space": "cosine"', patched)
            self.assertIn(
                '"atento:index_schema": ATENTO_INDEX_SCHEMA_VERSION',
                patched,
            )
            self.assertIn(
                '"atento:embedding_identity": self.embedding_identity',
                patched,
            )
            self.assertNotIn("self.client.delete_collection(COLLECTION_NAME)", patched)


    def test_rag_system_patch_preserves_message_construction(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "rag_system.py"
            path.write_text(RAG_SYSTEM_FIXTURE, encoding="utf-8")

            patch_rag_system(path)
            patched = path.read_text(encoding="utf-8")

            compile(patched, str(path), "exec")
            self.assertIn("messages = []", patched)
            self.assertIn('"role": "system"', patched)
            self.assertIn("recent_history = self.conversation_history[-12:]", patched)
            self.assertIn('"role": "user"', patched)
            self.assertNotIn("requests.post(", patched)

            class Gateway:
                def __init__(self):
                    self.calls = []

                def complete(self, **kwargs):
                    self.calls.append(kwargs)
                    return "ok"

            config = type("Config", (), {
                "DEEPSEEK_API_KEY": "",
                "DEEPSEEK_BASE_URL": "",
                "DEEPSEEK_MODEL": "stub",
            })
            import sys
            import types

            config_mod = types.ModuleType("config")
            for name in ("DEEPSEEK_API_KEY", "DEEPSEEK_BASE_URL", "DEEPSEEK_MODEL"):
                setattr(config_mod, name, getattr(config, name))
            sys.modules["config"] = config_mod

            namespace = {}
            exec(compile(patched, str(path), "exec"), namespace)
            gateway = Gateway()
            rag = namespace["RAGSystem"](
                gateway,
                object(),
                data_processor=object(),
                vector_store=object(),
                psychology_agent=object(),
            )
            rag.conversation_history = [
                {"role": "user", "content": "old"},
                {"role": "assistant", "content": "reply"},
            ]

            result = rag._generate_response("system", "current")

            self.assertEqual(result, "ok")
            self.assertEqual(len(gateway.calls), 1)
            self.assertEqual(
                gateway.calls[0]["messages"],
                [
                    {"role": "system", "content": "system"},
                    {"role": "user", "content": "old"},
                    {"role": "assistant", "content": "reply"},
                    {"role": "user", "content": "current"},
                ],
            )


if __name__ == "__main__":
    unittest.main()
