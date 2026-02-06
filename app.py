from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

# Bruker du Mariadb så bytter du ut mysql med mariadb. Mariadb må installeres med (pip install mariadb) Koden finner du på neste linje.
# import mariadb

app = Flask(__name__)
app.secret_key = "this is a key"

def get_db_connection():
    return mysql.connector.connect(
        host="10.200.14.14",
        user="Loji",
        password="TheLongMarch",
        database="Wikipedia"
    )

@app.route('/')
def some():
    return redirect('/home')

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/registrer', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        brukernavn = request.form['user']
        epost = request.form['email']
        passord = generate_password_hash(request.form['password'])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (Username, Email, Password_hashed) VALUES (%s, %s, %s)", 
                       (brukernavn, epost, passord))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Bruker registrert!", "success")
        return redirect(url_for("login"))

    return render_template("reg.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    
    if request.method == "POST":
        brukernavn = request.form['brukernavn']
        passord = request.form['passord']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE Username=%s", (brukernavn,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['Password_hashed'], passord):
            session['user'] = user['Username']
            session['role'] = user['Role']
            session['id'] = user['ID']
            if user['Role'] == 'admin':
                return redirect('/admin')
            else:
                return redirect('/profile')
        else:
            return render_template("log.html", feil_melding="Ugyldig brukernavn eller passord")

    return render_template("log.html")
@app.route("/admin", methods=["GET", "POST"])
def admin_dashboard():
    if session.get("role") == "admin":
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users;")
        uses = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template("admin.html", brukernavn=session['user'], users=uses)
    return redirect(url_for("login"))

# User dashboard
@app.route("/profile", methods=["GET", "POST"])
def user_dashboard():
    if session.get("role") == "user":
        return render_template("profile.html", brukernavn=session['user'])
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))
@app.route("/create", methods=["GET", "POST"])
def create_page():
    if not session.get("user"):
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        creatorid = session.get("id")

        slug = slugify(title)

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO pages (Title, Slug, Content, CreatorID) VALUES (%s, %s, %s, %s)",
            (title, slug, content, creatorid)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("view_page", slug=slug))

    return render_template("create.html")
@app.route("/wiki/<slug>")
def view_page(slug):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM pages WHERE Slug=%s", (slug,))
    page = cursor.fetchone()

    cursor.close()
    conn.close()

    if not page:
        flash("Page does not exist. Create it!")
        return redirect(url_for("create_page"))

    return render_template("view.html", page=page)
@app.route("/edit/<slug>", methods=["GET", "POST"])
def edit_page(slug):
    if not session.get("user"):
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM pages WHERE Slug=%s", (slug,))
    page = cursor.fetchone()

    if request.method == "POST":
        new_content = request.form['content']

        cursor.execute(
            "UPDATE pages SET Content=%s WHERE Slug=%s",
            (new_content, slug)
        )
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("view_page", slug=slug))

    cursor.close()
    conn.close()

    return render_template("edit.html", page=page)
@app.route("/pages", methods=["GET", "POST"])
def pages():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT Title FROM pages")
    pages = cursor.fetchall()
    
    return render_template("pages.html", pages=pages)

    