# Input Data

Place the UK Biobank approved applications TSV here only if you want a
repo-local input copy.

The pipeline defaults to:

```bash
/mnt/data/application (1)(1).txt
```

You can point to another copy without changing the repository:

```bash
python3 scripts/ukb_dmca_pipeline.py --applications "/path/to/applications.tsv"
```

The expected fields are `app_id`, `title`, `pi`, `institution`, and `notes`.
Participant-level UK Biobank data must never be stored in this repository.
