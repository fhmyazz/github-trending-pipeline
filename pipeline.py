import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime
import os
import time

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    print("GITHUB_TOKEN not found. Please fill in .env file")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

SEARCH_URL = "https://api.github.com/search/repositories"

print("[INFO]: Setup is completed...")

def extract(language="python", min_stars=1000, max_pages=2, per_page=10):
    print("[INFO]: Starting Extraction...")
    """
        Extract repos from Github API
        Return list of repo dictionaries
    """
    repos = []

    params = {
        "q": f"language:{language} stars:>{min_stars}",
        "sort": "stars",
        "order": "desc",
        "per_page": per_page
    }

    for page in range (1, max_pages+1):
        params["page"] = page
        print(f"[INFO]: Fetching page: {page}")

        response = requests.get(SEARCH_URL, headers=HEADERS, params=params)

        remaining = int(response.headers.get("X-RateLimit-Remaining", 0))
        print(f"[INFO]: Rate limit remaining: {remaining}")

        if response.status_code != 200:
            print(f"[ERROR]: {response.status_code} {response.text}")
            break
        
        data = response.json()
        items = data.get("items", [])
        repos.extend(items)

        if len(items) == 0:
            break

        time.sleep(1)
       
    print(f"[INFO]: Extracted {len(repos)} repos")
    return repos

def transform(repos):
    """
    Transform raw API into clean DataFrame
    Returns DataFrame
    """

    if not repos:
        print("[INFO]: No data to transform")
        return pd.DataFrame()

         # Buat DataFrame dari list repos
    df = pd.DataFrame([{
        "id": r["id"],
        "name": r["name"],
        "full_name": r["full_name"],
        "owner": r["owner"]["login"],
        "language": r["language"],
        "stars": r["stargazers_count"],
        "forks": r["forks_count"],
        "open_issues": r["open_issues_count"],
        "description": r["description"],
        "created_at": pd.to_datetime(r["created_at"]),
        "updated_at": pd.to_datetime(r["updated_at"]),
        "url": r["html_url"]
    } for r in repos])

    initial_count = len(df)
    df = df.drop_duplicates(subset="id")
    print(f"[INFO]: Removed {initial_count - len(df)} duplicate id")

    df["description"] = df["description"].fillna("No Description")
    df["fetched_at"] = datetime.now()

    def stars_category(stars):
        if stars >= 100000:
            return "legendary"
        elif stars >= 10000:
            return "popular"
        else:
            return "rising"

    df["stars_category"] = df["stars"].apply(stars_category)
    df = df.sort_values("stars", ascending=False)

    print(f"Transform completed. {len(df)} rows, {len(df.columns)} columns")
    return df

def load(df, db_path="data/repos.db", table_name="repositories"):
    """
    Load DataFrame into SQLite Database
    """

    if df.empty:
        print("[INFO]: No Data to Load")
        return
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    engine = create_engine(f"sqlite:///{db_path}")

    df.to_sql(table_name, engine, if_exists="replace", index=False)

    print(f"[INFO]: Loaded {len(df)} rows to db {db_path}, table: {table_name}")
    

if __name__ == "__main__":
    repos = extract()
    # print("Sample Repos: ", repos[0]["full_name"] if repos else "None")
    df = transform(repos)
    # print(df.head())
    load(df)
    print("[INFO]: Pipeline completed successfully")