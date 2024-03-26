from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set your secret key for session

# Database initialization

def init_db():
    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()

    # Create employee table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employee (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            salary REAL NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Initialize the databashne
init_db()
                           
# Create
@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        salary = request.form['salary']

        conn = sqlite3.connect('employee.db')
        cursor = conn.cursor()

        # Insert data into the employee table
        cursor.execute('INSERT INTO employee (name, position, salary) VALUES (?, ?, ?)', (name, position, salary))

        conn.commit()
        conn.close()

        flash('Employee created successfully', 'success')  # Add a flash message

        return redirect(url_for('get_employees'))

    return render_template('add_employee.html')

# Read
@app.route('/')
def get_employees():
    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()

    # Fetch all employees from the employee table
    cursor.execute('SELECT * FROM employee')
    employees = cursor.fetchall()

    conn.close()

    return render_template('employees.html', employees=employees)

# Update
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        salary = request.form['salary']

        # Update data in the employee table
        cursor.execute('UPDATE employee SET name=?, position=?, salary=? WHERE id=?', (name, position, salary, id))

        conn.commit()
        conn.close()

        flash('Employee updated successfully', 'success')  # Add a flash message

        return redirect(url_for('get_employees'))
    else:
        # Fetch the employee data by id
        cursor.execute('SELECT * FROM employee WHERE id=?', (id,))
        employee = cursor.fetchone()

        conn.close()

        return render_template('edit_employee.html', employee=employee)

# Delete
@app.route('/delete/<int:id>')
def delete_employee(id):
    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()

    # Delete the employee by id
    cursor.execute('DELETE FROM employee WHERE id=?', (id,))

    # Reset the ID sequence to start from the beginning
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="employee"')
    cursor.execute('INSERT INTO sqlite_sequence (name, seq) VALUES ("employee", 0)')

    conn.commit()
    conn.close()

    flash('Employee deleted successfully', 'success')  # Add a flash message

    return redirect(url_for('get_employees'))

if __name__ == '__main__':
    app.run(debug=True)
