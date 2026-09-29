import unittest
from pathlib import Path

from evals.atentoeval.runner import load_cases


RAG_CASES = Path("evals/cases/rag_v0.jsonl")


class RagCaseSetTest(unittest.TestCase):
    def test_rag_v0_has_expected_size_and_balance(self):
        cases = load_cases(RAG_CASES)
        self.assertEqual(len(cases), 20)

        expected = [case.steps[0].expected for case in cases.values()]
        positives = [item for item in expected if item.rag_required is True]
        negatives = [item for item in expected if item.rag_required is False]

        self.assertGreaterEqual(len(positives), 10)
        self.assertGreaterEqual(len(negatives), 5)

    def test_rag_fixture_ids_match_expected_retrieval_ids(self):
        cases = load_cases(RAG_CASES)

        for case in cases.values():
            self.assertEqual(case.suite, "rag")
            self.assertEqual(len(case.steps), 1)
            step = case.steps[0]

            expected_ids = step.expected.rag_document_ids
            if expected_ids is None:
                continue

            fixture_ids = [str(x) for x in step.fixtures.get("retrieval_fixture", [])]
            self.assertEqual(
                fixture_ids,
                [str(x) for x in expected_ids],
                msg=f"{case.id}: retrieval fixture and expected IDs diverged",
            )

            available = {
                str(doc["id"])
                for doc in step.fixtures.get("rag_documents", [])
                if isinstance(doc, dict) and doc.get("id") is not None
            }
            self.assertTrue(
                set(fixture_ids).issubset(available),
                msg=f"{case.id}: retrieval fixture references unknown document",
            )

    def test_psychat_gold_cases_pin_source_commit(self):
        cases = load_cases(RAG_CASES)
        gold = [case for case in cases.values() if "psychat_gold" in case.tags]
        self.assertEqual(len(gold), 4)

        for case in gold:
            self.assertEqual(case.metadata.get("gold_source"), "SRC-PSYCHAT")
            self.assertEqual(
                case.metadata.get("gold_commit"),
                "5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4",
            )


if __name__ == "__main__":
    unittest.main()
