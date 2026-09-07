# CXM Intelligence Hub

CRM analytics, AI lead scoring and customer intelligence dashboard for a
technology consulting internship portfolio.

Live project:
[https://suu-susu.github.io/cxm-ai-customer-intelligence-dashboard/](https://suu-susu.github.io/cxm-ai-customer-intelligence-dashboard/)

## Project Summary

CXM Intelligence Hub is an end-to-end mini project that turns synthetic CRM
records into a business development and consulting workflow. It is designed to
show how customer data can be cleaned, scored, analysed, visualised and converted
into practical client recommendations.

The project is public-safe: all records are synthetic and the dashboard is not
connected to a real client CRM. The workflow is still structured like a real
technology consulting task.

## Why This Is More Than a Web Page

The repository includes four layers:

- **Data pipeline:** `pipeline/clean_crm_data.py` loads CRM records, cleans data,
  flags quality issues, calculates AI-style priority scores and exports cleaned
  outputs.
- **SQL analysis:** `sql/customer_intelligence_queries.sql` contains warehouse
  queries for scored account views, pipeline summaries, priority accounts,
  data-quality audits and technology opportunity analysis.
- **Dashboard:** `index.html` provides an interactive browser dashboard with CRM
  filters, KPI cards, charts, account table, CSV import/export and proposal
  generation.
- **Architecture documentation:** `docs/architecture.md` explains the business
  problem, data flow, scoring logic, cloud mapping and next steps.

## Business Problem

Consulting and business development teams need to understand which accounts are
worth prioritising, which customer records need cleanup, and which technology
opportunities are strongest. Raw CRM exports do not automatically answer those
questions.

This project demonstrates a workflow for:

- identifying high-value accounts;
- finding duplicate or invalid CRM records;
- segmenting customers by opportunity and risk;
- summarising pipeline value;
- mapping accounts to AI, Salesforce, Power BI, Azure, Snowflake, SQL and API
  opportunities;
- turning account context into a proposal outline.

## Role Fit

The project maps strongly to a Technology Stream / Business Consulting internship:

- Python and SQL thinking through data cleaning, scoring and query logic;
- Power BI-style dashboard reporting;
- AI lead scoring and next-best-action recommendations;
- Salesforce-style CRM pipeline workflow;
- API, Azure and Snowflake integration positioning;
- business consulting output through a generated proposal outline.

## Dashboard Features

- CRM search and filters by account, owner, industry, pipeline stage, AI segment
  and minimum score.
- AI-style lead scoring based on revenue, probability, urgency, service pain and
  data quality.
- Data-quality checks for duplicate records, invalid email fields, stale contacts
  and high support volume.
- Salesforce-style pipeline view.
- Power BI-style revenue trend.
- Customer segment and technology opportunity charts.
- Scored CRM account table with risks and next action.
- SQL-style query logic panel.
- Generative AI proposal assistant.
- CSV import and scored CSV export.

## Repository Structure

```text
.
|-- index.html
|-- sample-crm-data.csv
|-- pipeline/
|   `-- clean_crm_data.py
|-- sql/
|   `-- customer_intelligence_queries.sql
`-- docs/
    `-- architecture.md
```

## Run Locally

Open `index.html` directly, or serve the folder with a local server:

```powershell
python -m http.server 8794 --bind 127.0.0.1
```

To run the Python data pipeline:

```powershell
python pipeline/clean_crm_data.py
```

The script writes cleaned outputs to the `data/` folder:

- `data/cleaned_crm_accounts.csv`
- `data/crm_pipeline_summary.csv`

## Limitations

- The dataset is synthetic.
- The AI score is explainable rule-based scoring, not a trained model.
- The web dashboard runs in the browser and does not persist imported records.
- Salesforce, Azure and Snowflake are represented as architecture-ready
  integration targets rather than live production connections.

## Next Steps

- Add a mock CRM REST API.
- Store cleaned records in SQLite or PostgreSQL.
- Add automated tests for scoring rules.
- Build a Power BI version from the cleaned CSV outputs.
- Add a small backend service for scoring and proposal generation.
