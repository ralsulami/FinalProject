from flask import Flask, request, render_template
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

if __name__ == '__main__':
    app.run(debug=True, port=27095, host='0.0.0.0')

