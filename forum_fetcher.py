# forum_fetcher.py
import requests, json, time

BASE_URL = "https://community.n8n.io"
OUTPUT = "workflows_forum.json"
TARGET = 50  # number of topics to fetch (change later)

def fetch_latest_topics(page=0):
    """Fetch latest topics from n8n forum public API."""
    url = f"{BASE_URL}/latest.json?page={page}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print("Error fetching:", e)
        return None

def extract_topic_data(topic):
    """Convert a forum topic to workflow-like structure."""
    return {
        "workflow": topic.get("title", ""),
        "platform": "Forum",
        "source_id": topic.get("id"),
        "url": f"{BASE_URL}/t/{topic.get('slug')}/{topic.get('id')}",
        "country": "GLOBAL",
        "popularity_metrics": {
            "views": topic.get("views", 0),
            "likes": topic.get("like_count", 0),
            "replies": topic.get("reply_count", 0),
            "unique_contributors": topic.get("participants_count", 0),
            "engagement_score": round(
                topic.get("like_count", 0)
                + topic.get("reply_count", 0),
                2
            )
        }
    }

def main():
    print("Fetching forum topics...")

    collected = []
    page = 0

    while len(collected) < TARGET:
        data = fetch_latest_topics(page)
        if not data:
            break

        topics = data.get("topic_list", {}).get("topics", [])
        if not topics:
            break

        for topic in topics:
            collected.append(extract_topic_data(topic))
            if len(collected) >= TARGET:
                break

        page += 1
        time.sleep(1)

    print(f"Collected {len(collected)} forum workflows")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(collected, f, indent=2, ensure_ascii=False)

    print("Saved to", OUTPUT)
    if collected:
        print("Sample entry:")
        print(json.dumps(collected[0], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
