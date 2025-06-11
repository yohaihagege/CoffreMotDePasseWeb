from flask import render_template, redirect, url_for, request, flash
from app import app

@app.route('/')
def accueil():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')
