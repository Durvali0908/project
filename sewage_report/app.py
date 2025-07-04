from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # needed for session management

# ---------------- Home Dashboard ------------------
@app.route('/')
def user_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('user_signIn'))  # redirect to login if not logged in

    conn = sqlite3.connect('garbage.db')
    c = conn.cursor()
    c.execute('SELECT * FROM complaints ORDER BY dateTime DESC')
    complaints = c.fetchall()
    conn.close()
    return render_template('dashboard.html', complaints=complaints)
#signUp
@app.route('/user_signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birth_date']
        phone = request.form['phone']
        address = request.form['address']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('garbage.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (name, birth_date, phone, address, email, password) VALUES (?, ?, ?, ?, ?, ?)",
                  (name, birth_date, phone, address, email, password))
        conn.commit()
        conn.close()
        return redirect(url_for('user_signIn'))  # After registration go to login

    return render_template('user_signup.html')  # Make sure signup.html exists

#signin
@app.route('/user_signIn', methods=['GET', 'POST'])
def user_signIn():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('garbage.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect(url_for('user_dashboard'))
        else:
            return "❌ Invalid credentials"
    
    return render_template('user_signIn.html')  # Make sure signin.html exists


# ---------------- Complaint Submission -------------
@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():
    location = request.form['location']
    waste_type = request.form['waste_type']
    description = request.form['description']
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    dateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    photo_fileName = ''

    photo = request.files.get('photo')
    if photo and photo.filename != '':
        photo_fileName = photo.filename
        photo.save(os.path.join('static/uploads', photo_fileName))

    conn = sqlite3.connect('garbage.db')
    c = conn.cursor()
    c.execute('''INSERT INTO complaints 
                (reported_by, location, waste_type, description, photo_fileName, dateTime, latitude, longitude)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              ('Anonymous', location, waste_type, description, photo_fileName, dateTime, latitude, longitude))
    conn.commit()
    conn.close()
    return redirect(url_for('user_dashboard'))

# -------------- GET Location API (used by JS) ----------
@app.route('/get_location/<int:case_id>')
def get_location(case_id):
    conn = sqlite3.connect('garbage.db')
    c = conn.cursor()
    c.execute("SELECT location FROM complaints WHERE id = ?", (case_id,))
    result = c.fetchone()
    conn.close()

    if result:
        return jsonify(success=True, location=result[0])
    else:
        return jsonify(success=False)

# -------------- Transfer Case (GET + POST) ---------------
@app.route('/transfer_case', methods=['GET', 'POST'])
def transfer_case():
    if request.method == 'POST':
        case_id = request.form['case_id']
        location = request.form['location']
        authority_email = request.form['authority_email']
        transferred_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect('garbage.db')
        c = conn.cursor()
        c.execute('''INSERT INTO transfers (case_id, location, authority_email, transferred_at)
                     VALUES (?, ?, ?, ?)''', (case_id, location, authority_email, transferred_at))
        conn.commit()
        conn.close()

        return "✅ Case transfer saved (email not sent but logged)."
    
    return render_template('transfer_case.html')
# signOut
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user_signIn'))

# ---------------------- RUN APP -------------------------
if __name__ == '__main__':
    app.run(debug=True)