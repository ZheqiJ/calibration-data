import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import ukb_dmca_public_metadata_seed_overlay as overlay


class PublicMetadataSeedOverlayTests(unittest.TestCase):
    def test_overlay_promotes_seeded_lineage_and_preserves_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "data").mkdir(parents=True)
            (root / "evidence/logs").mkdir(parents=True)
            (root / "evidence/lineages").mkdir(parents=True)

            apps = root / "data/applications.tsv"
            apps.write_text(
                "app_id\ttitle\tpi\tinstitution\tnotes\n"
                "45761\tGenetics of cancer risk and therapy response\tProfessor Moritz Gerstung\tEBI\t\n",
                encoding="utf-8",
            )
            (root / "data/public_metadata_seeds.tsv").write_text(
                "lineage_id\trepo_or_project\tevidence_class\tmatch_grade\tcandidate_app_id\tdoi\tpubmed_id\tpublication_title\tauthors\tapplication_title\tapplication_pi\tapplication_institution\tevidence_urls\tsource_relation\tnotes\n"
                "lineage_seeded\thttps://github.com/gerstung-lab/CancerRisk\tA4_EXACT_REPO_PUBLICATION_APPLICATION_CHAIN\tconfirmed\t45761\t10.1016/s2589-7500(24)00062-1\t38789140\tMulti-cancer risk stratification based on national health data: a retrospective modelling and validation study\tMoritz Gerstung\tGenetics of cancer risk and therapy response\tProfessor Moritz Gerstung\tEBI\thttps://www.medrxiv.org/content/10.1101/2022.10.12.22280908v1\tExact public repo-publication-application chain\tSeed test\n",
                encoding="utf-8",
            )

            match_fields = [
                "notice_id", "notice_date", "notice_path", "repo_url", "repo_owner", "repo_name", "lineage_id",
                "paper_title", "doi", "pubmed_id", "paper_authors", "repo_linked_doi", "repo_linked_pmid",
                "repo_linked_publication_title", "crosswalk_pub_ids", "crosswalk_app_ids",
                "crosswalk_application_count", "crosswalk_identifier_type", "crosswalk_evidence",
                "candidate_app_id", "application_title", "application_pi", "application_institution",
                "application_linked_to_dmca_targeted_repository_lineage", "match_grade", "match_score",
                "evidence_class", "evidence_components", "deterministic_evidence_present",
                "identity_evidence_present", "contextual_evidence_present", "match_reason", "evidence_urls",
                "manual_review_needed",
            ]
            candidate_fields = [
                "lineage_id", "candidate_rank", "candidate_app_id", "application_title", "application_pi",
                "application_institution", "match_grade", "match_score", "evidence_level", "evidence_class",
                "evidence_components", "score_details", "deterministic_evidence_present",
                "identity_evidence_present", "contextual_evidence_present", "crosswalk_pub_ids",
                "crosswalk_app_ids", "crosswalk_application_count", "crosswalk_identifier_type",
                "crosswalk_evidence", "match_reason", "evidence_urls", "manual_review_needed",
            ]
            evidence_fields = [
                "lineage_id", "candidate_app_id", "evidence_class", "evidence_type", "evidence_value",
                "evidence_source", "evidence_url", "deterministic_or_fuzzy", "strength_level",
            ]

            self._write_csv(root / "ukb_dmca_lineages.csv", [
                "lineage_id", "source_repo", "repo_urls", "doi", "pubmed_id", "paper_title", "paper_authors",
                "repo_linked_doi", "repo_linked_pmid", "repo_linked_publication_title", "crosswalk_pub_ids",
                "crosswalk_app_ids", "crosswalk_application_count", "crosswalk_identifier_type",
                "crosswalk_evidence", "evidence_urls", "evidence_file",
            ], [{
                "lineage_id": "lineage_seeded",
                "source_repo": "gerstung-lab/CancerRisk",
                "repo_urls": "https://github.com/gerstung-lab/CancerRisk",
                "evidence_file": "evidence/lineages/lineage_seeded.md",
            }])
            self._write_csv(root / "ukb_dmca_repositories.csv", match_fields[:7] + match_fields[7:19] + ["evidence_urls"], [{
                "notice_id": "n1",
                "notice_date": "2025-11-25",
                "notice_path": "2025/11/foo.md",
                "repo_url": "https://github.com/gerstung-lab/CancerRisk",
                "repo_owner": "gerstung-lab",
                "repo_name": "CancerRisk",
                "lineage_id": "lineage_seeded",
            }])
            self._write_csv(root / "ukb_dmca_application_candidates.csv", candidate_fields, [{
                "lineage_id": "lineage_seeded",
                "match_grade": "unresolved",
                "match_score": "0",
                "manual_review_needed": "true",
            }])
            self._write_csv(root / "ukb_dmca_application_matches.csv", match_fields, [])
            self._write_csv(root / "ukb_dmca_unresolved.csv", match_fields, [{
                "lineage_id": "lineage_seeded",
                "match_grade": "unresolved",
                "manual_review_needed": "true",
            }])
            self._write_csv(root / "ukb_dmca_manual_review.csv", match_fields, [{
                "lineage_id": "lineage_seeded",
                "match_grade": "unresolved",
                "manual_review_needed": "true",
            }])
            self._write_csv(root / "ukb_dmca_application_match_evidence.csv", evidence_fields, [])
            (root / "evidence/logs/result_summary.json").write_text(
                '{"cases_needing_extra_data": ["lineage_seeded"], "match_grade_counts": {"unresolved": 1}}',
                encoding="utf-8",
            )
            (root / "evidence/lineages/lineage_seeded.md").write_text("# lineage_seeded\n", encoding="utf-8")

            summary = overlay.apply_public_metadata_seeds(root, apps)

            matches = self._read_csv(root / "ukb_dmca_application_matches.csv")
            unresolved = self._read_csv(root / "ukb_dmca_unresolved.csv")
            candidates = self._read_csv(root / "ukb_dmca_application_candidates.csv")
            evidence = self._read_csv(root / "ukb_dmca_application_match_evidence.csv")
            lineages = self._read_csv(root / "ukb_dmca_lineages.csv")

            self.assertEqual(matches[0]["candidate_app_id"], "45761")
            self.assertEqual(matches[0]["match_grade"], "confirmed")
            self.assertEqual(matches[0]["application_linked_to_dmca_targeted_repository_lineage"], "true")
            self.assertEqual(unresolved, [])
            self.assertEqual(candidates[0]["candidate_rank"], "1")
            self.assertEqual(candidates[0]["manual_review_needed"], "false")
            self.assertEqual(lineages[0]["repo_linked_doi"], "10.1016/s2589-7500(24)00062-1")
            self.assertTrue(any(row["evidence_type"] == "public_metadata_seed" for row in evidence))
            self.assertTrue(any(row["evidence_type"] == "A4_EXACT_REPO_PUBLICATION_APPLICATION_CHAIN" for row in evidence))
            self.assertEqual(summary["match_grade_counts"]["confirmed"], 1)
            self.assertEqual(summary["public_metadata_seed_matched_lineages"], 1)
            self.assertEqual(summary["cases_needing_extra_data"], [])
            self.assertEqual(summary["lineages_with_doi"], 1)
            self.assertEqual(summary["lineages_with_pmid"], 1)
            self.assertIn("Public Metadata Seed Audit", (root / "evidence/lineages/lineage_seeded.md").read_text(encoding="utf-8"))

            persisted_summary = json.loads((root / "evidence/logs/result_summary.json").read_text(encoding="utf-8"))
            self.assertEqual(persisted_summary["unique_application_count"], 1)

    @staticmethod
    def _write_csv(path, fields, rows):
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fields)
            writer.writeheader()
            writer.writerows(rows)

    @staticmethod
    def _read_csv(path):
        with path.open("r", encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))


if __name__ == "__main__":
    unittest.main()
