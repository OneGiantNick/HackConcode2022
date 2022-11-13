from flask import Flask, render_template, redirect, request, url_for, make_response
import functions
from datetime import datetime

app = Flask(__name__, template_folder="templates", static_folder="static")
app.debug = True

cookiejar = {}


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
        cookiejar["session_address"] = result

        resp.set_cookie("session_address", result, domain="127.0.0.1")
        if functions.getUser(request.form.get("exampleInputUsername1"))[6] == True:
            return redirect(url_for("welcome"))
        return resp

    return render_template("login.html")


@app.route("/logout")
def logout():
    session = cookiejar["session_address"]
    try:
        functions.logout(session)
    except:
        pass
    cookiejar["session_address"] = None
    return redirect(url_for("login"))


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
    session = cookiejar["session_address"]
    username = str(functions.getUserFromSession(session))
    if functions.getUser(username)[6] == False:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        functions.updateNewcomer(
            username,
            request.form.get("sex"),
            request.form.get("height"),
            request.form.get("weight"),
        )
        return redirect(url_for("dashboard"))
    return render_template("welcome.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    session = cookiejar["session_address"]
    user = str(functions.getUserFromSession(session))
    if session == None:
        return redirect(url_for("login"))

    return render_template("dashboard.html", username=user)


@app.route("/appointments", methods=["GET", "POST"])
def appointments():
    session = cookiejar["session_address"]
    if session == None:
        return redirect(url_for("login"))
    username = functions.getUserFromSession(session)
    if request.method == "POST":
        dt = datetime.strptime(request.form.get("datetime"), "%Y-%m-%dT%H:%M")
        dt = int(round(dt.timestamp()))
        functions.createAppointment(
            username,
            request.form.get("location"),
            dt,
            request.form.get("symptoms"),
        )
        return redirect(url_for("appointments"))

    appointment_list = functions.getUserAppointments(username)
    if len(appointment_list) != 0:
        appointment_list_info = []
        print(len(appointment_list))
        
        for i in range(len(appointment_list)):
            appointtime = functions.getAppointmentDate(appointment_list[i])
            timestring = datetime.fromtimestamp(appointtime)
            print(appointment_list[i])
            info = (
                username,
                functions.getLocation(appointment_list[i]),
                timestring,
                functions.getSymptoms(appointment_list[i]),
                functions.getCompleted(appointment_list[i]),
                functions.getPrescriptions(appointment_list[i]),
            )
            appointment_list_info.append(info)
        return render_template("appointment.html", data=appointment_list_info)
    message = "No appointments... Make one now!"
    return render_template("appointment.html", message=message)


@app.route("/health")
def health():
    session = cookiejar["session_address"]
    if session == None:
        return redirect(url_for("login"))
    username = functions.getUserFromSession(session)
    data = functions.getUser(username)

    _sex = data[2]
    _height = data[3]
    _weight = data[4]
    _bmi = round(_weight / (_height / 100) ** 2, 2)
    return render_template(
        "health.html", sex=_sex, height=_height, weight=_weight, bmi=_bmi
    )


@app.route("/setup", methods=["GET", "POST"])
def setup():
    session = cookiejar["session_address"]
    username = str(functions.getUserFromSession(session))
    if request.method == "POST":
        functions.updateNewcomer(
            username,
            request.form.get("sex"),
            request.form.get("height"),
            request.form.get("weight"),
        )
        return redirect(url_for("health"))
    return render_template("setup.html")


if __name__ == "__main__":
    app.run()
