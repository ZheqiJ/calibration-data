import tempfile
import unittest
from pathlib import Path

from scripts.ukb_dmca_pipeline import (
    extract_github_targets,
    parse_applications_tsv,
    parse_notice_date,
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


if __name__ == "__main__":
    unittest.main()
