from __future__ import annotations

import unittest

from atento_apollo import ROLE, load_project


class ProjectContractTests(unittest.TestCase):
    def test_role_manifest_matches_package(self) -> None:
        project = load_project()
        self.assertEqual(project["agent"], ROLE)
        self.assertEqual(project["authority"]["role_id"], ROLE)
        self.assertFalse(project["authority"]["caller_selectable"])

    def test_has_no_direct_agent_dependencies(self) -> None:
        project = load_project()
        self.assertEqual(project["dependencies"]["agents"], [])

    def test_common_runtime_is_isolated_nanoclaw_group(self) -> None:
        project = load_project()
        self.assertEqual(project["runtime"]["chassis"], "nanoclaw")
        self.assertTrue(project["runtime"]["group_isolation_required"])


if __name__ == "__main__":
    unittest.main()
