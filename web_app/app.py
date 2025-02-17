# ./web_app/app.py
from config import SECRET_KEY
from scripts.build_calendar import CalendarBuild
from scripts.build_todo import TodoBuild
from scripts.build_job_applications import JobApplicationBuild
from scripts.build_habits import HabitBuild
from flask import Flask, render_template, url_for, redirect, session, request
from datetime import datetime

app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route('/home', methods=['GET'])
def home():
    current_time = datetime.now()
    if 'month' not in session or 'year' not in session:
        session['month'] = current_time.month
        session['year'] = current_time.year

    if 'month_display' not in session:
        session['month_display'] = True

    if 'select_date' not in session:
        session['select_date'] = f"{current_time.day}/{current_time.month}/{current_time.year}"

    month = session['month']
    year = session['year']
    date = session['select_date']

    current_day = current_time.day
    current_month = current_time.month
    current_year = current_time.year

    habits_for_day = HabitBuild.get_habits_for_date(date)

    calendar = CalendarBuild(month, year)
    month_name = calendar.get_month_name()
    month_layout = calendar.get_layout_month()
    year_layout = calendar.get_layout_year()
    num_of_weeks = len(month_layout[0])

    todo_list = TodoBuild.todo_list
    todo_complete = TodoBuild.todo_complete
    job_list = JobApplicationBuild.job_list

    if 'collapse_todo' not in session:
        session['collapse_todo'] = False

    if 'collapse_todo_complete' not in session:
        session['collapse_todo_complete'] = False

    if 'edit_task' not in session:
        session['edit_task'] = False

    collapse_todo_list = session['collapse_todo']
    collapse_complete = session['collapse_todo_complete']
    task_edit = session['edit_task']

    if 'edit_job_status' not in session:
        session['edit_job_status'] = False

    if 'collapse_job_applications' not in session:
        session['collapse_job_applications'] = False

    status_edit = session['edit_job_status']
    collapse_job = session['collapse_job_applications']

    return render_template(
        'index.html',
        month_name=month_name,
        month_num=month,
        year=year,
        current_day=current_day,
        current_month=current_month,
        current_year=current_year,
        month_layout=month_layout,
        num_of_weeks=num_of_weeks,
        year_layout=year_layout,
        todo_list=todo_list,
        todo_complete=todo_complete,
        collapse_todo=collapse_todo_list,
        collapse_complete=collapse_complete,
        edit_task=task_edit,
        job_list=job_list,
        edit_status=status_edit,
        collapse_job=collapse_job,
        habits_for_day=habits_for_day
    )


@app.route('/job_applications')
def job_applications():
    job_list = JobApplicationBuild.job_list

    if 'collapse_job_applications' not in session:
        session['collapse_job_applications'] = False

    if 'collapse_job_applications' not in session:
        session['collapse_job_applications'] = False

    status_edit = session['edit_job_status']
    collapse_job = session['collapse_job_applications']

    return render_template(
        'job_applications.html',
        job_list=job_list,
        edit_status=status_edit,
        collapse_job=collapse_job
    )


@app.route('/todo_and_habits')
def todo_and_habits():
    current_time = datetime.now()
    if 'month' not in session or 'year' not in session:
        session['month'] = current_time.month
        session['year'] = current_time.year

    if 'select_date' not in session:
        session['select_date'] = f"{current_time.day}/{current_time.month}/{current_time.year}"

    date = session['select_date']

    todo_list = TodoBuild.todo_list
    todo_complete = TodoBuild.todo_complete
    habits_for_day = HabitBuild.get_habits_for_date(date)

    if 'collapse_todo' not in session:
        session['collapse_todo'] = False

    if 'collapse_todo_complete' not in session:
        session['collapse_todo_complete'] = False

    if 'edit_task' not in session:
        session['edit_task'] = False

    collapse_todo_list = session['collapse_todo']
    collapse_complete = session['collapse_todo_complete']
    task_edit = session['edit_task']

    return render_template(
        'todo_and_habits.html',
        todo_list=todo_list,
        todo_complete=todo_complete,
        collapse_todo=collapse_todo_list,
        collapse_complete=collapse_complete,
        edit_task=task_edit,
        habits_for_day=habits_for_day
    )


@app.route('/prev_cal', methods=['POST'])
def prev_cal():
    month = session['month']
    year = session['year']

    if session['month_display']:
        month -= 1
        if month < 1:
            month = 12
            year -= 1
    else:
        year -= 1

    session['month'] = month
    session['year'] = year

    return redirect(url_for('home'))


@app.route('/next_cal', methods=['POST'])
def next_cal():
    month = session['month']
    year = session['year']

    if session['month_display']:
        month += 1
        if month > 12:
            month = 1
            year += 1
    else:
        year += 1

    session['month'] = month
    session['year'] = year

    return redirect(url_for('home'))


@app.route('/year_display', methods=['POST'])
def year_display():
    session['month_display'] = False
    return redirect(url_for('home'))


@app.route('/month_display', methods=['POST'])
def month_display():
    session['month_display'] = True
    return redirect(url_for('home'))


@app.route('/select_date', methods=['POST'])
def select_date():
    date = request.form.get('select_date', '')
    session['select_date'] = date
    return redirect(url_for('home'))


@app.route('/new_task', methods=['POST'])
def new_task():
    task = request.form.get('task', '')
    TodoBuild(task)
    return redirect(request.referrer or url_for('home'))


@app.route('/delete_task', methods=['POST'])
def delete_task():
    task = request.form.get('task', '')
    TodoBuild.delete_task(task)
    return redirect(request.referrer or url_for('home'))


@app.route('/complete_task', methods=['POST'])
def complete_task():
    task = request.form.get('task', '')
    TodoBuild.complete_task(task)
    return redirect(request.referrer or url_for('home'))


@app.route('/delete_complete_task', methods=['POST'])
def delete_complete_task():
    task = request.form.get('task', '')
    TodoBuild.delete_task_complete(task)
    return redirect(request.referrer or url_for('home'))


@app.route('/new_habit', methods=['POST'])
def new_habit():
    habit = request.form.get('habit', '')
    frequency = request.form.get('frequency', '')
    HabitBuild.add_habit(session['select_date'], habit, frequency)
    return redirect(request.referrer or url_for('home'))


@app.route('/delete_habit', methods=['POST'])
def delete_habit():
    habit_id = request.form.get('habit', '')
    HabitBuild.delete_habit(habit_id)
    return redirect(request.referrer or url_for('home'))


@app.route('/complete_habit', methods=['POST'])
def complete_habit():
    habit_id = request.form.get('habit', '')
    date = request.form.get('date', session.get('select_date', ''))
    HabitBuild.complete_habit_for_date(habit_id, date)
    return redirect(request.referrer or url_for('home'))


@app.route('/collapse_todo', methods=['POST'])
def collapse_todo():
    if session['collapse_todo']:
        session['collapse_todo'] = False
    else:
        session['collapse_todo'] = True
    return redirect(request.referrer or url_for('home'))


@app.route('/collapse_todo_complete', methods=['POST'])
def collapse_todo_complete():
    if session['collapse_todo_complete']:
        session['collapse_todo_complete'] = False
    else:
        session['collapse_todo_complete'] = True
    return redirect(request.referrer or url_for('home'))


@app.route('/edit_task', methods=['POST'])
def edit_task():
    if session['edit_task']:
        session['edit_task'] = False
    else:
        session['edit_task'] = True

    task_id = request.form.get('task_id', '')
    new_value = request.form.get('new_task', '')
    if task_id and new_value:
        TodoBuild.edit_task(task_id, new_value)
    return redirect(request.referrer or url_for('home'))


@app.route('/new_job', methods=['POST'])
def new_job():
    company = request.form.get('company', '')
    role = request.form.get('role', '')
    link = request.form.get('link', '')
    location = request.form.get('location', '')
    date = request.form.get('date', '')
    status = 'No Answer'
    JobApplicationBuild(status, company, role, link, location, date)
    return redirect(request.referrer or url_for('home'))


@app.route('/add_status', methods=['POST'])
def add_status():
    session['edit_job_status'] = False
    job_id = request.form.get('job_id', '')
    status = request.form.get('status', '')
    JobApplicationBuild.add_status(job_id, status)
    return redirect(request.referrer or url_for('home'))


@app.route('/edit_job_status', methods=['POST'])
def edit_job_status():
    session['edit_job_status'] = True

    job_id = request.form.get('job_id', '')
    new_status = request.form.get('new_status', '')
    if job_id and new_status:
        JobApplicationBuild.edit_status(job_id, new_status)
    return redirect(request.referrer or url_for('home'))


@app.route('/delete_job', methods=['POST'])
def delete_job():
    job_id = request.form.get('job_id', '')
    JobApplicationBuild.delete_job(job_id)
    return redirect(request.referrer or url_for('home'))


@app.route('/collapse_job_applications', methods=['POST'])
def collapse_job_applications():
    if session['collapse_job_applications']:
        session['collapse_job_applications'] = False
    else:
        session['collapse_job_applications'] = True
    return redirect(request.referrer or url_for('home'))


if __name__ == '__main__':
    app.run(port=8000, debug=False)
