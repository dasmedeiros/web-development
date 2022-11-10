import datetime
import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__, static_folder="static")
    client = MongoClient(os.environ.get("DATABASE_URL"))
    app.db = client.portfolio

    @app.route("/")
    def home():
        return render_template("home.html")
    
    @app.route("/about/")
    def about():
        return render_template("about.html")

    @app.route("/feedback/", methods=["GET", "POST"])
    def feedback():
        if request.method == "POST":
            review_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one({"content": review_content, "date": formatted_date})
        
        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]

        return render_template("feedback.html", entries=entries_with_date)
    
    @app.route("/contact/", methods=["GET", "POST"])
    def contact():
        contact_name = ""
        success = False
        if request.method == "POST":
            contact_name = request.form.get("name")
            contact_email = request.form.get("email")
            contact_tel = request.form.get("tel")
            contact_message = request.form.get("message")
            app.db.messages.insert_one({"name": contact_name, "email": contact_email, "tel": contact_tel, "message": contact_message})
            success = True

        return render_template("contact.html", contact_name=contact_name, success=success)    

    return app