#!/usr/bin/env python3
"""Apply the minimal Atento provider-boundary patch to pinned PsyChat.

The patch is intentionally generated from exact pinned-source anchors so drift
fails closed. It modifies the donor working tree; Git remains the source of
truth for exact change-surface measurement.
"""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

PINNED_COMMIT = "5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4"


def git(root: Path, *args: str) -> str:
    p = subprocess.run(["git", "-C", str(root), *args], text=True, capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stderr.strip() or p.stdout.strip())
    return p.stdout.strip()


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"{path}: expected anchor once, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def apply(root: Path) -> None:
    if git(root, "rev-parse", "HEAD") != PINNED_COMMIT:
        raise AssertionError("donor is not at the pinned commit")
    if git(root, "status", "--porcelain"):
        raise AssertionError("donor working tree must be clean")

    gateway = root / "core" / "model_gateway.py"
    gateway.write_text(
        '''from __future__ import annotations

from typing import Any, Protocol

import requests


class ModelGateway(Protocol):
    def complete(
        self,
        messages: list[dict[str, str]],
        *,
        max_tokens: int,
        temperature: float,
        top_p: float,
    ) -> str:
        ...


class DeepSeekModelGateway:
    def __init__(self, *, api_key: str, base_url: str, model: str) -> None:
        self.api_key = api_key
        self.url = f"{base_url}/chat/completions"
        self.model = model

    def complete(
        self,
        messages: list[dict[str, str]],
        *,
        max_tokens: int,
        temperature: float,
        top_p: float,
    ) -> str:
        response = requests.post(
            self.url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
            },
        )
        response.raise_for_status()
        result: dict[str, Any] = response.json()
        choices = result.get("choices") or []
        if not choices:
            return ""
        return choices[0]["message"]["content"]
''',
        encoding="utf-8",
    )

    rag = root / "core" / "rag_system.py"
    replace_once(rag, "import requests\n", "")
    replace_once(
        rag,
        "from core.tts_service import TTSService\n",
        "from core.tts_service import TTSService\n"
        "from core.model_gateway import DeepSeekModelGateway, ModelGateway\n",
    )
    replace_once(
        rag,
        "class RAGSystem:\n    def __init__(self):\n",
        "class RAGSystem:\n"
        "    def __init__(self, model_gateway: ModelGateway | None = None):\n",
    )
    replace_once(
        rag,
        "        self.psychology_agent = PsychologyAgent()\n",
        "        self.model_gateway = model_gateway or DeepSeekModelGateway(\n"
        "            api_key=DEEPSEEK_API_KEY,\n"
        "            base_url=DEEPSEEK_BASE_URL,\n"
        "            model=DEEPSEEK_MODEL,\n"
        "        )\n"
        "        self.psychology_agent = PsychologyAgent(model_gateway=self.model_gateway)\n",
    )
    replace_once(
        rag,
        '''            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json"
            }
            
            # 构建消息列表，包含对话历史
''',
        '''            # 构建消息列表，包含对话历史
''',
    )
    replace_once(
        rag,
        '''            data = {
                "model": DEEPSEEK_MODEL,
                "messages": messages,
                "max_tokens": 1000,  # 减少token数，鼓励简短回答
                "temperature": 0.6,   # 降低随机性，更稳定
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
''',
        '''            answer = self.model_gateway.complete(
                messages,
                max_tokens=1000,
                temperature=0.6,
                top_p=0.9,
            )
            return answer or "抱歉，我无法生成有效的回答。"
''',
    )

    agent = root / "agent" / "psychology_agent.py"
    replace_once(agent, "import requests\n", "")
    replace_once(
        agent,
        "from config import *\n",
        "from config import *\n"
        "from core.model_gateway import DeepSeekModelGateway, ModelGateway\n",
    )
    replace_once(
        agent,
        "    def __init__(self):\n"
        "        self.api_key = DEEPSEEK_API_KEY\n"
        "        self.llm_url = f\"{DEEPSEEK_BASE_URL}/chat/completions\"\n",
        "    def __init__(self, model_gateway: ModelGateway | None = None):\n"
        "        self.model_gateway = model_gateway or DeepSeekModelGateway(\n"
        "            api_key=DEEPSEEK_API_KEY,\n"
        "            base_url=DEEPSEEK_BASE_URL,\n"
        "            model=DEEPSEEK_MODEL,\n"
        "        )\n",
    )
    replace_once(
        agent,
        '''            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": DEEPSEEK_MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": 0.3,
                "top_p": 0.8
            }

            response = requests.post(self.llm_url, headers=headers, json=data)
            response.raise_for_status()

            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            else:
                return ""
''',
        '''            return self.model_gateway.complete(
                [{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.3,
                top_p=0.8,
            )
''',
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--donor-root", type=Path, required=True)
    args = parser.parse_args()
    apply(args.donor_root)
    print(git(args.donor_root, "diff", "--stat"))
    print(git(args.donor_root, "status", "--short"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
