from database import db

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_code = db.Column(db.String(20), unique=True, nullable=False)
    original_url = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    visit_count = db.Column(db.Integer, default=0)
    meta = db.Column(db.Text, default="{}")
