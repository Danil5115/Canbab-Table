from flask import Flask, render_template, request, redirect, url_for
from models import db, Sprint, Task, Person
from forms import TaskForm, SprintForm, PersonForm
import os
from datetime import datetime
from utils import (
    calculate_burndown,
    calculate_velocity,
    calculate_lead_time,
    calculate_cycle_time,
    calculate_time_in_process,
    plot_burndown,
    plot_velocity,
    plot_lead_time_histogram,
    plot_lead_time_box,
    plot_cycle_time_box,
    plot_cycle_time_scatter,
    plot_time_in_process_stacked,
    plot_cumulative_flow
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kanban.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['WTF_CSRF_ENABLED'] = False  # Отключение CSRF
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    selected_sprint = request.args.get('sprint_id', type=int)
    if selected_sprint:
        tasks = Task.query.filter_by(sprint_id=selected_sprint).all()
        sprint = Sprint.query.get(selected_sprint)
        sprint_name = sprint.name
        burndown_data = calculate_burndown(tasks)
        lead_time_data = calculate_lead_time(tasks)
        cycle_time_data = calculate_cycle_time(tasks)
        time_in_process_data = calculate_time_in_process(tasks)
        plot_burndown(burndown_data)
        plot_lead_time_histogram(lead_time_data)
        plot_lead_time_box(lead_time_data)
        plot_cycle_time_box(cycle_time_data)
        plot_cycle_time_scatter(cycle_time_data)
        plot_time_in_process_stacked(time_in_process_data)
        plot_cumulative_flow(tasks)
    else:
        tasks = Task.query.all()
        sprint_name = "All Sprints"
        burndown_data = calculate_burndown(tasks)
        velocity_data = calculate_velocity(tasks)
        lead_time_data = calculate_lead_time(tasks)
        cycle_time_data = calculate_cycle_time(tasks)
        time_in_process_data = calculate_time_in_process(tasks)
        plot_burndown(burndown_data)
        plot_velocity(velocity_data)
        plot_lead_time_histogram(lead_time_data)
        plot_lead_time_box(lead_time_data)
        plot_cycle_time_box(cycle_time_data)
        plot_cycle_time_scatter(cycle_time_data)
        plot_time_in_process_stacked(time_in_process_data)
        plot_cumulative_flow(tasks)

    return render_template('index.html', tasks=tasks, sprints=Sprint.query.all(), selected_sprint=selected_sprint, sprint_name=sprint_name)

@app.route('/sprints', methods=['GET', 'POST'])
def view_sprints():
    form = SprintForm()
    if form.validate_on_submit():
        new_sprint = Sprint(name=form.name.data, start_date=form.start_date.data, end_date=form.end_date.data)
        db.session.add(new_sprint)
        db.session.commit()
        return redirect(url_for('view_sprints'))
    return render_template('sprints.html', form=form, sprints=Sprint.query.all())

@app.route('/sprint/<int:sprint_id>')
def sprint_detail(sprint_id):
    sprint = Sprint.query.get_or_404(sprint_id)
    tasks = Task.query.filter_by(sprint_id=sprint_id).all()
    return render_template('sprint_detail.html', sprint=sprint, tasks=tasks)

@app.route('/tasks', methods=['GET', 'POST'])
def view_tasks():
    form = TaskForm()
    form.sprint_id.choices = [(s.id, s.name) for s in Sprint.query.all()]
    form.person_id.choices = [(p.id, p.name) for p in Person.query.all()]
    if form.validate_on_submit():
        new_task = Task(
            title=form.title.data,
            description=form.description.data,
            status='To Do',  # Статус автоматически задается как 'To Do'
            sprint_id=form.sprint_id.data,
            person_id=form.person_id.data
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('view_tasks'))
    tasks = Task.query.all()
    return render_template('tasks.html', form=form, tasks=tasks, sprints=Sprint.query.all(), persons=Person.query.all())

@app.route('/create_person', methods=['GET', 'POST'])
def create_person():
    form = PersonForm()
    if form.validate_on_submit():
        new_person = Person(name=form.name.data, position=form.position.data)
        db.session.add(new_person)
        db.session.commit()
        return redirect(url_for('create_person'))
    persons = Person.query.all()
    return render_template('create_person.html', form=form, persons=persons)

@app.route('/add_sprint', methods=['POST'])
def add_sprint():
    form = SprintForm()
    if form.validate_on_submit():
        new_sprint = Sprint(name=form.name.data, start_date=form.start_date.data, end_date=form.end_date.data)
        db.session.add(new_sprint)
        db.session.commit()
    return redirect(url_for('view_sprints'))

@app.route('/add_task', methods=['POST'])
def add_task():
    form = TaskForm()
    form.sprint_id.choices = [(s.id, s.name) for s in Sprint.query.all()]
    form.person_id.choices = [(p.id, p.name) for p in Person.query.all()]
    if form.validate_on_submit():
        new_task = Task(
            title=form.title.data,
            description=form.description.data,
            status='To Do',  # Статус автоматически задается как 'To Do'
            sprint_id=form.sprint_id.data,
            person_id=form.person_id.data
        )
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('view_tasks'))

@app.route('/add_person', methods=['POST'])
def add_person():
    form = PersonForm()
    if form.validate_on_submit():
        new_person = Person(name=form.name.data, position=form.position.data)
        db.session.add(new_person)
        db.session.commit()
    return redirect(url_for('create_person'))

@app.route('/update/<int:task_id>/<string:new_status>', methods=['POST'])
def update_task(task_id, new_status):
    task = Task.query.get(task_id)
    sprint_id = request.form.get('sprint_id', type=int)
    if new_status == 'In Progress' and task.status != 'In Progress':
        task.in_progress_at = datetime.utcnow()
    if new_status == 'Done' and task.status != 'Done':
        task.done_at = datetime.utcnow()
    task.status = new_status
    db.session.commit()
    if sprint_id:
        return redirect(url_for('index', sprint_id=sprint_id))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
