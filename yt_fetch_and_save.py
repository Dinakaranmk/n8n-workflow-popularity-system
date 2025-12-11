# yt_fetch_and_save.py
from dotenv import load_dotenv
import os, json, time
from googleapiclient.discovery import build

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
if not API_KEY:
    raise SystemExit("YOUTUBE_API_KEY not found in .env")

youtube = build("youtube", "v3", developerKey=API_KEY)

KEYWORDS = [
    "n8n workflow", "n8n gmail", "n8n slack", "n8n airtable",
    "n8n google sheets", "n8n whatsapp", "n8n shopify", "n8n webhook",
    "n8n cron", "n8n integration", "n8n tutorial", "n8n automation"
]

REGIONS = ["US", "IN"]
TARGET = 50   # change to higher number later
OUTPUT = "workflows_real.json"

def search_videos(q, region, max_results=25):
    try:
        resp = youtube.search().list(
            q=q, part="id", type="video", maxResults=min(max_results,50), regionCode=region
        ).execute()
        return [it['id']['videoId'] for it in resp.get('items', []) if it.get('id', {}).get('videoId')]
    except Exception as e:
        print("Search error:", e)
        return []

def fetch_stats(video_ids):
    out = {}
    if not video_ids:
        return out
    try:
        resp = youtube.videos().list(part="snippet,statistics", id=",".join(video_ids)).execute()
        for v in resp.get('items', []):
            vid = v['id']
            snip = v.get('snippet', {})
            stats = v.get('statistics', {})
            views = int(stats.get('viewCount', 0))
            likes = int(stats.get('likeCount', 0))
            comments = int(stats.get('commentCount', 0))
            out[vid] = {
                "workflow": snip.get('title', '').strip(),
                "platform": "YouTube",
                "source_id": vid,
                "url": f"https://www.youtube.com/watch?v={vid}",
                "country": None,
                "popularity_metrics": {
                    "views": views,
                    "likes": likes,
                    "comments": comments,
                    "like_to_view_ratio": round((likes / views) if views else 0.0, 6),
                    "comment_to_view_ratio": round((comments / views) if views else 0.0, 6)
                }
            }
    except Exception as e:
        print("Videos.list error:", e)
    return out

def main():
    collected = {}
    for region in REGIONS:
        for kw in KEYWORDS:
            if len(collected) >= TARGET:
                break
            ids = search_videos(kw, region, max_results=25)
            for i in range(0, len(ids), 50):
                batch = ids[i:i+50]
                stats = fetch_stats(batch)
                for vid, data in stats.items():
                    if vid in collected:
                        continue
                    data['country'] = "US" if region == "US" else "IN"
                    collected[vid] = data
                    if len(collected) >= TARGET:
                        break
                if len(collected) >= TARGET:
                    break
            time.sleep(1.2)
        if len(collected) >= TARGET:
            break

    results = list(collected.values())
    print(f"Collected {len(results)} workflows; saving to {OUTPUT}")
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("Saved. Sample entry:")
    if results:
        print(json.dumps(results[0], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
