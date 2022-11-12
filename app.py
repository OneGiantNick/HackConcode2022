from flask import Flask, render_template, redirect, request, url_for, make_response
import functions

app = Flask(__name__, template_folder="templates", static_folder="static")
app.debug = True


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        result = functions.login(
            request.form.get("exampleInputUsername1"),
            request.form.get("exampleInputPassword1"),
        )
        if result == "error":
            return render_template("login.html", incorrectDetails=True)

        resp = make_response(redirect(url_for("dashboard")))
        resp.set_cookie("session_address", result)
        if functions.getUser(request.form.get("exampleInputUsername1"))[6] == True:
            return redirect(url_for("welcome"))
        return resp

    return render_template("login.html")


@app.route("/logout")
def logout():
    session = request.cookies.get("session_address")
    functions.logout(session)
    resp = make_response(redirect(url_for("login")))
    resp.set_cookie("session_address", "", expires=0)
    return resp


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        if request.form.get("signUpPassword1") != request.form.get("signUpPassword2"):
            return render_template("signup.html", noPasswordMatch=True)

        result = functions.createUser(
            request.form.get("signUpUsername1"), request.form.get("signUpPassword1")
        )
        if result == "error":
            return render_template("signup.html", usernameExists=True)

        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    if request.method == "POST":
        return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    session = request.cookies.get("session_address")
    if session == None:
        return redirect(url_for("login"))

    return render_template("dashboard.html")


@app.route("/appointments")
def appointments():
    session = request.cookies.get("session_address")
    if session == None:
        return redirect(url_for("login"))

    return render_template("appointment.html")


@app.route("/health")
def health():
    return render_template("health.html")


if __name__ == "__main__":
    app.run()
