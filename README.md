# GOV IA — Real Git Source Agent

**Purpose:** Small, genuinely executable Python/LangGraph agent used as a **real GitHub source** for the GOV IA end-to-end demonstration. It contains real source code; it does not preload or fabricate any GOV IA canonical rows, assessments, risk ratings or assurance results.

## What it does

- Reads actual files from a checked-out Git repository, without executing them.
- Produces file-path and SHA-256 citations from actual bytes.
- Runs an actual two-node LangGraph workflow.
- Optionally uses the OpenAI API to explain observed source evidence; if no key is configured it clearly reports that interpretation was not executed.
- Never claims that detected code is approved canonical truth.

## Run

```bash
python -m venv .venv
# Activate your virtual environment, then:
python -m pip install -e '.[dev]'
python -m pytest -q
govia-agent-source . --question "What agent frameworks can we substantiate from these files?"
```

To activate optional model interpretation, set `OPENAI_API_KEY` **in your local shell only**, never in a committed file. Avoid using sensitive source code with external models.

## GOV IA demonstration — expected happy path

1. Publish these files in a separate GitHub repository, on `main`.
2. Connect the real repository using GOV IA GitHub Source & Acquisition.
3. Capture actual repository identity, branch/commit SHA, source snapshot and evidence.
4. Run Discovery; inspect observed, evidence-backed candidate identities.
5. Submit candidates for governed reconciliation/human approval.
6. Verify canonical objects and their lineage in the real isolated GOV IA database.
7. Inspect the actual Agent Passport and governed reads.
8. Navigate M17 risk/controls, M17.5 Assurance, and M18 Executive, displaying UNKNOWN/NOT_EVIDENCED where no human-governed facts exist.

**Important:** GOV IA's older `/api/discovery/scan` route currently marks `governedIngestion: NOT_ACTIVE`. Do not use its legacy inventory as proof of canonical ingestion. The GOV IA team must validate or bridge the governed acquisition/review flow before claiming a complete live journey.

## Security & correctness

- No API keys, customer data or confidential files in this repository.
- No direct writing to GOV IA canonical tables.
- No invented evidence, risk scores or certifications.
- This is an actual source-code repository, not a source of pre-generated demonstration business records.
