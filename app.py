from flask import Flask, render_template, redirect, request, url_for
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

        return redirect(url_for("dashboard", session=result))

    return render_template("login.html")


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


@app.route("/dashboard")
def dashboard():
    print(request.args.get("session"))
    return render_template("dashboard.html")


@app.route("/appointments")
def appointments():
    return render_template("appointment.html")


if __name__ == "__main__":
    app.run()
