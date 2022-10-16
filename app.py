from flask import Flask, render_template, url_for
from flask import request, redirect
import sqlite3

app = Flask(__name__)


def get_todos():
    with sqlite3.connect('db/app.db') as conn:
        cursor = conn.cursor()

        cursor.execute("select * from todo")
        result = cursor.fetchall()

        todos = []

        for row in result:
            todos.append({"id": row[0],
                          "date": row[1],
                          "title": row[2],
                          "completed": row[3]}),
    conn.close()
    return todos


@app.route("/")
def index():
    todos = get_todos()
    return render_template('index.html',
                           todos=todos
                           )


@app.route("/add_todo_item", methods=["GET", "POST"])
def add_todo_item():
    if request.method == "POST":
        item = request.form['todo-item']

        item = item.strip().lower()

        with sqlite3.connect('db/app.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"insert into todo (title, completed) values ('{item}', 'false') ")
        conn.close()
        return redirect(url_for('index'))


@app.route("/complete_todo", methods=["GET", "POST"])
def complete_todo():
    if request.method == "POST":
        item = request.form['el']

        with sqlite3.connect('db/app.db') as conn:
            cursor = conn.cursor()
            query = f"update todo set completed = 'true' where title == '{item}' "
            cursor.execute(query)
        conn.close()
        return redirect(url_for('index'))


@app.route("/delete_todo", methods=["GET", "POST"])
def delete_todo():
    if request.method == "POST":
        item = request.form['el']

        with sqlite3.connect('db/app.db') as conn:
            cursor = conn.cursor()
            query = f"delete from todo where title == '{item}' "
            cursor.execute(query)
        conn.close()
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
