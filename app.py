from flask import Flask, request, render_template, redirect, url_for
import sqlite3

db = sqlite3.connect('sqlite.db', check_same_thread=False)
db.row_factory = sqlite3.Row
cursor = db.cursor()

app = Flask(__name__)

@app.route('/')
def index():
    cursor.execute("SELECT * FROM appartments")
    appartments = cursor.fetchall()
    return render_template('home.html', title="Appartment Complex Tracker", appartments=appartments)

@app.route('/add')
def add():
    return render_template('add.html', title="Add Appartment")

@app.route('/add-submit', methods=['POST'])
def add_submit():
    data = request.form
    does_have_garage = data.get('does_have_garage', False)
    does_have_garage = True if does_have_garage else False
    cursor.execute("INSERT INTO appartments (address, floor_level, number_of_bedrooms, number_of_bathrooms, does_have_garage, user_id) VALUES (?, ?, ?, ?, ?, 1)", (data['address'], data['floor_level'], data['number_of_bedrooms'], data['number_of_bathrooms'], does_have_garage))
    print(data)
    db.commit()
    return "Appartment added successfully"

@app.route('/appartments/<int:id>/view')
def appartment_detail(id):
    # Fetch appartment data
    cursor.execute("SELECT * FROM appartments WHERE id = ?", (id,))
    appartment = cursor.fetchone()

    # Fetch owner details
    owner_id = appartment['user_id']
    owner = None
    if owner_id:
        cursor.execute("SELECT * FROM user WHERE id = ?", (owner_id,))
        owner = cursor.fetchone()

    return render_template('appartment-detail.html', title="Appartment Detail", appartment=appartment, owner=owner)

@app.route('/appartments/<int:appartment_id>/add-owner')
def add_owner(appartment_id):
    return render_template('add-owner.html', title="Add Owner", appartment_id=appartment_id)

@app.route('/appartments/<int:appartment_id>/add-owner-submit', methods=['POST'])
def add_owner_submit(appartment_id):
    data = request.form
    cursor.execute("INSERT INTO user (name, email, phone) VALUES (?, ?, ?)", (data['name'], data['email'], data['phone']))

    # Add user ID in appartment table
    user_id = cursor.lastrowid
    cursor.execute("UPDATE appartments SET user_id = ? WHERE id = ?", (user_id, appartment_id))

    db.commit()

    # Redirect to appartment detail page
    return redirect(url_for ('appartment_detail', id=appartment_id))


if __name__ == '__main__':
    app.run(debug=True, port=27095, host='0.0.0.0')

