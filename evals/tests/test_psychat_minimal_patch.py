import tempfile
import unittest
from pathlib import Path

from evals.spikes.psychat.minimal_fork_patch import patch_data_processor


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
            self.assertIn("section.split('\\n')", patched)


if __name__ == "__main__":
    unittest.main()
