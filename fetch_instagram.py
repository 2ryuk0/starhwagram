import requests, os, json, hashlib

API_KEY = os.getenv("APIFY_KEY")
USERNAME = "_starhwa_"

os.makedirs("images", exist_ok=True)
os.makedirs("data", exist_ok=True)

# 1. Apify Instagram Scraper 호출
url = f"https://api.apify.com/v2/acts/apify~instagram-scraper/run-sync?token={API_KEY}"
payload = {"usernames": [USERNAME]}

response = requests.post(url, json=payload).json()
items = response.get("instagramUsers", [])[0].get("latestPosts", [])

# 2. JSON 저장
with open("data/feed.json", "w", encoding="utf-8") as f:
    json.dump(items, f, indent=2, ensure_ascii=False)

# 3. 이미지 다운로드
for post in items:
    if "displayUrl" not in post:
        continue

    img_url = post["displayUrl"]
    h = hashlib.md5(img_url.encode()).hexdigest()
    filename = f"images/{h}.jpg"

    if not os.path.exists(filename):
        img = requests.get(img_url).content
        with open(filename, "wb") as f:
            f.write(img)

print("Done.")
