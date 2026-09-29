#!/usr/bin/env python3
"""Apply the minimal PsyChat fork patch needed by BLOCO I — RAG.

The patch is intentionally narrow:
- agent/psychology_agent.py: inject the LLM gateway;
- core/vector_store.py: inject the embedding gateway;
- core/rag_system.py: inject long-lived dependencies and remove its direct LLM call.

It does not patch the donor web/TTS chassis. Those are outside the RAG donor
surface being evaluated.

The script is pinned-source aware and fails if the expected source shape has
drifted. After applying, it records the exact changed-file set from Git.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


PINNED_COMMIT = "5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4"
PATCHED_FILES = (
    "agent/psychology_agent.py",
    "core/vector_store.py",
    "core/rag_system.py",
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
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.DOTALL)
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
        "from typing import List, Dict, Any\n",
        label="vector requests import",
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
    def __init__(self, embedding_gateway):
        self.embedding_gateway = embedding_gateway

        # 初始化ChromaDB客户端
""",
        label="VectorStore constructor",
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
    text = replace_regex_once(
        text,
        r"""            headers = \{.*?            result = response\.json\(\)\n            if 'choices' in result and len\(result\['choices'\]\) > 0:\n                return result\['choices'\]\[0\]\['message'\]\['content'\]\n            else:\n                print\(f"LLM API响应格式错误: \{result\}"\)\n                return "抱歉，我无法生成有效的回答。"\n""",
        """            return self.model_gateway.complete(
                purpose="psychat.rag.response",
                messages=messages,
                timeout_s=30.0,
            )
""",
        label="RAGSystem direct LLM call",
    )
    path.write_text(text, encoding="utf-8")


def direct_provider_bypasses(root: Path) -> dict[str, list[str]]:
    patterns = {
        "requests.post": re.compile(r"requests\.post\("),
        "requests.get": re.compile(r"requests\.get\("),
        "requests.request": re.compile(r"requests\.request\("),
    }
    result: dict[str, list[str]] = {key: [] for key in patterns}
    for relative in PATCHED_FILES:
        text = (root / relative).read_text(encoding="utf-8")
        for name, pattern in patterns.items():
            if pattern.search(text):
                result[name].append(relative)
    return result


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

    return {
        "metric_version": "psychat-minimal-fork-patch-v0.1",
        "pinned_commit": head_before,
        "changed_files": changed,
        "files_touched_exact": len(changed),
        "direct_provider_bypass_count_in_patched_rag_surface": remaining,
        "direct_provider_bypass_evidence": bypasses,
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
