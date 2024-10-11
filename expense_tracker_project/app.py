from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Home Page (Add Expense Form)
@app.route('/')
def index():
    return render_template('index.html')

# Add Expense to the database
@app.route('/add', methods=['POST'])
def add_expense():
    try:
        # Get form data
        amount = float(request.form['amount'])
        category = request.form['category']
        description = request.form['description']
        date = request.form['date']

        # Ensure required fields are provided
        if not amount or not category or not date:
            return "Missing required fields!", 400

        # Insert data into the database
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute("INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
                  (amount, category, description, date))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error: {e}")  # Log error in the console
        return "An error occurred while adding the expense.", 500

# Show All Expenses
@app.route('/expenses')
def show_expenses():
    try:
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute("SELECT * FROM expenses")
        expenses = c.fetchall()
        conn.close()
        return render_template('expenses.html', expenses=expenses)
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while retrieving the expenses.", 500

if __name__ == '__main__':
    init_db()  # This should initialize the database and create the 'expenses' table
    app.run(debug=True)
