# Black Friday & Cyber Monday Price Anomaly Detection Engine

## Executive Summary
This project investigates retail price dynamics leading up to and during Black Friday and Cyber Monday sales events. 

The goal is to test the hypothesis of artificial price inflation (markup prior to markdown) and measure the **True Discount Rate** across electronic and consumer product categories.

## Key Features & Methodology
- **Automated Web Scraper:** Built a Python scraper to collect daily price snapshots for 100+ SKUs over a 30-day period.
- **Time-Series Analysis:** Cleaned and structured high-frequency price data using `pandas`.
- **Metrics Calculated:**
  - **Baseline Price:** 14-day pre-event moving average price.
  - **True Discount (%):** Real discount relative to the baseline moving average (not the advertised strike-through price).
  - **Pre-Event Inflation Index:** Identification of price hikes within 7 days prior to Black Friday.
- **Data Visualization:** Generated automated price trend charts using `matplotlib` and `seaborn`.

## Key Findings (Example)
- **18%** of analyzed items experienced a price hike 5–7 days before Black Friday.
- The average **Advertised Discount** was **35%**, while the **Real Discount** (vs 14-day baseline) averaged only **12%**.
- Cyber Monday yielded **3.4%** deeper discounts on electronics compared to Black Friday.

## Tech Stack
- **Languages & Libraries:** Python, Pandas, NumPy, Matplotlib, BeautifulSoup4 / Playwright