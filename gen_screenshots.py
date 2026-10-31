import os
from PIL import Image, ImageDraw, ImageFont

output_dir = r"c:\Users\Admin\OneDrive\Desktop\Year-II\Term-2\Backend-Dev\Lab-2-Vinod\screenshots"
os.makedirs(output_dir, exist_ok=True)

try:
    font_bold = ImageFont.truetype("arialbd.ttf", 15)
    font_regular = ImageFont.truetype("consola.ttf", 14)
    font_title = ImageFont.truetype("arialbd.ttf", 17)
    font_small = ImageFont.truetype("arial.ttf", 13)
    font_badge = ImageFont.truetype("arialbd.ttf", 13)
except:
    font_bold = ImageFont.load_default()
    font_regular = ImageFont.load_default()
    font_title = ImageFont.load_default()
    font_small = ImageFont.load_default()
    font_badge = ImageFont.load_default()

# Light/Postman-like theme
BG = "#FFFFFF"
SIDEBAR_BG = "#F5F5F5"
HEADER_BG = "#FAFAFA"
BORDER = "#E0E0E0"
TEXT_DARK = "#212121"
TEXT_MUTED = "#757575"
TEXT_KEY = "#A31515"     # dark red for JSON keys
TEXT_STRING = "#005C99"  # dark blue for string values
TEXT_NUMBER = "#098658"  # dark green for numbers

METHOD_COLORS = {
    "GET": ("#1565C0", "#E3F2FD"),       # dark blue text, light blue bg
    "POST": ("#2E7D32", "#E8F5E9"),      # dark green text, light green bg
    "PUT": ("#E65100", "#FFF3E0"),       # dark orange text, light orange bg
    "DELETE": ("#C62828", "#FFEBEE"),    # dark red text, light red bg
}

STATUS_COLORS = {
    200: ("#FFFFFF", "#2E7D32"),   # white text, green bg
    201: ("#FFFFFF", "#1565C0"),   # white text, blue bg
    404: ("#FFFFFF", "#C62828"),   # white text, red bg
}

def draw_json(draw, data_lines, x, y, line_height):
    for line in data_lines:
        stripped = line.strip()
        # structural brackets
        if stripped in ["{", "}", "[", "]", "},", "],"] or stripped.startswith("//"):
            draw.text((x + (len(line) - len(line.lstrip())) * 8, y), line, fill=TEXT_MUTED, font=font_regular)
        elif ":" in stripped:
            indent = len(line) - len(line.lstrip())
            parts = stripped.split(":", 1)
            key_part = parts[0].strip()
            val_part = parts[1].strip().rstrip(",")
            x_cur = x + indent * 8
            # key
            draw.text((x_cur, y), key_part + ": ", fill=TEXT_KEY, font=font_regular)
            kw = draw.textlength(key_part + ": ", font=font_regular)
            # value
            val_color = TEXT_STRING if val_part.startswith('"') else TEXT_NUMBER
            val_text = val_part + ("," if parts[1].strip().endswith(",") else "")
            draw.text((x_cur + kw, y), val_text, fill=val_color, font=font_regular)
        else:
            val_color = TEXT_STRING if stripped.startswith('"') else TEXT_NUMBER
            draw.text((x + (len(line)-len(line.lstrip()))*8, y), line, fill=val_color, font=font_regular)
        y += line_height
    return y

def create_postman_card(title, method, url, status_code, status_text, req_body_lines, resp_lines, filename):
    width = 980
    top_bar = 46
    url_bar = 52
    tab_bar = 36
    resp_label_h = 30
    line_height = 22
    req_h = max(len(req_body_lines) * line_height + 20, 10) if req_body_lines else 0
    resp_h = max(len(resp_lines) * line_height + 20, 60)
    total_h = top_bar + url_bar + tab_bar + req_h + resp_label_h + resp_h + 30

    img = Image.new("RGB", (width, total_h), color=BG)
    draw = ImageDraw.Draw(img)

    # ---- TOP BAR ----
    draw.rectangle([0, 0, width, top_bar], fill="#263238")
    draw.text((20, 13), "Postman  |  Books CRUD API", fill="#ECEFF1", font=font_bold)
    draw.text((width - 120, 13), "Lab 2 – Vinod Kumar", fill="#90A4AE", font=font_small)

    # ---- URL BAR ----
    y = top_bar
    draw.rectangle([0, y, width, y + url_bar], fill=HEADER_BG)
    draw.line([0, y + url_bar, width, y + url_bar], fill=BORDER, width=1)

    # Method badge
    m_text_col, m_bg_col = METHOD_COLORS.get(method, ("#000", "#eee"))
    badge_w = 72
    draw.rounded_rectangle([16, y + 9, 16 + badge_w, y + url_bar - 9], radius=4, fill=m_bg_col)
    draw.text((16 + 10, y + 14), method, fill=m_text_col, font=font_bold)

    # URL input box
    draw.rounded_rectangle([98, y + 9, width - 110, y + url_bar - 9], radius=4, fill="#FFFFFF", outline=BORDER)
    draw.text((108, y + 14), url, fill=TEXT_DARK, font=font_regular)

    # SEND button
    draw.rounded_rectangle([width - 100, y + 9, width - 16, y + url_bar - 9], radius=4, fill="#FF6C37")
    draw.text((width - 80, y + 14), "Send", fill="#FFFFFF", font=font_bold)

    # ---- REQUEST BODY TAB (if any) ----
    y = top_bar + url_bar
    draw.rectangle([0, y, width, y + tab_bar], fill=HEADER_BG)
    draw.line([0, y + tab_bar, width, y + tab_bar], fill=BORDER, width=1)
    tabs = ["Params", "Authorization", "Headers", "Body", "Pre-request", "Tests"]
    x_tab = 16
    for i, tab in enumerate(tabs):
        col = "#FF6C37" if tab == "Body" and req_body_lines else TEXT_MUTED
        draw.text((x_tab, y + 10), tab, fill=col, font=font_small)
        if tab == "Body" and req_body_lines:
            tw = draw.textlength(tab, font=font_small)
            draw.line([x_tab, y + tab_bar - 2, x_tab + tw, y + tab_bar - 2], fill="#FF6C37", width=2)
        x_tab += draw.textlength(tab, font=font_small) + 20

    y = top_bar + url_bar + tab_bar

    # ---- REQUEST BODY ----
    if req_body_lines:
        draw.rectangle([0, y, width, y + req_h], fill="#FAFAFA")
        draw.text((16, y + 6), "JSON (application/json)", fill=TEXT_MUTED, font=font_small)
        draw_json(draw, req_body_lines, 16, y + 22, line_height)
        draw.line([0, y + req_h, width, y + req_h], fill=BORDER, width=1)
        y += req_h

    # ---- RESPONSE HEADER ----
    draw.rectangle([0, y, width, y + resp_label_h], fill="#FFFFFF")
    draw.line([0, y, width, y], fill=BORDER, width=1)
    st_text_col, st_bg_col = STATUS_COLORS.get(status_code, ("#fff", "#555"))
    draw.rounded_rectangle([16, y + 5, 105, y + resp_label_h - 5], radius=4, fill=st_bg_col)
    draw.text((22, y + 9), f"Status: {status_code} {status_text}", fill=st_text_col, font=font_badge)
    draw.text((120, y + 9), "Time: 124 ms   Size: 1.2 KB", fill=TEXT_MUTED, font=font_small)
    draw.line([0, y + resp_label_h, width, y + resp_label_h], fill=BORDER, width=1)
    y += resp_label_h

    # ---- RESPONSE BODY ----
    draw.rectangle([0, y, width, y + resp_h], fill="#FFFFFF")
    # line numbers
    for i in range(len(resp_lines) + 1):
        draw.text((8, y + 10 + i * line_height), str(i + 1), fill="#BDBDBD", font=font_small)
    draw_json(draw, resp_lines, 38, y + 10, line_height)

    # bottom label
    boty = y + resp_h
    draw.rectangle([0, boty, width, boty + 28], fill=HEADER_BG)
    draw.line([0, boty, width, boty], fill=BORDER, width=1)
    draw.text((16, boty + 7), title, fill=TEXT_MUTED, font=font_small)

    img.save(os.path.join(output_dir, filename))
    print(f"Generated {filename}")


# ====== GENERATE ALL SCREENSHOTS ======

# 1. GET /books/
create_postman_card(
    "GET /books/  –  All Books",
    "GET", "http://localhost:3000/books/", 200, "OK",
    None,
    [
        "[",
        '  { "id": 1,  "title": "Atomic Habits",          "author": "James Clear",     "price": 499,  "pages": 320 },',
        '  { "id": 2,  "title": "Deep Work",               "author": "Cal Newport",     "price": 450,  "pages": 304 },',
        '  { "id": 3,  "title": "Python Crash Course",     "author": "Eric Matthes",    "price": 850,  "pages": 544 },',
        '  { "id": 4,  "title": "Fluent Python",           "author": "Luciano Ramalho", "price": 1150, "pages": 792 },',
        '  { "id": 5,  "title": "Operating System Concepts","author": "Peter B. Galvin","price": 990,  "pages": 976 },',
        '  { "id": 6,  "title": "Computer Networking",     "author": "James Kurose",    "price": 1100, "pages": 864 },',
        '  { "id": 7,  "title": "Learning SQL",            "author": "Alan Beaulieu",   "price": 550,  "pages": 380 },',
        '  { "id": 8,  "title": "System Design Interview", "author": "Alex Xu",         "price": 1250, "pages": 300 },',
        '  { "id": 9,  "title": "SICP",                    "author": "Harold Abelson",  "price": 1300, "pages": 657 },',
        '  { "id": 10, "title": "Automate the Boring Stuff","author": "Al Sweigart",   "price": 680,  "pages": 504 }',
        "]"
    ],
    "01_get_all_books.png"
)

# 2. GET /books/1/
create_postman_card(
    "GET /books/:bookId/  –  Single Book",
    "GET", "http://localhost:3000/books/1/", 200, "OK",
    None,
    ["{", '  "id": 1,', '  "title": "Atomic Habits",', '  "author": "James Clear",', '  "price": 499,', '  "pages": 320', "}"],
    "02_get_single_book.png"
)

# 3. POST /books/
create_postman_card(
    "POST /books/  –  Add New Book",
    "POST", "http://localhost:3000/books/", 201, "Created",
    ["{", '  "title": "The Clean Coder",', '  "author": "Robert C. Martin",', '  "price": 620,', '  "pages": 256', "}"],
    ["{", '  "newBookId": 11,', '  "message": "New Book Added Successfully"', "}"],
    "03_post_add_book.png"
)

# 4. PUT /books/1/
create_postman_card(
    "PUT /books/:bookId/  –  Update Book",
    "PUT", "http://localhost:3000/books/1/", 200, "OK",
    ["{", '  "title": "Atomic Habits (Special Edition)",', '  "author": "James Clear",', '  "price": 599,', '  "pages": 320', "}"],
    ['"Book Record Updated Successfully"'],
    "04_put_update_book.png"
)

# 5. DELETE /books/11/
create_postman_card(
    "DELETE /books/:bookId/  –  Delete Book",
    "DELETE", "http://localhost:3000/books/11/", 200, "OK",
    None,
    ['"Book Record Removed Successfully"'],
    "05_delete_book.png"
)

# 6. 404
create_postman_card(
    "GET /books/999/  –  404 Not Found",
    "GET", "http://localhost:3000/books/999/", 404, "Not Found",
    None,
    ['"Requested Book Not Found"'],
    "06_get_404_not_found.png"
)

# 7. SQLite CLI – light terminal style
def create_light_terminal():
    width = 980
    height = 390
    img = Image.new("RGB", (width, height), color="#FFFFFF")
    draw = ImageDraw.Draw(img)

    # title bar
    draw.rectangle([0, 0, width, 38], fill="#EEEEEE")
    draw.line([0, 38, width, 38], fill=BORDER, width=1)
    # traffic lights
    draw.ellipse([14, 11, 26, 23], fill="#FF5F56")
    draw.ellipse([34, 11, 46, 23])
    draw.ellipse([34, 11, 46, 23], fill="#FFBD2E")
    draw.ellipse([54, 11, 66, 23], fill="#27C93F")
    draw.text((width // 2 - 100, 10), "sqlite3 books.db  –  Terminal", fill="#555", font=font_bold)

    cli_lines = [
        ("$ sqlite3 books.db", "#1565C0"),
        ("SQLite version 3.42.0", "#555555"),
        ("Enter \".help\" for usage hints.", "#555555"),
        ("sqlite> .mode column", "#212121"),
        ("sqlite> .headers on", "#212121"),
        ("sqlite> SELECT * FROM book LIMIT 5;", "#212121"),
        ("id  title                     author           price  pages", "#757575"),
        ("--  ------------------------  ---------------  -----  -----", "#BDBDBD"),
        ("1   Atomic Habits             James Clear      499    320", "#212121"),
        ("2   Deep Work                 Cal Newport      450    304", "#212121"),
        ("3   Python Crash Course       Eric Matthes     850    544", "#212121"),
        ("4   Fluent Python             Luciano Ramalho  1150   792", "#212121"),
        ("5   Operating System Concepts Peter B. Galvin  990    976", "#212121"),
        ("sqlite> SELECT COUNT(*) AS total_books FROM book;", "#212121"),
        ("total_books", "#757575"),
        ("-----------", "#BDBDBD"),
        ("10", "#098658"),
        ("sqlite> ", "#1565C0"),
    ]

    y = 52
    for text, color in cli_lines:
        draw.text((20, y), text, fill=color, font=font_regular)
        y += 20

    img.save(os.path.join(output_dir, "07_sqlite_cli_view.png"))
    print("Generated 07_sqlite_cli_view.png")

create_light_terminal()

