# CXM Intelligence Hub Architecture

This project is a public portfolio demo built with synthetic CRM records. It is
not connected to a real client system, but the architecture shows how the same
workflow could be extended into a real consulting environment.

## Business Problem

Consulting teams often receive customer and sales information from CRM exports,
support tools, spreadsheets and campaign systems. The raw records are useful but
not always ready for business development decisions. Common issues include
duplicates, invalid contact details, stale follow-up activity, unclear pipeline
priority and weak visibility across customer segments.

CXM Intelligence Hub turns those records into a practical workflow:

- clean CRM data before reporting;
- score accounts by commercial value, urgency and customer risk;
- identify which accounts need proposal follow-up or service discovery;
- visualise the pipeline in a dashboard;
- create a structured proposal outline from selected account context.

## Data Flow

```text
Synthetic CRM CSV
        |
        v
Python cleaning and scoring pipeline
        |
        +--> cleaned_crm_accounts.csv
        +--> crm_pipeline_summary.csv
        |
        v
SQL warehouse model
        |
        v
Power BI-style dashboard and customer intelligence views
        |
        v
AI-style recommendation and proposal assistant
```

## Components

| Layer | Current implementation | Real-world extension |
| --- | --- | --- |
| Source data | `sample-crm-data.csv` with synthetic customer records | Salesforce export, CRM API, support desk API, campaign platform or spreadsheet upload |
| Data cleaning | `pipeline/clean_crm_data.py` flags duplicates, invalid emails, stale contacts and service risk | Scheduled Python job, Azure Function, Data Factory pipeline or dbt model |
| Analytics model | `sql/customer_intelligence_queries.sql` defines scored views and dashboard queries | Snowflake, Azure SQL, PostgreSQL or Databricks warehouse |
| Dashboard | `index.html` with filters, KPI cards, charts and CRM table | Power BI, embedded dashboard, internal portal or Salesforce dashboard |
| AI workflow | Explainable scoring and proposal assistant using selected CRM context | Generative AI assistant connected to approved CRM fields and proposal templates |

## Scoring Logic

The AI-style score is deliberately explainable rather than a black-box model. It
combines:

- revenue value;
- sales probability;
- urgency from recent contact activity;
- support ticket volume;
- satisfaction risk;
- penalties for duplicate accounts and invalid email fields.

This makes the output easier to explain in a business consulting interview: the
score is not just a number, it is a decision aid that leads to a next action.

## Dashboard Views

The web dashboard demonstrates:

- CRM filters by industry, stage, segment and minimum AI score;
- weighted pipeline value;
- high-priority account count;
- Salesforce-style pipeline stages;
- Power BI-style revenue trend;
- customer segment distribution;
- technology opportunity mix across SQL, Power BI, Azure, Snowflake, Salesforce,
  API and AI;
- data-quality checks;
- SQL-style query logic;
- AI proposal outline generation.

## Technology Mapping

This project is designed for a technology consulting internship where the work
may involve both business and technical tasks.

| Internship area | Project evidence |
| --- | --- |
| Market research | Industry and account segmentation for business development prioritisation |
| Proposal preparation | Proposal assistant converts account context into a consulting outline |
| Client engagement | Account table recommends next actions and discussion themes |
| CRM and Salesforce support | Pipeline stages, account health and duplicate checks mirror CRM support work |
| AI business use cases | Lead scoring and account-level proposal generation demonstrate practical AI use cases |
| Data Engineering | Python pipeline and SQL model show repeatable data preparation logic |
| Cloud | Architecture is ready to map onto Azure SQL, Snowflake and dashboard services |
| Power BI | Dashboard structure mirrors KPI, trend and segmentation reporting |

## Limitations and Next Steps

Current version:

- uses synthetic data only;
- runs fully in the browser for public portfolio safety;
- uses explainable scoring logic rather than a trained machine learning model;
- does not store uploaded data after page refresh.

Possible next steps:

- connect to a mock CRM REST API;
- store cleaned records in SQLite or PostgreSQL;
- add automated tests for scoring rules;
- build a Power BI version using the cleaned CSV outputs;
- add a small backend API for scoring and proposal generation;
- create a short case-study page explaining business problem, method and results.
