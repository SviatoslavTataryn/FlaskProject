from flask import Flask, render_template, request, redirect, url_for
from models import db, Task

app = Flask(__name__)

# Конфігурація для бази даних
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Ініціалізація бази даних
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    query = request.args.get('search')  # Отримання параметра пошуку
    if query:
        tasks = Task.query.filter(Task.content.like(f"%{query}%")).all()  # Пошук завдань
    else:
        tasks = Task.query.all()  # Виведення всіх завдань
    return render_template('index.html', tasks=tasks, search_query=query)

@app.route('/add', methods=['POST'])
def add_task():
    task_text = request.form.get('task')
    if task_text:
        new_task = Task(content=task_text)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get(task_id)
    if request.method == 'POST':
        new_content = request.form.get('task')
        if new_content:
            task.content = new_content
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', task=task)

if __name__ == '__main__':
    app.run(debug=True)
