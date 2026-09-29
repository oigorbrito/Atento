#!/usr/bin/env python3
"""Apply the minimal PsyChat fork patch needed by BLOCO I — RAG.

The patch is intentionally narrow:
- agent/psychology_agent.py: inject the LLM gateway;
- core/vector_store.py: inject the embedding gateway;
- core/rag_system.py: inject long-lived dependencies and remove its direct LLM call;
- data/processor.py: preserve corpus QA IDs across the donor's ## record delimiter.

It does not patch the donor web/TTS chassis. Those are outside the RAG donor
surface being evaluated.

The script is pinned-source aware and fails if the expected source shape has
drifted. After applying, it records the exact changed-file set from Git.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path


PINNED_COMMIT = "5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4"
PROVIDER_BOUNDARY_FILES = (
    "agent/psychology_agent.py",
    "core/vector_store.py",
    "core/rag_system.py",
)
PATCHED_FILES = PROVIDER_BOUNDARY_FILES + (
    "data/processor.py",
)


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed: {result.stderr.strip()}"
        )
    return result.stdout.strip()


def replace_once(text: str, old: str, new: str, *, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one source match, found {count}")
    return text.replace(old, new, 1)


def replace_regex_once(text: str, pattern: str, replacement: str, *, label: str) -> str:
    # Use a callable replacement so backslashes in generated Python source
    # (for example '\\n') are not re-interpreted by re.sub's template parser.
    updated, count = re.subn(
        pattern,
        lambda _match: replacement,
        text,
        count=1,
        flags=re.DOTALL,
    )
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one regex match, found {count}")
    return updated


def patch_psychology_agent(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "import requests\nfrom typing import List, Dict, Any, Optional, Tuple\n",
        "from typing import List, Dict, Any, Optional, Tuple\n",
        label="psychology requests import",
    )
    text = replace_once(
        text,
        """    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY
        self.llm_url = f"{DEEPSEEK_BASE_URL}/chat/completions"
        print("心理咨询AGENT初始化完成")
""",
        """    def __init__(self, model_gateway):
        self.model_gateway = model_gateway
        print("心理咨询AGENT初始化完成")
""",
        label="PsychologyAgent constructor",
    )
    text = replace_regex_once(
        text,
        r"""    def _call_llm\(self, prompt: str, max_tokens: int = 1000\) -> str:\n.*?\n    # ==================== 入口方法 ====================""",
        """    def _call_llm(self, prompt: str, max_tokens: int = 1000) -> str:
        \"\"\"Call the injected Atento-compatible model gateway.\"\"\"
        try:
            return self.model_gateway.complete(
                purpose="psychat.rag.agent",
                messages=[{"role": "user", "content": prompt}],
                timeout_s=30.0,
            )
        except Exception as e:
            print(f"调用LLM时出错: {e}")
            return ""

    # ==================== 入口方法 ====================""",
        label="PsychologyAgent _call_llm",
    )
    path.write_text(text, encoding="utf-8")


def patch_vector_store(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "import requests\nfrom typing import List, Dict, Any\n",
        "import hashlib\nfrom typing import List, Dict, Any\n",
        label="vector requests import",
    )
    text = replace_once(
        text,
        "from config import *\n\nclass VectorStore:",
        "from config import *\n\n"
        "ATENTO_INDEX_SCHEMA_VERSION = \"rag-cosine-v1\"\n"
        "ATENTO_DEFAULT_CORPUS_IDENTITY = \"psychat@5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4\"\n\n"
        "class VectorStore:",
        label="VectorStore index schema version",
    )
    text = replace_once(
        text,
        """class VectorStore:
    def __init__(self):
        # 初始化阿里云百炼Embedding API配置
        self.api_key = ALIBABA_API_KEY
        self.embedding_url = "https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings"
        
        # 初始化ChromaDB客户端
""",
        """class VectorStore:
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
        self.collection_name = (
            f"{COLLECTION_NAME}__{ATENTO_INDEX_SCHEMA_VERSION}__{identity_hash}"
        )

        # 初始化ChromaDB客户端
""",
        label="VectorStore constructor",
    )
    text = replace_once(
        text,
        "name=COLLECTION_NAME,",
        "name=self.collection_name,",
        label="VectorStore versioned collection name",
    )
    text = replace_once(
        text,
        'metadata={"description": "MCP知识库向量存储"}',
        'metadata={'
        '"description": "MCP知识库向量存储", '
        '"hnsw:space": "cosine", '
        '"atento:index_schema": ATENTO_INDEX_SCHEMA_VERSION, '
        '"atento:embedding_identity": self.embedding_identity, '
        '"atento:corpus_identity": self.corpus_identity'
        '}',
        label="VectorStore cosine distance metric",
    )
    text = replace_once(
        text,
        "                'name': COLLECTION_NAME,",
        "                'name': self.collection_name,",
        label="VectorStore collection info name",
    )
    text = replace_once(
        text,
        "            self.client.delete_collection(COLLECTION_NAME)\n"
        "            self.collection = self.client.create_collection(\n"
        "                name=COLLECTION_NAME,\n"
        "                metadata={\"description\": \"MCP知识库向量存储\"}\n"
        "            )",
        "            self.client.delete_collection(self.collection_name)\n"
        "            self.collection = self.client.create_collection(\n"
        "                name=self.collection_name,\n"
        "                metadata={\n"
        "                    \"description\": \"MCP知识库向量存储\",\n"
        "                    \"hnsw:space\": \"cosine\",\n"
        "                    \"atento:index_schema\": ATENTO_INDEX_SCHEMA_VERSION,\n"
        "                    \"atento:embedding_identity\": self.embedding_identity,\n"
        "                    \"atento:corpus_identity\": self.corpus_identity,\n"
        "                }\n"
        "            )",
        label="VectorStore clear collection contract",
    )
    text = replace_once(
        text,
        """                    self.collection.add(
                        ids=batch_ids,
                        documents=batch_texts,
                        embeddings=batch_embeddings,
                        metadatas=batch_metadatas
                    )""",
        """                    self.collection.upsert(
                        ids=batch_ids,
                        documents=batch_texts,
                        embeddings=batch_embeddings,
                        metadatas=batch_metadatas
                    )""",
        label="VectorStore idempotent document upsert",
    )
    text = replace_regex_once(
        text,
        r"""    def get_embedding\(self, text: str\) -> List\[float\]:\n.*?\n    def add_documents""",
        """    def get_embedding(self, text: str) -> List[float]:
        \"\"\"Generate embeddings through the injected gateway.\"\"\"
        try:
            return list(self.embedding_gateway.embed(text=text))
        except Exception as e:
            print(f"生成嵌入向量时出错: {e}")
            return []

    def add_documents""",
        label="VectorStore get_embedding",
    )
    path.write_text(text, encoding="utf-8")


def patch_rag_system(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "import os\nimport requests\nfrom typing import List, Dict, Any\n",
        "import os\nfrom typing import List, Dict, Any\n",
        label="RAG requests import",
    )
    text = replace_regex_once(
        text,
        r"""class RAGSystem:\n    def __init__\(self\):\n.*?        # 对话历史\n""",
        """class RAGSystem:
    def __init__(
        self,
        model_gateway,
        embedding_gateway,
        *,
        data_processor=None,
        vector_store=None,
        psychology_agent=None,
        tts_service=None,
    ):
        # Long-lived/stateless resources can be injected and reused by the
        # composition root; mutable conversation state remains per runtime.
        self.model_gateway = model_gateway
        self.data_processor = data_processor or DataProcessor()
        self.vector_store = vector_store or VectorStore(
            embedding_gateway=embedding_gateway
        )
        self.psychology_agent = psychology_agent or PsychologyAgent(
            model_gateway=model_gateway
        )
        self.tts_service = tts_service

        # 对话历史
""",
        label="RAGSystem constructor",
    )
    text = replace_once(
        text,
        "    def generate_response(self, query: str, max_tokens: int = 1000) -> Dict[str, Any]:\n",
        "    def generate_response(\n"
        "        self,\n"
        "        query: str,\n"
        "        max_tokens: int = 1000,\n"
        "        force_retrieval: bool = False,\n"
        "    ) -> Dict[str, Any]:\n",
        label="RAGSystem generate_response route seam",
    )
    text = replace_once(
        text,
        "            analysis = self.psychology_agent.analyze_user_input(query, self.conversation_history, self.vector_store)\n",
        "            analysis = self.psychology_agent.analyze_user_input(\n"
        "                query,\n"
        "                self.conversation_history,\n"
        "                self.vector_store,\n"
        "                force_retrieval=force_retrieval,\n"
        "            )\n",
        label="RAGSystem external force_retrieval authority",
    )
    text = replace_regex_once(
        text,
        r"""            headers = \{.*?            \}\n            \n""",
        "",
        label="RAGSystem direct LLM headers",
    )
    text = replace_regex_once(
        text,
        r"""            data = \{.*?            result = response\.json\(\)\n            if 'choices' in result and len\(result\['choices'\]\) > 0:\n                return result\['choices'\]\[0\]\['message'\]\['content'\]\n            else:\n                print\(f"LLM API响应格式错误: \{result\}"\)\n                return "抱歉，我无法生成有效的回答。"\n""",
        """            return self.model_gateway.complete(
                purpose="psychat.rag.response",
                messages=messages,
                timeout_s=30.0,
            )
""",
        label="RAGSystem direct LLM call",
    )
    path.write_text(text, encoding="utf-8")


def patch_data_processor(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = replace_regex_once(
        text,
        r"""    def split_psychology_qa_pairs\(self, text: str, source: str\) -> List\[Dict\[str, Any\]\]:\n.*?\n    def _split_dialogue_by_turns""",
        """    def split_psychology_qa_pairs(self, text: str, source: str) -> List[Dict[str, Any]]:
        \"\"\"Split QA records while preserving the ID that precedes each ## dialogue block.\"\"\"
        chunks = []
        sections = text.split('##')
        pending_qa_id = None

        for i, section in enumerate(sections):
            section = section.strip()
            if not section:
                continue

            lines = section.splitlines()
            section_qa_id = None
            content_lines = []

            for line in lines:
                line = line.strip()
                if line.startswith('ID:'):
                    section_qa_id = line.replace('ID:', '').strip()
                elif not line:
                    continue
                elif i == 0 and (
                    '心理咨询对话' in line
                    or set(line) == {'='}
                ):
                    # The first record ID shares section 0 with the file header.
                    # Ignore only header lines; never discard the whole section.
                    continue
                else:
                    content_lines.append(line)

            if section_qa_id is not None:
                pending_qa_id = section_qa_id

            if content_lines:
                dialogue_chunks = self._split_dialogue_by_turns(
                    content_lines,
                    source,
                    pending_qa_id,
                )
                chunks.extend(dialogue_chunks)

        return chunks

    def _split_dialogue_by_turns""",
        label="DataProcessor QA ID preservation",
    )
    path.write_text(text, encoding="utf-8")


def constructor_parameters(path: Path, class_name: str) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                    return {arg.arg for arg in item.args.args}
    return set()


def method_parameters(path: Path, class_name: str, method_name: str) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == method_name:
                    return {arg.arg for arg in item.args.args}
    return set()


def method_assigned_names(path: Path, class_name: str, method_name: str) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == method_name:
                    return {
                        target.id
                        for child in ast.walk(item)
                        if isinstance(child, ast.Assign)
                        for target in child.targets
                        if isinstance(target, ast.Name)
                    }
    return set()


def direct_provider_bypasses(root: Path) -> dict[str, list[str]]:
    patterns = {
        "requests.post": re.compile(r"requests\.post\("),
        "requests.get": re.compile(r"requests\.get\("),
        "requests.request": re.compile(r"requests\.request\("),
    }
    result: dict[str, list[str]] = {key: [] for key in patterns}
    for relative in PROVIDER_BOUNDARY_FILES:
        text = (root / relative).read_text(encoding="utf-8")
        for name, pattern in patterns.items():
            if pattern.search(text):
                result[name].append(relative)
    return result


def retention_metrics(root: Path) -> dict:
    rows = []
    total_original = 0
    total_deleted = 0

    for line in git(root, "diff", "--numstat").splitlines():
        if not line.strip():
            continue
        added_raw, deleted_raw, path = line.split("\t", 2)
        if path not in PATCHED_FILES:
            continue
        added = int(added_raw)
        deleted = int(deleted_raw)
        original = len(git(root, "show", f"HEAD:{path}").splitlines())
        retained = max(original - deleted, 0)
        rows.append(
            {
                "path": path,
                "original_lines": original,
                "added_lines": added,
                "deleted_or_replaced_original_lines": deleted,
                "retained_original_lines": retained,
                "retained_original_line_ratio": (
                    retained / original if original else 1.0
                ),
            }
        )
        total_original += original
        total_deleted += deleted

    total_retained = max(total_original - total_deleted, 0)
    return {
        "files": sorted(rows, key=lambda item: item["path"]),
        "original_lines": total_original,
        "deleted_or_replaced_original_lines": total_deleted,
        "retained_original_lines": total_retained,
        "retained_original_line_ratio": (
            total_retained / total_original if total_original else 1.0
        ),
        "interpretation": (
            "Approximation from git diff --numstat: original lines not deleted "
            "or replaced in the BLOCO I RAG correctness patch surface."
        ),
    }


def apply_patch(donor_root: Path) -> dict:
    head_before = git(donor_root, "rev-parse", "HEAD")
    if head_before != PINNED_COMMIT:
        raise AssertionError(
            f"expected donor HEAD {PINNED_COMMIT}, got {head_before}"
        )
    if git(donor_root, "status", "--porcelain"):
        raise AssertionError("donor worktree must be clean before patch")

    patch_psychology_agent(donor_root / "agent/psychology_agent.py")
    patch_vector_store(donor_root / "core/vector_store.py")
    patch_rag_system(donor_root / "core/rag_system.py")
    patch_data_processor(donor_root / "data/processor.py")

    changed = [
        line for line in git(donor_root, "diff", "--name-only").splitlines() if line
    ]
    expected = list(PATCHED_FILES)
    if sorted(changed) != sorted(expected):
        raise AssertionError(
            f"unexpected changed-file set: expected {expected}, got {changed}"
        )

    bypasses = direct_provider_bypasses(donor_root)
    remaining = sum(len(paths) for paths in bypasses.values())
    if remaining:
        raise AssertionError(f"direct provider bypasses remain in patched RAG files: {bypasses}")

    rag_params = constructor_parameters(donor_root / "core/rag_system.py", "RAGSystem")
    agent_params = constructor_parameters(
        donor_root / "agent/psychology_agent.py", "PsychologyAgent"
    )
    vector_params = constructor_parameters(
        donor_root / "core/vector_store.py", "VectorStore"
    )
    if not {"model_gateway", "embedding_gateway"}.issubset(rag_params):
        raise AssertionError("RAGSystem provider gateways are not injectable")
    if "model_gateway" not in agent_params:
        raise AssertionError("PsychologyAgent model gateway is not injectable")
    if "embedding_gateway" not in vector_params:
        raise AssertionError("VectorStore embedding gateway is not injectable")

    generate_params = method_parameters(
        donor_root / "core/rag_system.py",
        "RAGSystem",
        "generate_response",
    )
    if "force_retrieval" not in generate_params:
        raise AssertionError(
            "RAGSystem does not expose external force_retrieval routing authority"
        )

    response_locals = method_assigned_names(
        donor_root / "core/rag_system.py",
        "RAGSystem",
        "_generate_response",
    )
    if "messages" not in response_locals:
        raise AssertionError(
            "RAGSystem _generate_response lost local messages construction"
        )

    retention = retention_metrics(donor_root)

    return {
        "metric_version": "psychat-minimal-fork-patch-v0.9",
        "pinned_commit": head_before,
        "changed_files": changed,
        "donor_files_touched_to_introduce_provider_boundary": len(PROVIDER_BOUNDARY_FILES),
        "donor_files_touched_for_bloco_i_rag_correctness": len(changed),
        "qa_id_provenance_patch_required": True,
        "vector_distance_metric": "cosine",
        "vector_index_schema_version": "rag-cosine-v1",
        "vector_collection_versioned": True,
        "vector_clear_preserves_index_contract": True,
        "embedding_identity_required_by_vector_store": True,
        "vector_collection_namespaced_by_embedding_identity": True,
        "vector_collection_namespaced_by_corpus_identity": True,
        "same_identity_rebuild_uses_upsert": True,
        "similarity_transform": "1 - cosine_distance",
        "files_touched_to_swap_model_provider_after_boundary": 0,
        "files_touched_to_swap_embedding_provider_after_boundary": 0,
        "provider_swap_mechanism": "constructor injection",
        "model_gateway_injectable": True,
        "embedding_gateway_injectable": True,
        "external_rag_route_enforceable": True,
        "rag_route_enforcement_parameter": "force_retrieval",
        "direct_provider_bypass_count_in_patched_rag_surface": remaining,
        "direct_provider_bypass_evidence": bypasses,
        "upstream_code_retention": retention,
        "scope": "BLOCO I RAG core only; donor web/TTS chassis intentionally excluded",
        "git_diff_stat": git(donor_root, "diff", "--stat"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--donor-root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = apply_patch(args.donor_root)
    encoded = json.dumps(result, ensure_ascii=False, indent=2)
    print(encoded)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
