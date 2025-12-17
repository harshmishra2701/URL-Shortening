import os
import string
import random
import json
import datetime
from flask import Flask, request, redirect, render_template, send_file
from pymongo import MongoClient
import re
from dotenv import load_dotenv
import qrcode
from PIL import Image, ImageDraw, ImageFont

load_dotenv()



def sanitize_url(url):
    url = url.strip()
    url = re.sub(r"\s+", "", url)
    return url

def is_valid_url(url):
    pattern = re.compile(
        r"^(https?:\/\/)"
        r"([\w\-]+\.)+[\w\-]+"
        r"(\/[\w\-._~:/?#\[\]@!$&'()*+,;=%]*)?$",
        re.IGNORECASE
    )
    return re.match(pattern, url)

def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def generate_qr_with_logo(data, filename):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=3,
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    logo = Image.open("static/images/logo.jpg")

    
    qr_width, qr_height = qr_img.size
    logo_size = qr_width // 4
    logo = logo.resize((logo_size, logo_size))

    
    pos = (
        (qr_width - logo_size) // 2,
        (qr_height - logo_size) // 2
    )

    qr_img.paste(logo, pos, mask=logo if logo.mode == "RGBA" else None)

    save_path = f"static/qr/{filename}"
    qr_img.save(save_path)

    return save_path




app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client["url_shortener"]
urls = db["urls"]



@app.route("/", methods=["GET", "POST"])
def index():
    new_short_url = None
    error = None
    qr_data = None
    qr_enabled = False
    qr_type = "short"
    qr_image = None

    if request.method == "POST":
        original_url = request.form.get("original_url", "")
        qr_enabled = request.form.get("generate_qr") == "on"
        qr_type = request.form.get("qr_type", "short") if qr_enabled else "short"

        original_url = sanitize_url(original_url)

        if not original_url:
            error = "URL cannot be empty."
        elif not is_valid_url(original_url):
            error = "Please enter a valid URL (must start with http:// or https://)."
        else:
            short_code = generate_code()
            while urls.find_one({"short_code": short_code}):
                short_code = generate_code()

            doc = {
                "short_code": short_code,
                "original_url": original_url,
                "created_at": datetime.datetime.utcnow(),
                "visit_count": 0,
                "meta": {}
            }

            urls.insert_one(doc)
            new_short_url = request.host_url + short_code

            if qr_enabled:
             qr_data = new_short_url if qr_type == "short" else original_url

            qr_filename = f"{short_code}.png"
            qr_path = generate_qr_with_logo(qr_data, qr_filename)


    all_urls = list(urls.find().sort("created_at", -1))
    qr_image = f"/static/qr/{qr_filename}" if qr_enabled else None

    return render_template(
        "index.html",
        urls=all_urls,
        new_short_url=new_short_url,
        error=error,
        qr_data=qr_data,
        qr_enabled=qr_enabled,
        qr_type=qr_type,
        qr_image=qr_image
     )

@app.route("/<short_code>")
def redirect_short(short_code):
    doc = urls.find_one_and_update(
        {"short_code": short_code},
        {"$inc": {"visit_count": 1}}
    )
    if doc:
        return redirect(doc["original_url"])
    return "Invalid or expired short URL", 404

@app.route("/delete/<short_code>")
def delete_url(short_code):
    urls.delete_one({"short_code": short_code})
    return redirect("/")

@app.route("/admin", methods=["GET", "POST"])
def admin_page():
    if request.method == "POST":
        if "json_file" not in request.files:
            return "No file uploaded!", 400

        json_file = request.files["json_file"]

        if json_file.filename == "":
            return "Please select a JSON file", 400

        if not json_file.filename.lower().endswith(".json"):
            return "Invalid file type! Only .json allowed", 400

        try:
            data = json.load(json_file)
        except:
            return "Invalid JSON format!", 400

        if not isinstance(data, list):
            return "JSON must contain a list of objects", 400

        required_fields = ["short_code", "original_url", "created_at", "visit_count", "meta"]

        for index, item in enumerate(data):
            if not isinstance(item, dict):
                return f"Item {index} must be an object", 400
            for f in required_fields:
                if f not in item:
                    return f"Missing field '{f}' at index {index}", 400
            if not item["original_url"].startswith(("http://", "https://")):
                return f"Invalid URL at index {index}", 400

            try:
                datetime.datetime.fromisoformat(item["created_at"])
            except:
                return f"Invalid created_at timestamp at index {index}", 400

            if not isinstance(item["visit_count"], int):
                return f"visit_count must be integer at index {index}", 400

            if not isinstance(item["meta"], dict):
                return f"meta must be dictionary at index {index}", 400
        for item in data:
            created_at = datetime.datetime.fromisoformat(item["created_at"])
            existing = urls.find_one({"short_code": item["short_code"]})
            if existing:
                urls.update_one(
                    {"short_code": item["short_code"]},
                    {"$set": {"visit_count": max(existing["visit_count"], item["visit_count"])}}
                )
            else:
                urls.insert_one({
                    "short_code": item["short_code"],
                    "original_url": item["original_url"],
                    "created_at": created_at,
                    "visit_count": item["visit_count"],
                    "meta": item["meta"]
                })

    all_urls = list(urls.find().sort("created_at", -1))
    return render_template("admin.html", urls=all_urls)

@app.route("/export")
def export_json():
    export = []
    for u in urls.find():
        export.append({
            "short_code": u["short_code"],
            "original_url": u["original_url"],
            "created_at": u["created_at"].isoformat(),
            "visit_count": u["visit_count"],
            "meta": u["meta"]
        })

    path = "urls_export.json"
    with open(path, "w") as f:
        json.dump(export, f, indent=4)

    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
