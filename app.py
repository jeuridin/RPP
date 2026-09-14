from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = 'secret_key'

db = SQLAlchemy()

## СДЕЛАТЬ ПУНКТ 3 !!!!!!!!!!!

class Visit(Model):
    __tablename__ = 'visits'
    id = Column(Integer, primary_key = True)
    visit_time = Column(DateTime, default=DateTime.utcnow, nullable=False)
    client_ip = Column(String(45), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/hello')
def hello():
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    new_visit = Visit(client_ip = client_ip)
    db.session.add(new_visit)
    db.session.commit()

    return 'hello', 200