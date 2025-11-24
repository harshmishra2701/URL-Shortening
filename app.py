
from flask import Flask, request, redirect, render_template, jsonify, send_file
from database import db, init_db
from models import URL
import string, random, json, datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
with app.app_context():
    init_db()


def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        original_url = request.form["original_url"]
        custom_code = request.form.get("custom_code")

        short_code = custom_code if custom_code else generate_code()

        while URL.query.filter_by(short_code=short_code).first():
            short_code = generate_code()

        new_url = URL(
            short_code=short_code,
            original_url=original_url,
            created_at=datetime.datetime.utcnow()
        )
        db.session.add(new_url)
        db.session.commit()

        return render_template("index.html", new_url=new_url, urls=URL.query.all())

    return render_template("index.html", urls=URL.query.all())


@app.route("/<short_code>")
def redirect_short(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if url:
        url.visit_count += 1
        db.session.commit()
        return redirect(url.original_url)

    return "Invalid Short URL", 404


@app.route("/delete/<short_code>")
def delete_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if url:
        db.session.delete(url)
        db.session.commit()
    return redirect("/")


@app.route("/admin", methods=["GET", "POST"])
def admin_page():
    if request.method == "POST":
        json_file = request.files["json_file"]
        data = json.load(json_file)

        for item in data:
            code = item["short_code"]
            existing = URL.query.filter_by(short_code=code).first()

            if existing:
                existing.visit_count = max(existing.visit_count, item["visit_count"])
            else:
                new_url = URL(
                    short_code=item["short_code"],
                    original_url=item["original_url"],
                    created_at=datetime.datetime.fromisoformat(item["created_at"]),
                    visit_count=item["visit_count"],
                    meta=json.dumps(item["meta"])
                )
                db.session.add(new_url)

        db.session.commit()
        return "JSON Imported Successfully!"

    return render_template("admin.html", urls=URL.query.all())


@app.route("/export")
def export_json():
    urls = URL.query.all()
    output = []

    for url in urls:
        output.append({
            "short_code": url.short_code,
            "original_url": url.original_url,
            "created_at": url.created_at.isoformat(),
            "visit_count": url.visit_count,
            "meta": json.loads(url.meta or "{}")
        })

    path = "urls_export.json"

    with open(path, "w") as f:
        json.dump(output, f, indent=4)

    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)

