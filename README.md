# GitHub Trending ETL Pipeline

An end-to-end ETL pipeline built with Python, pandas, and Google BigQuery to collect, transform, and analyze trending GitHub repositories.

This project is part of my Data Engineering learning journey, focusing on building reproducible data pipelines instead of standalone scripts.

---

## 📌 Overview

The pipeline extracts trending repositories from the GitHub REST API, performs data cleaning and transformation using pandas, and loads the processed data into Google BigQuery for analytics.

```
GitHub REST API
        │
        ▼
   Extract (Python)
        │
        ▼
Transform (pandas)
  - Data cleaning
  - Deduplication
  - Custom categorization
        │
        ▼
Load (BigQuery)
        │
        ▼
Analytics-ready Table
github_data.repositories
```

---

## ✨ Features

- Fetch trending GitHub repositories through the GitHub REST API
- Clean and normalize raw JSON responses
- Remove duplicate records
- Apply custom repository categorization
- Load structured data into Google BigQuery
- Produce an analytics-ready table for SQL exploration

---

## 🛠 Tech Stack

| Component | Technology |
|------------|----------------|
| Language | Python |
| Data Processing | pandas |
| API | GitHub REST API |
| Data Warehouse | Google BigQuery |
| Authentication | Google Cloud Service Account |
| Environment | Jupyter Notebook / Virtual Environment |

---

## 🚀 Pipeline Steps

### 1. Extract

- Connect to GitHub REST API
- Retrieve trending repositories
- Convert JSON response into a pandas DataFrame

### 2. Transform

- Select relevant columns
- Clean missing values
- Remove duplicate repositories
- Apply custom categorization logic
- Filter repositories with more than 1000 stars

### 3. Load

- Authenticate to Google Cloud
- Push transformed data into BigQuery
- Create an analytics-ready table

Destination table:

```
github_data.repositories
```
