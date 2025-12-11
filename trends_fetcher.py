# trends_fetcher.py
from pytrends.request import TrendReq
import json, time

OUTPUT = "workflows_trends.json"

KEYWORDS = [
    "n8n workflow",
    "n8n automation",
    "n8n gmail",
    "n8n webhook",
    "n8n slack",
    "n8n whatsapp",
    "n8n airtable",
    "n8n google sheets",
    "n8n integration",
    "n8n cron",
    "n8n tutorial"
]

COUNTRIES = ["US", "IN"]

pytrends = TrendReq(hl='en-US', tz=330)

def fetch_trends(keyword, country):
    try:
        pytrends.build_payload([keyword], geo=country, timeframe="today 3-m")
        df = pytrends.interest_over_time()

        if df.empty:
            return None
        
        values = df[keyword].tolist()
        if len(values) < 2:
            return None

        start_val = values[0]
        end_val = values[-1]
        change = ((end_val - start_val) / start_val * 100) if start_val > 0 else 0

        return {
            "workflow": keyword,
            "platform": "GoogleTrends",
            "country": country,
            "popularity_metrics": {
                "trend_values": values[-10:],   # last 10 data points
                "start_value": start_val,
                "end_value": end_val,
                "trend_percentage_change": round(change, 2)
            }
        }
    except Exception as e:
        print("Error for:", keyword, country, e)
        return None

def main():
    all_results = []

    for keyword in KEYWORDS:
        for country in COUNTRIES:
            print(f"Fetching trends for {keyword} ({country})...")
            data = fetch_trends(keyword, country)
            if data:
                all_results.append(data)
            time.sleep(1)

    print(f"Collected {len(all_results)} trend entries")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print("Saved to", OUTPUT)
    if all_results:
        print("Sample entry:")
        print(json.dumps(all_results[0], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
