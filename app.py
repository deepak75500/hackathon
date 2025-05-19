from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from slots import generate_slots

app = Flask(__name__)
app.secret_key = 'your-secret-key'
from datetime import date 
BOOKINGS = {} 

@app.route('/logout')
def logout():
    session.clear()
    return render_template("login.html", error=None)
@app.route("/home", methods=["GET", "POST"]) 
def home():
    return 
@app.route("/", methods=["GET", "POST"])           
def login():
    if request.method == "POST":
        name          = request.form["name"].strip()
        selected_date = request.form["date"]
        is_admin      = "admin" in request.form    

        if name and selected_date:
            session["username"]      = name
            session["selected_date"] = selected_date
            session["is_admin"]      = is_admin

            if selected_date not in BOOKINGS:
                BOOKINGS[selected_date] = generate_slots()

            return redirect(url_for("dashboard"))
        return render_template("login.html",
                               error="Both name and date are required!",
                               today=date.today().isoformat())
    return render_template("login.html", error=None,
                           today=date.today().isoformat())

@app.route('/dashboard')
def dashboard():
    if 'username' not in session or 'selected_date' not in session:
        return redirect(url_for('select_date'))
    selected_date = session['selected_date']
    return render_template(
        'index.html',
        slots=BOOKINGS[selected_date],
        username=session['username'],
        is_admin=session.get('is_admin', False),
        selected_date=selected_date
    )

@app.route("/book", methods=["POST"])
def book_slot():
    date = session.get('selected_date')
    name = session.get('username', 'Anonymous')
    slot = request.form["slot"]
    if BOOKINGS[date].get(slot) is None:
        BOOKINGS[date][slot] = name
        return jsonify({"status": "success", "message": f"Booked {slot}"})
    return jsonify({"status": "fail", "message": "Slot already booked"})

@app.route("/cancel", methods=["POST"])
def cancel_slot():
    date = session.get('selected_date')
    slot = request.form["slot"]
    user = session.get('username')
    is_admin = session.get('is_admin', False)

    if is_admin or BOOKINGS[date].get(slot) == user:
        BOOKINGS[date][slot] = None
        return jsonify({"status": "success", "message": f"Canceled {slot}"})
    return jsonify({"status": "fail", "message": "You are not authorized to cancel this slot"})

if __name__ == "__main__":
    app.run(debug=True)
