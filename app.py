from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('todo.db') as conn:    # connect to the database
        cursor = conn.cursor()                  # create a cursor object to execute SQL queries
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS tasks (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       task TEXT NOT NULL,
                       status TEXT NOT NULL DEFAULT 'Pending'
                       )
                       """)
        conn.commit()

@app.route('/')
def index():
    with sqlite3.connect('todo.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
    return render_template("index.html", tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        with sqlite3.connect('todo.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
            conn.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>')
def update_task(task_id):
    with sqlite3.connect('todo.db') as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?", (task_id,))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    with sqlite3.connect('todo.db') as conn:
        cursor = conn.cursor()
        cursor.execute(" DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)