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

from models import Teacher, Student, Schedule
from xl_uploader import get_row_values
from helpers import generate_key

teacher_view = Blueprint('teacher_view', __name__)

########### teacher REST controller ###########

@teacher_view.route('/teacher/',methods=['GET','POST'],defaults={'id':None})
@teacher_view.route('/teacher/<id>',methods=['GET','PUT','DELETE'])
def teacher_controller(id):
	name = request.values.get('name')
	email = request.values.get('email')

	if id:
		teacher = Teacher.query(Teacher.id==id).get()
		if teacher:
			if request.method == 'GET':
				if request.values.get('json'):
					return json.dumps(dict(teacher=teacher.json))
				return render_template('teacher_view.html',teacher = teacher, title = "Teacher List")
			elif request.method == 'PUT':
				teacher = edit_parser(teacher,request)
				teacher.put()
				return 'Value Updated', 204
			elif request.method == 'DELETE':
				teacher.key.delete()
				return 'Item deleted', 204
			else:
				return 'Method Not Allowed'
	else:
		if request.method == 'GET':
			teacher_list = Teacher.query().fetch(1000)
			entries=None
			if teacher_list:
				entries = [teacher.dto() for teacher in teacher_list]
			if request.values.get('json'):
				return json.dumps(dict(teacher=entries))
			return render_template('teacher.html',teacher_entries = entries, title = "Teacher List")
		elif request.method == 'POST':
			teacher = Teacher()
			teacher = new_parser(teacher,request)
			teacher.put()
			url = '/teacher/'
			if request.values.get('json'):
				url = '/teacher/json=true'
			return redirect(url)
		else:
			return abort(405)

@teacher_view.route('/teacher/add/')
def teacher_add_controller():
	#this is the controller to add new model entries
	return render_template('teacher_add.html', title = "Add New Entry")

@teacher_view.route('/teacher/edit/<id>')
def teacher_edit_controller(id):
	#this is the controller to edit model entries
	teacher_item = Teacher.query(Teacher.id==id).get()
	return render_template('teacher_edit.html', teacher_item = teacher_item, title = "Edit Entries")

@teacher_view.route('/teacher/upload')
def teacher_upload_controller():
	return render_template('teacher_excel.html')

@teacher_view.route('/teacher/upload/process', methods=["GET","POST"])
def teacher_upload_process_controller():
	file = request.files['file']
	rows = get_row_values(file)
	rows=rows[1:]
	for column in rows:
		new_teacher = Teacher(
					id=generate_key(),
					name=column[0],
					email=column[1])
		new_teacher.put()
	return render_template('all_done.html')

@teacher_view.route('/teacher/list/<id>')
def fetch_my_teacher(id):
	student = Student.query(Student.id == id).get()
	teacher_list = []
	schedules = student.get_schedule()
	for schedule in schedules:
		teacher = schedule.get_teacher()
		if teacher.dto() not in teacher_list:
			teacher_list.append(teacher.dto())
	other_list = []
	teachers = Teacher.query().fetch(1000)
	for teacher in teachers:
		if teacher.dto() not in teacher_list:
			other_list.append(teacher.dto())
	teacher_list = multikeysort(teacher_list, ['name'])
	teacher_list = add_sort_order(teacher_list)
	other_list = multikeysort(other_list, ['name'])
	other_list = add_sort_order(other_list)
	return json.dumps(dict(my_teacher=teacher_list,other_teachers=other_list))

def add_sort_order(input_list):
	index = 1
	for item in input_list:
		item["sort_order"] = index
		index+=1
	return input_list