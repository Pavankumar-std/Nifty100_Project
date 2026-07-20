-- ===========================================
-- Exploratory SQL Queries
-- Nifty100 Project - Sprint 1
-- ===========================================

-- Query 1
-- Total Companies

SELECT COUNT(*) AS total_companies
FROM companies;


-- Query 2
-- Top 10 Companies by ROE

SELECT
    id,
    company_name,
    roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;


-- Query 3
-- Top 10 Companies by ROCE

SELECT
    id,
    company_name,
    roce_percentage
FROM companies
ORDER BY roce_percentage DESC
LIMIT 10;


-- Query 4
-- Top 10 Companies by Market Capitalization

SELECT
    company_id,
    year,
    market_capitalization
FROM market_cap
ORDER BY market_capitalization DESC
LIMIT 10;


-- Query 5
-- Highest Sales

SELECT
    company_id,
    year,
    sales
FROM profitandloss
ORDER BY sales DESC
LIMIT 10;


-- Query 6
-- Highest Net Profit

SELECT
    company_id,
    year,
    net_profit
FROM profitandloss
ORDER BY net_profit DESC
LIMIT 10;


-- Query 7
-- Companies with ROE Greater Than 20

SELECT
    id,
    company_name,
    roe_percentage
FROM companies
WHERE roe_percentage > 20
ORDER BY roe_percentage DESC;


-- Query 8
-- Companies with ROCE Greater Than 20

SELECT
    id,
    company_name,
    roce_percentage
FROM companies
WHERE roce_percentage > 20
ORDER BY roce_percentage DESC;


-- Query 9
-- Average ROE and ROCE

SELECT
    AVG(roe_percentage) AS average_roe,
    AVG(roce_percentage) AS average_roce
FROM companies;


-- Query 10
-- Number of Financial Records per Company

SELECT
    company_id,
    COUNT(*) AS total_years
FROM profitandloss
GROUP BY company_id
ORDER BY total_years DESC;