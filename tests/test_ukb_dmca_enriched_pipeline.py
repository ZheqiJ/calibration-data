import base64
import json
import unittest

from scripts import ukb_dmca_enriched_pipeline as enriched
from scripts import ukb_dmca_pipeline as base


class EnrichedMatchingTests(unittest.TestCase):
    def setUp(self):
        enriched.install_enrichment()

    def test_readme_application_id_becomes_confirmed(self):
        class FakeClient:
            def fetch(self, url, *args, **kwargs):
                if url.endswith("/readme"):
                    body = {
                        "encoding": "base64",
                        "content": base64.b64encode(b"This repository uses UK Biobank application 123 for cardiac MRI.").decode(),
                        "html_url": "https://github.com/example/repo/blob/main/README.md",
                    }
                    return {"status": 200, "body": json.dumps(body)}
                return {
                    "status": 200,
                    "body": json.dumps(
                        {
                            "id": 1,
                            "description": "Cardiac MRI model",
                            "fork": False,
                            "created_at": "2020-01-01T00:00:00Z",
                        }
                    ),
                }

        repos = base.repo_enrich(
            FakeClient(),
            [
                {
                    "repo_url": "https://github.com/example/repo",
                    "repo_owner": "example",
                    "repo_name": "repo",
                    "offending_file_path": "README.md",
                    "offending_file_name": "README.md",
                    "target_scope": "repository",
                    "alleged_data_type": "imaging",
                    "direct_app_ids": "",
                    "notice_id": "n1",
                    "notice_date": "2024-01-01",
                    "notice_path": "2024/01/notice.md",
                }
            ],
            wayback_limit=0,
        )
        lineages = base.make_lineages(repos)
        _, final = base.candidate_tables(
            lineages,
            [
                {
                    "app_id": "123",
                    "title": "Cardiac MRI model",
                    "pi": "Dr Ada Smith",
                    "institution": "Example University",
                    "notes": "UK Biobank imaging",
                }
            ],
            limit=10,
        )

        self.assertEqual(final[lineages[0]["lineage_id"]]["grade"], "confirmed")

    def test_paper_identifier_plus_public_text_scores_probable(self):
        lineage = {
            "lineage_id": "lineage_example",
            "_direct_app_ids": "",
            "_repo_text": "https://github.com/example/repo data/cardiac_mri.csv imaging",
            "_paper_text": "Cardiac MRI risk prediction Ada Smith 10.1234/example",
            "_readme_text": "Publication: Cardiac MRI risk prediction by Ada Smith at Example University",
            "doi": "10.1234/example",
            "pubmed_id": "",
            "alleged_data_types": "imaging",
            "evidence_urls": "https://doi.org/10.1234/example",
        }
        app = {
            "app_id": "456",
            "title": "Cardiac MRI risk prediction",
            "pi": "Ada Smith",
            "institution": "Example University",
            "notes": "UK Biobank cardiac imaging",
        }
        indexed = dict(app)
        indexed.update(
            {
                "_title": base.tokens(app["title"]),
                "_pi": base.tokens(app["pi"]),
                "_inst": base.tokens(app["institution"]),
                "_notes": base.tokens(app["notes"]),
            }
        )

        score, components, _, level = base.score(lineage, indexed)
        top = {"candidate_app_id": "456", "match_score": score, "evidence_components": base.uniq(components)}
        grade, _, _ = base.final_label(top, None, [])

        self.assertEqual(level, "B")
        self.assertEqual(grade, "probable")


if __name__ == "__main__":
    unittest.main()
