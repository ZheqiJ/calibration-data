import tempfile
import unittest
from pathlib import Path

from scripts.ukb_dmca_pipeline import (
    extract_github_targets,
    matched_notice_terms,
    notice_matches,
    parse_applications_tsv,
    parse_notice_date,
    repo_enrich,
)


class PipelineParserTests(unittest.TestCase):
    def test_multiline_application_parser(self):
        text = (
            "app_id\ttitle\tpi\tinstitution\tnotes\n"
            "123\tHeart imaging\tDr Ada Smith\tExample University\tFirst line\n"
            "continued notes\n"
            "456\tGenetics\tProf Ben Jones\tExample Institute\tSingle line\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "apps.tsv"
            path.write_text(text, encoding="utf-8")
            rows = parse_applications_tsv(path)

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["app_id"], "123")
        self.assertIn("continued notes", rows[0]["notes"])
        self.assertEqual(rows[1]["pi"], "Prof Ben Jones")

    def test_parse_notice_date_with_suffix(self):
        self.assertEqual(
            parse_notice_date("2025/11/2025-11-13-uk-biobank-5.md"),
            "2025-11-13",
        )

    def test_notice_match_requires_ukb_signal_in_notice_text(self):
        text = "# UK Biobank\nReported content includes a UKB phenotype file."

        self.assertTrue(notice_matches("2025/11/2025-11-13-uk-biobank.md", text))
        self.assertIn("UK Biobank", matched_notice_terms(text))
        self.assertIn("UKB", matched_notice_terms(text))

    def test_notice_match_rejects_unrelated_notice(self):
        text = "# JetBrains\nReported content includes cracked software keys."

        self.assertFalse(notice_matches("2015/2015-07-06-jetbrains.md", text))
        self.assertEqual(matched_notice_terms(text), "")

    def test_notice_match_does_not_match_ukb_inside_longer_token(self):
        text = "# Unrelated\nThis text mentions a token like aukbzz but not the acronym."

        self.assertFalse(notice_matches("2025/05/2025-05-29-packt.md", text))
        self.assertEqual(matched_notice_terms(text), "")

    def test_extract_file_target_from_blob_url(self):
        text = (
            "Reported content: "
            "https://github.com/example/repo/blob/main/data/ukb_fields.csv"
        )
        targets = extract_github_targets(text)

        self.assertEqual(len(targets), 1)
        self.assertEqual(targets[0]["repo_owner"], "example")
        self.assertEqual(targets[0]["repo_name"], "repo")
        self.assertEqual(targets[0]["offending_file_path"], "data/ukb_fields.csv")
        self.assertEqual(targets[0]["target_scope"], "single_file")

    def test_repo_enrich_handles_null_github_description(self):
        class FakeClient:
            def fetch(self, url):
                return {
                    "status": 200,
                    "body": (
                        '{"id": 1, "description": null, "fork": false, '
                        '"created_at": "2020-01-01T00:00:00Z", '
                        '"pushed_at": "2020-01-02T00:00:00Z"}'
                    ),
                }

        rows = repo_enrich(
            FakeClient(),
            [
                {
                    "repo_url": "https://github.com/example/repo",
                    "repo_owner": "example",
                    "repo_name": "repo",
                    "offending_file_path": "data/ukb.csv",
                    "offending_file_name": "ukb.csv",
                    "target_scope": "single_file",
                    "alleged_data_type": "phenotype",
                    "direct_app_ids": "",
                    "notice_id": "n1",
                    "notice_date": "2024-01-01",
                    "notice_path": "2024/01/notice.md",
                }
            ],
            wayback_limit=0,
        )

        self.assertEqual(rows[0]["repo_status"], "live")
        self.assertIn("https://github.com/example/repo", rows[0]["_text"])


if __name__ == "__main__":
    unittest.main()
