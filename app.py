import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.secret_key = 'secret_key'

# подключение к БД
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Visit(db.Model):
    __tablename__ = 'visits'

    id = db.Column(db.Integer, primary_key=True)
    visit_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    client_ip = db.Column(db.String(45), nullable=False)


with app.app_context():
    db.create_all()

@app.route('/hello')
def hello():
    client_ip = request.remote_addr
    current_time = datetime.utcnow()

    new_visit = Visit(
        visit_time=current_time,
        client_ip=client_ip
    )

    db.session.add(new_visit)
    db.session.commit()

    return 'Hello', 200