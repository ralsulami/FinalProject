from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime
import sqlite3

db = sqlite3.connect('sqlite.db', check_same_thread=False)
db.row_factory = sqlite3.Row
cursor = db.cursor()

app = Flask(__name__)

@app.route('/')
def index():
    # Get the list of appartments with is_available flag to indicate whether
    # it is available for rent or not
    cursor.execute("""
        SELECT a.*,
               CASE
                   WHEN EXISTS (SELECT 1 FROM rent_history WHERE appartment_id = a.id AND ? BETWEEN from_date AND to_date) THEN 0
                   ELSE 1
               END AS is_available
        FROM appartments a
    """, (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),))
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
    cursor.execute("INSERT INTO appartments (address, floor_level, number_of_bedrooms, number_of_bathrooms, does_have_garage) VALUES (?, ?, ?, ?, ?)", (data['address'], data['floor_level'], data['number_of_bedrooms'], data['number_of_bathrooms'], does_have_garage))
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

    # Fetch rent history
    cursor.execute("SELECT * FROM rent_history WHERE appartment_id = ? ORDER BY id DESC", (id,))
    rent_history = cursor.fetchall()

    return render_template('appartment-detail.html', title="Appartment Detail", appartment=appartment, owner=owner, rent_history=rent_history)

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

@app.route('/appartments/<int:appartment_id>/put-on-rent')
def toggle_rent_status(appartment_id):
    return render_template('put-on-rent.html', title="Put on rent", appartment_id=appartment_id)

@app.route('/appartments/<int:appartment_id>/put-on-rent-submit', methods=['POST'])
def put_on_rent(appartment_id):
    data = request.form
    to_date = datetime.strptime(data.get('to_date', '9999-12-31'), '%Y-%m-%d')
    cursor.execute("INSERT INTO rent_history (from_date, to_date, price, appartment_id) VALUES (?, ?, ?, ?)", (datetime.now().strftime('%Y-%m-%d'), to_date.strftime('%Y-%m-%d'), data['price'], appartment_id))
    db.commit()
    return redirect(url_for('index'))

@app.route('/appartments/<int:appartment_id>/make-available-for-rent', methods=['POST'])
def make_available_for_rent(appartment_id):
    cursor.execute("SELECT * FROM rent_history WHERE appartment_id = ? AND ? BETWEEN from_date AND to_date", (appartment_id, datetime.now().strftime('%Y-%m-%d')))
    rent_history_latest = cursor.fetchone()

    cursor.execute("UPDATE rent_history SET to_date = ? WHERE id = ?", (datetime.now().strftime('%Y-%m-%d'), rent_history_latest['id']))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=27095, host='0.0.0.0')

