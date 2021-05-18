from flask import Flask, redirect, render_template, url_for, request, Response, after_this_request, session, Blueprint, jsonify

app = Flask(__name__)
app.secret_key = "sadSJdsZMxcMC123231"  

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run()