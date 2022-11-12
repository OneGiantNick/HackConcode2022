from flask import Flask, render_template, redirect, request, url_for
import functions

app = Flask(__name__, template_folder="templates", static_folder="static")
app.debug = True


@app.route("/", methods=["GET", "POST"])
def login():
    context = {"title": "HealthUp"}
    if request.method == "POST":
        result = functions.login(
            request.form.get("exampleInputUsername1"),
            request.form.get("exampleInputPassword1"),
        )
        if result == False:
            context["incorrectDetails"] = True
            return redirect(url_for(login, context=context))

        return redirect(url_for(dashboard(result)))

    return render_template("login.html", context=context)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    context = {"title": "Sign up"}
    if request.method == "POST":
        username = request.form.get("signUpUsername1")
        password = request.form.get("signUpPassword1")
        print(functions.createUser(username, password)
        return redirect(url_for(login))
    return render_template("signup.html")


if __name__ == "__main__":
    app.run()


@app.route("/dashboard")
def dashboard(session):
    return render_template("dashboard.html")
