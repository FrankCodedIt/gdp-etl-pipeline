# 🌍 Country GDP ETL Pipeline

## 📖 Overview

This project implements an **ETL (Extract, Transform, Load)** pipeline to gather, process, and store data on the **Gross Domestic Product (GDP)** of countries as published by the **International Monetary Fund (IMF)**. The GDP data (in nominal terms) is sourced from a snapshot of a Wikipedia page and is updated biannually by the IMF.

🔧 This script:
- 📥 Extracts GDP data from a specified web source,
- 🔄 Transforms GDP figures from USD millions to USD billions (rounded to 2 decimal places),
- 💾 Saves the data both to a CSV file and a local SQLite database,
- 🧾 Logs each stage of the process,
- 📊 Executes a SQL query to display countries with GDP ≥ 100 billion USD.

---

## ✅ Features

- 📝 Automated logging of ETL steps
- 🌐 Web scraping using BeautifulSoup
- 🧹 Data cleaning and transformation with pandas and NumPy
- 💽 Storage in both CSV and SQLite formats
- 🚀 Easy to extend for future updates

---

## 🧰 Prerequisites

Install the required Python packages:

```bash
pip install pandas numpy requests beautifulsoup4
```

---

## 📁 File Structure

```
.
├── Countries_by_GDP.csv         # 📄 Output CSV file
├── World_Economies.db           # 🗃️ SQLite database storing the GDP table
├── etl_project_log.txt          # 🧾 Log file capturing ETL steps
├── main_script.py               # 🧠 Main ETL script
└── README.md                    # 📘 Project documentation
```

---

## 🔍 How It Works

### 1️⃣ Extraction

- Scrapes a Wikipedia page (snapshot) containing GDP information.
- Parses table data using BeautifulSoup.
- Extracts countries and their nominal GDP values (in USD millions).

### 2️⃣ Transformation

- Cleans GDP data (removing commas).
- Converts values to billions (dividing by 1000).
- Rounds GDP values to 2 decimal places.

### 3️⃣ Load

- Saves the transformed data to a CSV file.
- Loads the data into an SQLite database as `Countries_by_GDP`.

### 4️⃣ Query

- Runs a SQL query to fetch countries with GDP ≥ 100 billion USD.

---

## 🕓 Logging

Each step of the ETL process is logged in `etl_project_log.txt` with timestamps:

```
YYYY-MMM-DD-HH:MM:SS, <Log Message>
```

---

## 🎯 Output

After execution:
- `Countries_by_GDP.csv` contains the cleaned dataset.
- `World_Economies.db` holds the `Countries_by_GDP` SQL table.
- Console displays countries with GDPs ≥ 100 billion USD.

---

## 📌 Notes

- This script uses a static archived URL to ensure consistent scraping.
- For live updates, replace the archive URL with the current Wikipedia link.
- Ideal for automation and scheduled execution as new IMF data becomes available.

---

## 👥 Author

Developed by the **IMF Data Engineering Team**  
© 2025 International Monetary Fund
