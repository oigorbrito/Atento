import tempfile
import unittest
from pathlib import Path

from evals.spikes.psychat.forkability_probe import probe


class PsyChatForkabilityProbeTest(unittest.TestCase):
    def test_injection_friendly_runtime_scores_high(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for d in ("agent", "core", "web"):
                (root / d).mkdir()
            (root / "agent/psychology_agent.py").write_text(
                "class PsychologyAgent:\n"
                "    def __init__(self, gateway): self.gateway=gateway\n"
                "    def parse(x): return {'need_rag': True}\n",
                encoding="utf-8",
            )
            (root / "core/vector_store.py").write_text(
                "class VectorStore:\n"
                "    def __init__(self, embedding_gateway): self.gateway=embedding_gateway\n",
                encoding="utf-8",
            )
            (root / "core/rag_system.py").write_text(
                "class RAGSystem:\n"
                "    def __init__(self, agent, vector_store):\n"
                "        self.agent=agent; self.vector_store=vector_store\n",
                encoding="utf-8",
            )
            (root / "web/interface.py").write_text(
                "def chat(session, runtime): return runtime\n", encoding="utf-8"
            )
            result = probe(root)
            self.assertEqual(result["thin_wrapper_feasibility"], "HIGH")

    def test_hardwired_runtime_scores_low(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for d in ("agent", "core", "web"):
                (root / d).mkdir()
            (root / "agent/psychology_agent.py").write_text(
                "import requests\n"
                "class PsychologyAgent:\n"
                "    def __init__(self): pass\n"
                "    def x(self):\n"
                "        y='YES,主题1,主题2'\n"
                "        z=y.split(',')\n"
                "        return requests.post('https://x')\n",
                encoding="utf-8",
            )
            (root / "core/vector_store.py").write_text(
                "import requests\n"
                "class VectorStore:\n"
                "    def __init__(self): pass\n"
                "    def x(self): return requests.post('https://x')\n",
                encoding="utf-8",
            )
            (root / "core/rag_system.py").write_text(
                "class RAGSystem:\n"
                "    def __init__(self):\n"
                "        self.vector_store=VectorStore(); self.agent=PsychologyAgent(); self.conversation_history=[]\n"
                "    def x(self):\n"
                "        a=MAX_NO_RAG_ROUNDS\n"
                "        return force_retrieval=True\n",
                encoding="utf-8",
            )
            (root / "web/interface.py").write_text(
                "rag_system = RAGSystem()\n", encoding="utf-8"
            )
            result = probe(root)
            self.assertEqual(result["thin_wrapper_feasibility"], "LOW")
            self.assertEqual(result["seams_passed"], 0)


if __name__ == "__main__":
    unittest.main()
