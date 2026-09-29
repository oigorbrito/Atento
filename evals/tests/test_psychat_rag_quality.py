import unittest

from evals.spikes.psychat.rag_quality_report import validate_multilingual


def paired_report():
    rows = []
    for index in range(4):
        pair_id = f"pair-{index}"
        rows.append(
            {
                "pair_id": pair_id,
                "query_language": "pt-BR",
                "expected_id": str(index),
            }
        )
        rows.append(
            {
                "pair_id": pair_id,
                "query_language": "zh-CN",
                "expected_id": str(index),
            }
        )
    return {
        "metric_version": "psychat-multilingual-microbenchmark-v0.2",
        "quality_claim": True,
        "embedding_model": "text-embedding-v4",
        "hit_rate_by_language": {
            "pt-BR": 0.75,
            "zh-CN": 1.0,
        },
        "mrr_by_language": {
            "pt-BR": 0.6,
            "zh-CN": 0.9,
        },
        "zh_minus_pt_hit_rate_gap": 0.25,
        "zh_minus_pt_mrr_gap": 0.3,
        "rows": rows,
    }


class PsyChatRagQualityContractTest(unittest.TestCase):
    def test_rejects_pt_only_report_as_cross_language_evidence(self):
        report = paired_report()
        report["hit_rate_by_language"] = {"pt-BR": 0.75}
        report["mrr_by_language"] = {"pt-BR": 0.6}
        report["rows"] = [
            row for row in report["rows"]
            if row["query_language"] == "pt-BR"
        ]

        with self.assertRaisesRegex(
            AssertionError,
            "pt-BR \+ zh-CN",
        ):
            validate_multilingual(report)

    def test_rejects_skipped_multilingual_run(self):
        with self.assertRaisesRegex(
            AssertionError,
            "absent/skipped",
        ):
            validate_multilingual(
                {
                    "quality_claim": False,
                    "status": "SKIPPED_NO_EMBEDDING_CREDENTIAL",
                }
            )

    def test_accepts_four_complete_language_pairs(self):
        summary = validate_multilingual(paired_report())

        self.assertEqual(summary["gold_pair_count"], 4)
        self.assertEqual(summary["query_count"], 8)
        self.assertEqual(
            set(summary["hit_rate_by_language"]),
            {"pt-BR", "zh-CN"},
        )


if __name__ == "__main__":
    unittest.main()
