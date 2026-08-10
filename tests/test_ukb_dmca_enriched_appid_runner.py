import csv
import tempfile
import unittest
from pathlib import Path

from scripts import ukb_dmca_enriched_appid_runner as runner


class EnrichedAppIdRunnerTests(unittest.TestCase):
    def test_normalize_doi_and_pmid(self):
        self.assertEqual(runner.normalize_doi("https://doi.org/10.1234/ABC."), "10.1234/abc")
        self.assertEqual(runner.normalize_pmid("PMID: 12345678"), "12345678")

    def test_schema_crosswalk_doi_to_single_application(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            schema19 = root / "schema19.tsv"
            schema24 = root / "schema24.tsv"
            schema19.write_text("publication_id\tdoi\ttitle\tauthors\nP100\t10.1234/example\tPaper\tA Smith\n", encoding="utf-8")
            schema24.write_text("publication_id\tapp_id\nP100\t1001\n", encoding="utf-8")

            crosswalk = runner.load_schema_crosswalk(str(schema19), str(schema24))
            hits = runner._crosswalk_hits({"doi": "10.1234/example", "pubmed_id": ""}, crosswalk)

            self.assertEqual(hits["pub_ids"], ["100"])
            self.assertEqual(hits["app_ids"], ["1001"])
            self.assertEqual(hits["evidence_classes"], ["A2_DOI_UKB_CROSSWALK"])

    def test_postprocess_confirms_unique_crosswalk_application(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "evidence/logs").mkdir(parents=True)
            (root / "evidence/lineages").mkdir(parents=True)

            apps = root / "applications.tsv"
            apps.write_text("app_id\ttitle\tpi\tinstitution\tnotes\n1001\tHeart paper\tA Smith\tOxford\tLinked DOI 10.1234/example\n", encoding="utf-8")
            schema19 = root / "schema19.tsv"
            schema24 = root / "schema24.tsv"
            schema19.write_text("publication_id\tdoi\ttitle\tauthors\nP100\t10.1234/example\tHeart paper\tA Smith\n", encoding="utf-8")
            schema24.write_text("publication_id\tapp_id\nP100\t1001\n", encoding="utf-8")

            self._write_csv(root / "ukb_dmca_lineages.csv", ["lineage_id", "source_repo", "repo_urls", "doi", "pubmed_id", "evidence_urls", "evidence_file"], [
                {"lineage_id": "lineage-1", "source_repo": "alice/repo", "repo_urls": "https://github.com/alice/repo", "doi": "10.1234/example", "pubmed_id": "", "evidence_urls": "https://doi.org/10.1234/example", "evidence_file": "evidence/lineages/lineage-1.md"}
            ])
            self._write_csv(root / "ukb_dmca_repositories.csv", ["notice_id", "notice_date", "notice_path", "repo_url", "repo_owner", "repo_name", "lineage_id"], [
                {"notice_id": "n1", "notice_date": "2020-01-01", "notice_path": "2020/01/foo.md", "repo_url": "https://github.com/alice/repo", "repo_owner": "alice", "repo_name": "repo", "lineage_id": "lineage-1"}
            ])
            self._write_csv(root / "ukb_dmca_application_candidates.csv", ["lineage_id", "candidate_app_id", "match_score", "match_grade"], [])
            (root / "evidence/logs/result_summary.json").write_text("{}", encoding="utf-8")
            (root / "evidence/lineages/lineage-1.md").write_text("# lineage-1\n", encoding="utf-8")

            runner.postprocess_outputs([
                "--output-dir", str(root),
                "--applications", str(apps),
                "--schema19", str(schema19),
                "--schema24", str(schema24),
            ])

            with (root / "ukb_dmca_application_matches.csv").open() as handle:
                matches = list(csv.DictReader(handle))
            with (root / "ukb_dmca_application_match_evidence.csv").open() as handle:
                evidence = list(csv.DictReader(handle))
            self.assertEqual(matches[0]["candidate_app_id"], "1001")
            self.assertEqual(matches[0]["match_grade"], "confirmed")
            self.assertTrue(any(row["evidence_type"] == "A2_DOI_UKB_CROSSWALK" for row in evidence))

    @staticmethod
    def _write_csv(path, fields, rows):
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fields)
            writer.writeheader()
            writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
