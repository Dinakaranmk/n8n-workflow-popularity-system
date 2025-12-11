# merge_datasets.py
import json, os
from pathlib import Path

INPUT_YT = "workflows_real.json"
INPUT_FORUM = "workflows_forum.json"
INPUT_TRENDS = "workflows_trends.json"
OUTPUT = "workflows_final.json"

def load_json(path):
    if not Path(path).exists():
        print(f"[WARN] {path} not found.")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize_item(item, platform):
    # Ensure required keys exist and normalize names
    out = {}
    out["workflow"] = item.get("workflow") or item.get("title") or ""
    out["platform"] = platform
    out["source_id"] = str(item.get("source_id") or item.get("id") or item.get("workflow")[:30])
    out["url"] = item.get("url") or item.get("link") or ""
    country = item.get("country") or item.get("country_code") or item.get("geo") or ""
    out["country"] = country if country else ("global" if platform == "Forum" else "global")
    # popularity_metrics: expect dict; if missing, create minimal structure
    pm = item.get("popularity_metrics") or {}
    out["popularity_metrics"] = pm
    return out

def dedupe(items):
    seen = set()
    out = []
    for it in items:
        key = (it.get("platform","").lower(), it.get("source_id",""))
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
    return out

def main():
    print("Loading datasets...")
    yt = load_json(INPUT_YT)
    forum = load_json(INPUT_FORUM)
    trends = load_json(INPUT_TRENDS)

    print(f"Loaded: YouTube={len(yt)}, Forum={len(forum)}, Trends={len(trends)}")

    merged = []

    # Normalize YouTube
    for it in yt:
        merged.append(normalize_item(it, "YouTube"))

    # Normalize Forum
    for it in forum:
        merged.append(normalize_item(it, "Forum"))

    # Normalize Trends
    for it in trends:
        # trends entries may already have fields similar - set platform name "Google"
        merged.append(normalize_item(it, "Google"))

    print("Deduplicating...")
    merged = dedupe(merged)
    print(f"After dedupe: total {len(merged)} items")

    # Very small enrichment: if YouTube items have no country set, keep existing country if present
    # (already handled in normalize_item)

    # Save final
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

    print("Wrote", OUTPUT)

if __name__ == "__main__":
    main()
