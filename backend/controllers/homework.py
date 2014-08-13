from flask import Blueprint
from flask import render_template
from flask import json
from flask import session
from flask import url_for
from flask import redirect
from flask import request
from flask import abort
from flask import Response
from helpers import new_parser
from helpers import edit_parser, multikeysort

from models import Homework, Schedule, Student
from xl_uploader import get_row_values
from helpers import generate_key

homework_view = Blueprint('homework_view', __name__)

########### homework REST controller ###########

@homework_view.route('/homework/',methods=['GET','POST'],defaults={'id':None})
@homework_view.route('/homework/<id>',methods=['GET','PUT','DELETE'])
def homework_controller(id):
	title = request.values.get('title')
	due_date = request.values.get('due_date')
	description = request.values.get('description')
	schedule_id = request.values.get('schedule_id')

	if id:
		homework = Homework.query(Homework.id==id).get()
		if homework:
			if request.method == 'GET':
				if request.values.get('json'):
					return json.dumps(dict(homework=homework.json))
				return render_template('homework_view.html',homework = homework, title = "Homework List")
			elif request.method == 'PUT':
				homework = edit_parser(homework,request)
				homework.put()
				return 'Value Updated', 204
			elif request.method == 'DELETE':
				homework.delete()
				return 'Item deleted', 204
			else:
				return 'Method Not Allowed'
	else:
		if request.method == 'GET':
			homework_list = Homework.query().fetch(1000)
			entries=None
			if homework_list:
				entries = [homework.dto() for homework in homework_list]
			if request.values.get('json'):
				return json.dumps(dict(homework=entries))
			return render_template('homework.html',homework_entries = entries, title = "Homework List")
		elif request.method == 'POST':
			homework = Homework()
			homework = new_parser(homework,request)
			homework.put()
			url = '/homework/'
			if request.values.get('json'):
				url = '/homework/json=true'
			return redirect(url)
		else:
			return abort(405)

@homework_view.route('/homework/add/')
def homework_add_controller():
	#this is the controller to add new model entries
	schedules = Schedule.query().fetch(1000)
	return render_template('homework_add.html', title = "Add New Entry", schedules = schedules)

@homework_view.route('/homework/edit/<id>')
def homework_edit_controller(id):
	#this is the controller to edit model entries
	homework_item = Homework.query(Homework.id==id).get()
	return render_template('homework_edit.html', homework_item = homework_item, title = "Edit Entries")

@homework_view.route('/homework/upload')
def homework_upload_controller():
	return render_template('homework_excel.html')

@homework_view.route('/homework/upload/process', methods=["GET","POST"])
def homework_upload_process_controller():
	file = request.file('file')
	rows = get_row_values(file)
	rows=rows[1:]
	for column in rows:
		new_homework = Homework(
					id=generate_key(),
					title=column[0],
					due_date=column[1],
					description=column[2],
					schedule_id=column[3])
		new_homework.put()
	return render_template('all_done.html')


@homework_view.route('/homework/list/<id>')
def fetch_homework(id):
	student = Student.query(Student.id == id).get()
	homework = []
	schedules = student.get_schedule()
	for schedule in schedules:
		list_of_work = schedule.get_homework()
		for work in list_of_work:
			homework.append(work.dto())
	homework = multikeysort(homework, ['due_date'])
	homework = add_sort_order(homework)
	return json.dumps(homework)

def add_sort_order(input_list):
	index = 1
	for item in input_list:
		item["sort_order"] = index
		index+=1
	return input_list