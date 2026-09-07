-- Customer intelligence analysis queries for CXM Intelligence Hub.
-- The queries are written for a warehouse-style table that could live in
-- Snowflake, Azure SQL, PostgreSQL or another analytics database.

-- 1. Base scored account view.
CREATE OR REPLACE VIEW crm_scored_accounts AS
SELECT
  account,
  industry,
  stage,
  owner,
  revenue,
  probability,
  tickets,
  satisfaction,
  last_contact_days,
  email,
  duplicate,
  opportunity,
  stack,
  valid_email,
  stale_contact,
  high_support_load,
  low_satisfaction,
  ai_score,
  segment,
  next_action,
  ROUND(revenue * probability / 100.0, 0) AS weighted_pipeline
FROM cleaned_crm_accounts;

-- 2. Executive pipeline summary for a Power BI dashboard.
SELECT
  stage,
  COUNT(*) AS account_count,
  SUM(weighted_pipeline) AS weighted_pipeline,
  ROUND(AVG(ai_score), 1) AS average_ai_score,
  SUM(CASE WHEN ai_score >= 76 THEN 1 ELSE 0 END) AS priority_accounts
FROM crm_scored_accounts
GROUP BY stage
ORDER BY
  CASE stage
    WHEN 'Discovery' THEN 1
    WHEN 'Qualified' THEN 2
    WHEN 'Proposal' THEN 3
    WHEN 'Negotiation' THEN 4
    WHEN 'Won' THEN 5
    ELSE 6
  END;

-- 3. Accounts to prioritise for client engagement or proposal follow-up.
SELECT
  account,
  industry,
  stage,
  ai_score,
  weighted_pipeline,
  opportunity,
  next_action
FROM crm_scored_accounts
WHERE ai_score >= 76
  AND duplicate = FALSE
  AND valid_email = TRUE
ORDER BY ai_score DESC, weighted_pipeline DESC;

-- 4. CRM data-quality audit before reporting or campaign outreach.
SELECT
  account,
  email,
  duplicate,
  valid_email,
  stale_contact,
  high_support_load,
  low_satisfaction,
  CASE
    WHEN duplicate THEN 'Merge duplicate CRM records'
    WHEN valid_email = FALSE THEN 'Validate email before outreach'
    WHEN stale_contact THEN 'Refresh account contact date'
    WHEN high_support_load THEN 'Review service case backlog'
    WHEN low_satisfaction THEN 'Escalate customer experience risk'
    ELSE 'No immediate data-quality action'
  END AS recommended_cleanup_action
FROM crm_scored_accounts
WHERE duplicate = TRUE
   OR valid_email = FALSE
   OR stale_contact = TRUE
   OR high_support_load = TRUE
   OR low_satisfaction = TRUE
ORDER BY account;

-- 5. Technology opportunity mix for consulting capacity planning.
SELECT
  technology,
  COUNT(*) AS account_count,
  SUM(weighted_pipeline) AS weighted_pipeline
FROM (
  SELECT account, weighted_pipeline, TRIM(value) AS technology
  FROM crm_scored_accounts,
  LATERAL SPLIT_TO_TABLE(stack, ';')
) tech
GROUP BY technology
ORDER BY account_count DESC, weighted_pipeline DESC;

-- 6. Business development shortlist by industry.
SELECT
  industry,
  COUNT(*) AS accounts,
  ROUND(AVG(ai_score), 1) AS average_ai_score,
  SUM(weighted_pipeline) AS weighted_pipeline,
  SUM(CASE WHEN segment = 'At-risk service' THEN 1 ELSE 0 END) AS at_risk_accounts,
  SUM(CASE WHEN stack ILIKE '%AI%' THEN 1 ELSE 0 END) AS ai_opportunities,
  SUM(CASE WHEN stack ILIKE '%Power BI%' THEN 1 ELSE 0 END) AS dashboard_opportunities
FROM crm_scored_accounts
GROUP BY industry
HAVING COUNT(*) >= 1
ORDER BY weighted_pipeline DESC;
