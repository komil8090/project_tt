import requests
import json
import os
import time
import hashlib
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed


OUT_DIR = "responses"      
MAX_WORKERS = 8            
TIMEOUT = 10      
MAX_RETRIES = 3            
BACKOFF_FACTOR = 1.0      


def safe_filename_from_url(url, idx=None):
    """URL asosida xavfsiz fayl nomi yaratadi (domain + hash + vaqt)."""
    parsed = urlparse(url)
    domain = parsed.netloc or "unknown"
    h = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
    ts = int(time.time())
    part_idx = f"_{idx}" if idx is not None else ""
    return f"{domain}_{h}_{ts}{part_idx}.json"

def ensure_out_dir(path):
    """Agar chiqish papkasi mavjud bo‘lmasa — yaratadi."""
    os.makedirs(path, exist_ok=True)

def fetch_url(url, idx=None):
    """Berilgan URL’ga  yuborish (retry bilan)."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, timeout=TIMEOUT)
            response.raise_for_status()
   
            return response.json()
        except (requests.RequestException, ValueError) as e:
            print(f"[{idx}] ⚠️ Urinish {attempt}/{MAX_RETRIES} muvaffaqiyatsiz: {url} ({e})")
            if attempt < MAX_RETRIES:
                sleep_time = BACKOFF_FACTOR * attempt
                time.sleep(sleep_time)
            else:
                print(f"[{idx}] ❌ Hamma urinishlar muvaffaqiyatsiz bo‘ldi: {url}")
                return None

def save_response(url, data, idx=None):
    """Javobni JSON faylga saqlash."""
    ensure_out_dir(OUT_DIR)
    filename = safe_filename_from_url(url, idx)
    filepath = os.path.join(OUT_DIR, filename)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[{idx}] ✅ Saqlandi: {filepath}")
    except Exception as e:
        print(f"[{idx}] ❌ Faylni saqlashda xato: {e}")

def process_url(url, idx=None):
    """Bitta URL uchun: yuklab olish va saqlash."""
    data = fetch_url(url, idx)
    if data is not None:
        save_response(url, data, idx)

def main(urls):
    start = time.time()
    print(f"🔄 {len(urls)} ta URL yuklanmoqda...")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_url, url, i) for i, url in enumerate(urls)]
        for _ in as_completed(futures):
            pass  

    elapsed = time.time() - start
    print(f"✅ Tayyor! {len(urls)} ta sorov {elapsed:.2f} sekundda bajarildi.")


if __name__ == "__main__":
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/users/1",
        "https://jsonplaceholder.typicode.com/todos/1",
    ]
    main(urls)
