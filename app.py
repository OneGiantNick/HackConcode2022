from flask import Flask, render_template, url_for

app = Flask(__name__, template_folder='templates', static_folder='static')
app.debug = True

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

if __name__ == "__main__":
    app.run()
