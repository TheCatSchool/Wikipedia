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

def get_db_connection(): #defines the database
    return mysql.connector.connect(
        host="10.200.14.14",
        user="Loji",
        password="TheLongMarch",
        database="Wikipedia"
    )

@app.route('/') #for start up, redirects to home so i dont have to manually write /home
def some():
    return redirect('/home')

@app.route('/home')
def home():
    return render_template("home.html") #renders home template, which includes links for other pages

@app.route('/registrer', methods=["GET", "POST"]) #register, fetches get and post functions
def register():
    if request.method == "POST": #when posting
        brukernavn = request.form['user'] #fetches information from the html template
        epost = request.form['email'] #same as above but with email
        passord = generate_password_hash(request.form['password']) #grabs the set password before hashing it.
        #hashing the password makes it so that the password in databasee =/ the password

        conn = get_db_connection() #fetch database
        cursor = conn.cursor() #define database cmds
        cursor.execute("INSERT INTO users (Username, Email, Password_hashed) VALUES (%s, %s, %s)",  
                       (brukernavn, epost, passord)) #insert into the database with the gathered information
        conn.commit()
        #commit changes so its saved
        cursor.close()
        conn.close()
        #closes the database functions
        flash("Bruker registrert!", "success")
        #register check
        return redirect(url_for("login"))
        #redirect to login
    return render_template("reg.html") #render the html template
@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("role") == "user": ##checking if you are allready logged in or not
        return redirect('/profile')
    elif session.get("role") == "admin":
        return redirect('/admin')
    if request.method == "POST":
        brukernavn = request.form['brukernavn']
        passord = request.form['passord']
        #fetches username and password for log in
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE Username=%s", (brukernavn,)) #fetches user with matching username
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['Password_hashed'], passord): #if the username's password hashed = the inserted password hashed. then continue
            session['user'] = user['Username'] #set sessions
            session['role'] = user['Role']
            session['id'] = user['ID']
            if user['Role'] == 'admin': #if user = admin redirect to admin else redirect to profile
                return redirect('/admin')
            else:
                return redirect('/profile')
        else:
            return render_template("log.html", feil_melding="Ugyldig brukernavn eller passord") #if non matching, re render
        #ps: add max chances for safety.

    return render_template("log.html")
@app.route("/admin", methods=["GET", "POST"]) #admin b
def admin_dashboard():
    if session.get("role") == "admin": #makes it so you need to be admin to be here.
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users;") #fetches all users
        uses = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template("admin.html", brukernavn=session['user'], users=uses)  #displays the information
    return redirect(url_for("login"))

# User dashboard
@app.route("/profile", methods=["GET", "POST"])
def user_dashboard():
    if session.get("role") == "user": #need to be logged in to view
        return render_template("profile.html", brukernavn=session['user'])
    elif session.get("role") == "admin":
        return redirect('/admin')
    return redirect(url_for("login"))

@app.route("/logout") #ends all sessions
def logout():
    session.pop("user", None)
    session.pop("role", None) #ends all sessions
    session.pop("id", None)
    return redirect(url_for("login"))
@app.route("/create", methods=["GET", "POST"]) 
def create_page():
    if not session.get("user"): #checks if you are logged in if not redirects
        return redirect(url_for("login"))

    if request.method == "POST": 
        title = request.form['title']
        content = request.form['content'] #fetches information like title, content and creator id
        creatorid = session.get("id")

        slug = slugify(title) #turns the title into a slug used for urls

        conn = get_db_connection()
        cursor = conn.cursor() #fetches database

        cursor.execute(
            "INSERT INTO pages (Title, Slug, Content, CreatorID) VALUES (%s, %s, %s, %s)",
            (title, slug, content, creatorid) #inserts info into database(creating the site)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("view_page", slug=slug)) #redirects to the page, the slug is url

    return render_template("create.html")
@app.route("/wiki/<slug>")
def view_page(slug):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM pages WHERE Slug=%s", (slug,)) #fetches the information
    page = cursor.fetchone()

    cursor.close()
    conn.close()

    if not page:
        flash("Page does not exist. Create it!")
        return redirect(url_for("create_page")) #if page doesnt exist redirect to create

    return render_template("view.html", page=page)
@app.route("/edit/<slug>", methods=["GET", "POST"])
def edit_page(slug):
    if not session.get("user"):
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM pages WHERE Slug=%s", (slug,)) #feches page info
    page = cursor.fetchone()

    if request.method == "POST":
        new_content = request.form['content'] #fetches edits

        cursor.execute(
            "UPDATE pages SET Content=%s WHERE Slug=%s", #updates page
            (new_content, slug)
        )
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("view_page", slug=slug)) #redirects to view page, therefore refreshing the page

    cursor.close()
    conn.close()

    return render_template("edit.html", page=page)
@app.route("/pages", methods=["GET", "POST"])
def pages():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT Title FROM pages") #fetchas all pages
    pages = cursor.fetchall()
    
    return render_template("pages.html", pages=pages) #renders template where they are showed

    
@app.route("/wiki/") #this is only used for the search function
def wiki_redirect(): 
    title = request.args.get("title") #uses title which it has been given before
    return redirect(f"/wiki/{title}") #redirects to wiki page with slug. 