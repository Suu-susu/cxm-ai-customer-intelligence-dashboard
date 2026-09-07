"""
CRM cleaning and lead-scoring pipeline for CXM Intelligence Hub.

This script uses a small synthetic CRM dataset so the portfolio project can be
shared publicly without exposing client data. The workflow mirrors the kind of
analysis that could sit before a Salesforce, Snowflake, Azure SQL or Power BI
dashboard:

1. Load CRM account records from CSV.
2. Standardise stage names and numeric fields.
3. Flag duplicate accounts, invalid emails, stale contacts and high support load.
4. Calculate an explainable AI-style priority score.
5. Export cleaned records and summary metrics for dashboard or SQL analysis.
"""

from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from statistics import mean


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "sample-crm-data.csv"
OUTPUT_DIR = PROJECT_ROOT / "data"
CLEAN_OUTPUT_PATH = OUTPUT_DIR / "cleaned_crm_accounts.csv"
SUMMARY_OUTPUT_PATH = OUTPUT_DIR / "crm_pipeline_summary.csv"

VALID_STAGES = {"Discovery", "Qualified", "Proposal", "Negotiation", "Won"}
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
STAGE_WEIGHT = {
    "Discovery": 8,
    "Qualified": 17,
    "Proposal": 28,
    "Negotiation": 35,
    "Won": 15,
}


@dataclass
class CleanAccount:
    account: str
    industry: str
    stage: str
    owner: str
    revenue: int
    probability: int
    tickets: int
    satisfaction: int
    last_contact_days: int
    email: str
    duplicate: bool
    opportunity: str
    stack: str
    notes: str
    valid_email: bool
    stale_contact: bool
    high_support_load: bool
    low_satisfaction: bool
    ai_score: int
    segment: str
    next_action: str


def to_int(value: str, fallback: int = 0) -> int:
    try:
        return int(float(str(value).strip()))
    except (TypeError, ValueError):
        return fallback


def to_bool(value: str) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def normalise_stage(stage: str) -> str:
    stage = str(stage).strip().title()
    return stage if stage in VALID_STAGES else "Discovery"


def calculate_score(row: dict[str, str], duplicate_names: set[str]) -> int:
    revenue = to_int(row.get("revenue", "0"))
    probability = to_int(row.get("probability", "0"))
    tickets = to_int(row.get("tickets", "0"))
    satisfaction = to_int(row.get("satisfaction", "0"))
    last_contact = to_int(row.get("lastContact", "0"))
    account = row.get("account", "").strip().lower()
    email = row.get("email", "")

    stage = normalise_stage(row.get("stage", ""))
    revenue_component = min(30, revenue / 4000)
    probability_component = probability * 0.28
    urgency_component = max(0, 18 - last_contact) * 0.75
    pain_component = min(18, tickets * 0.55 + max(0, 75 - satisfaction) * 0.28)
    data_quality_penalty = 0

    if account in duplicate_names or not EMAIL_PATTERN.match(email):
        data_quality_penalty += 10

    score = (
        revenue_component
        + probability_component
        + urgency_component
        + pain_component
        + STAGE_WEIGHT[stage]
        - data_quality_penalty
    )
    return max(0, min(100, round(score)))


def segment_for(score: int, tickets: int, satisfaction: int, duplicate: bool) -> str:
    if score >= 76:
        return "High-value priority"
    if score >= 62:
        return "Proposal-ready"
    if tickets >= 22 or satisfaction < 65:
        return "At-risk service"
    if score >= 45:
        return "Qualified opportunity"
    return "Nurture"


def next_action_for(record: CleanAccount) -> str:
    if record.duplicate or not record.valid_email:
        return "Clean CRM record before outreach"
    if record.ai_score >= 76:
        return "Schedule proposal follow-up this week"
    if record.high_support_load or record.low_satisfaction:
        return "Run service-risk discovery call"
    if record.stage in {"Proposal", "Negotiation"}:
        return "Prepare tailored client proposal"
    return "Send discovery email with dashboard pilot offer"


def clean_records(rows: list[dict[str, str]]) -> list[CleanAccount]:
    account_counts = Counter(row.get("account", "").strip().lower() for row in rows)
    duplicate_names = {name for name, count in account_counts.items() if name and count > 1}
    cleaned: list[CleanAccount] = []

    for row in rows:
        revenue = to_int(row.get("revenue", "0"))
        probability = to_int(row.get("probability", "0"))
        tickets = to_int(row.get("tickets", "0"))
        satisfaction = to_int(row.get("satisfaction", "0"))
        last_contact = to_int(row.get("lastContact", "0"))
        email = row.get("email", "").strip()
        account_key = row.get("account", "").strip().lower()
        duplicate = to_bool(row.get("duplicate", "")) or account_key in duplicate_names
        score = calculate_score(row, duplicate_names)

        record = CleanAccount(
            account=row.get("account", "Unknown Account").strip(),
            industry=row.get("industry", "Unknown").strip(),
            stage=normalise_stage(row.get("stage", "")),
            owner=row.get("owner", "Unassigned").strip(),
            revenue=revenue,
            probability=probability,
            tickets=tickets,
            satisfaction=satisfaction,
            last_contact_days=last_contact,
            email=email,
            duplicate=duplicate,
            opportunity=row.get("opportunity", "CRM analytics pilot").strip(),
            stack=row.get("stack", "SQL; Power BI").strip(),
            notes=row.get("notes", "").strip(),
            valid_email=bool(EMAIL_PATTERN.match(email)),
            stale_contact=last_contact > 14,
            high_support_load=tickets >= 20,
            low_satisfaction=satisfaction < 70,
            ai_score=score,
            segment=segment_for(score, tickets, satisfaction, duplicate),
            next_action="",
        )
        record.next_action = next_action_for(record)
        cleaned.append(record)

    return sorted(cleaned, key=lambda item: item.ai_score, reverse=True)


def summarise(records: list[CleanAccount]) -> list[dict[str, object]]:
    by_stage: dict[str, list[CleanAccount]] = defaultdict(list)
    for record in records:
        by_stage[record.stage].append(record)

    summary = []
    for stage in ["Discovery", "Qualified", "Proposal", "Negotiation", "Won"]:
        stage_records = by_stage.get(stage, [])
        weighted_pipeline = sum(r.revenue * r.probability / 100 for r in stage_records)
        summary.append(
            {
                "stage": stage,
                "accounts": len(stage_records),
                "weighted_pipeline": round(weighted_pipeline),
                "average_ai_score": round(mean([r.ai_score for r in stage_records]), 1)
                if stage_records
                else 0,
                "data_quality_issues": sum(
                    r.duplicate or not r.valid_email or r.stale_contact for r in stage_records
                ),
            }
        )
    return summary


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    with INPUT_PATH.open("r", newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    cleaned = clean_records(rows)
    write_csv(CLEAN_OUTPUT_PATH, [asdict(record) for record in cleaned])
    write_csv(SUMMARY_OUTPUT_PATH, summarise(cleaned))

    print(f"Input records: {len(rows)}")
    print(f"Cleaned records: {len(cleaned)}")
    print(f"Priority accounts: {sum(r.ai_score >= 76 for r in cleaned)}")
    print(f"Data quality issues: {sum(r.duplicate or not r.valid_email or r.stale_contact for r in cleaned)}")
    print(f"Wrote {CLEAN_OUTPUT_PATH}")
    print(f"Wrote {SUMMARY_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
