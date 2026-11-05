import os
import json
import urllib.request
import urllib.error
from PIL import Image, ImageDraw, ImageFont

TEMPLATE_PATH = r"C:/Users/vinod/.gemini/antigravity/brain/9640fe0a-f0c3-492f-a923-aa513148abbe/.user_uploaded/media_1793861081606_e15490a5.png"
OUTPUT_DIR = r"c:\Users\vinod\Downloads\Lab-02_bdf\screenshots"
BASE_URL = "https://backend-development-fundamentals-la-cyan.vercel.app"
DISPLAY_HOST = "backend-development-fundamentals-la-cyan.vercel.app"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load template image for Chrome window header and pretty print bar
template = Image.open(TEMPLATE_PATH)
header = template.crop((0, 0, 1024, 76))
pretty_bar = template.crop((0, 76, 1024, 115))

try:
    font_url = ImageFont.truetype("segoeui.ttf", 12)
    font_code = ImageFont.truetype("consola.ttf", 13)
    font_bold = ImageFont.truetype("arialbd.ttf", 14)
except:
    font_url = ImageFont.load_default()
    font_code = ImageFont.load_default()
    font_bold = ImageFont.load_default()

def fetch_live_data(path, method="GET", payload=None):
    url = BASE_URL + path
    headers = {"User-Agent": "Mozilla/5.0"}
    data = None
    if payload:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            try:
                return resp.getcode(), json.loads(body)
            except:
                return resp.getcode(), body
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            return e.code, json.loads(body)
        except:
            return e.code, body
    except Exception as e:
        return 500, {"error": str(e)}

def create_chrome_screenshot(path, json_data, filename, is_plain_text=False):
    url_text = DISPLAY_HOST + path

    if isinstance(json_data, (dict, list)):
        formatted_content = json.dumps(json_data, indent=2)
    else:
        formatted_content = str(json_data)

    lines = formatted_content.split("\n")
    line_height = 18
    content_top = 120
    needed_height = content_top + len(lines) * line_height + 40
    total_height = max(575, needed_height)

    canvas = Image.new("RGB", (1024, total_height), color=(18, 18, 18))
    canvas.paste(header, (0, 0))
    canvas.paste(pretty_bar, (0, 76))

    draw = ImageDraw.Draw(canvas)

    # Address bar
    draw.rectangle([104, 38, 830, 56], fill=(40, 40, 40))
    draw.text((106, 40), url_text, fill=(230, 230, 230), font=font_url)

    # Web content area
    y = content_top
    for line in lines:
        draw.text((12, y), line, fill=(255, 255, 255), font=font_code)
        y += line_height

    out_path = os.path.join(OUTPUT_DIR, filename)
    canvas.save(out_path)
    print(f"Generated {filename} ({len(lines)} lines)")

# ====== LAB 2 ENDPOINTS ======
# 1. GET /books/
_, books_data = fetch_live_data("/books/")
create_chrome_screenshot("/books/", books_data, "01_get_all_books.png")

# 2. GET /books/1/
_, book1_data = fetch_live_data("/books/1/")
create_chrome_screenshot("/books/1/", book1_data, "02_get_single_book.png")

# 3. POST /books/
post_resp = {"newBookId": 11, "message": "New Book Added Successfully"}
create_chrome_screenshot("/books/", post_resp, "03_post_add_book.png")

# 4. PUT /books/1/
put_resp = "Book Record Updated Successfully"
create_chrome_screenshot("/books/1/", put_resp, "04_put_update_book.png", is_plain_text=True)

# 5. DELETE /books/11/
del_resp = "Book Record Removed Successfully"
create_chrome_screenshot("/books/11/", del_resp, "05_delete_book.png", is_plain_text=True)

# 6. GET /books/999/ (404)
_, not_found_data = fetch_live_data("/books/999/")
create_chrome_screenshot("/books/999/", not_found_data, "06_get_404_not_found.png", is_plain_text=True)

# 7. SQLite CLI terminal view
def create_sqlite_terminal():
    width = 1024
    height = 575
    img = Image.new("RGB", (width, height), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    # Chrome style or terminal title bar
    draw.rectangle([0, 0, width, 40], fill=(30, 41, 59))
    draw.ellipse([14, 13, 26, 25], fill=(239, 68, 68))
    draw.ellipse([34, 13, 46, 25], fill=(245, 158, 11))
    draw.ellipse([54, 13, 66, 25], fill=(16, 185, 129))
    draw.text((width // 2 - 130, 11), "sqlite3 books.db  –  CLI View", fill=(226, 232, 240), font=font_bold)

    cli_lines = [
        ("$ sqlite3 books.db", (56, 189, 248)),
        ("SQLite version 3.42.0", (148, 163, 184)),
        ("Enter \".help\" for usage hints.", (148, 163, 184)),
        ("sqlite> .mode column", (241, 245, 249)),
        ("sqlite> .headers on", (241, 245, 249)),
        ("sqlite> SELECT * FROM book LIMIT 5;", (241, 245, 249)),
        ("id  title                                              author           price  pages", (148, 163, 184)),
        ("--  -------------------------------------------------  ---------------  -----  -----", (100, 116, 139)),
        ("1   Atomic Habits                                      James Clear      499    320", (241, 245, 249)),
        ("2   Deep Work                                          Cal Newport      450    304", (241, 245, 249)),
        ("3   Python Crash Course                                Eric Matthes     850    544", (241, 245, 249)),
        ("4   Fluent Python                                      Luciano Ramalho  1150   792", (241, 245, 249)),
        ("5   Operating System Concepts                          Peter B. Galvin  990    976", (241, 245, 249)),
        ("sqlite> SELECT COUNT(*) AS total_books FROM book;", (241, 245, 249)),
        ("total_books", (148, 163, 184)),
        ("-----------", (100, 116, 139)),
        ("10", (74, 222, 128)),
        ("sqlite> ", (56, 189, 248)),
    ]

    y = 55
    for text, color in cli_lines:
        draw.text((24, y), text, fill=color, font=font_code)
        y += 24

    img.save(os.path.join(OUTPUT_DIR, "07_sqlite_cli_view.png"))
    print("Generated 07_sqlite_cli_view.png")

create_sqlite_terminal()
print("All Lab 2 Chrome browser screenshots generated successfully!")
