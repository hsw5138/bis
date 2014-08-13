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
from helpers import edit_parser

from models import Student
from helpers import generate_key
from xl_uploader import get_row_values

student_view = Blueprint('student_view', __name__)

########### student REST controller ###########

@student_view.route('/student/',methods=['GET','POST'],defaults={'id':None})
@student_view.route('/student/<id>',methods=['GET','PUT','DELETE'])
def student_controller(id):
	name = request.values.get('name')
	username = request.values.get('username')
	email = request.values.get('email')

	if id:
		student = Student.query(Student.id==id).get()
		if student:
			if request.method == 'GET':
				if request.values.get('json'):
					return json.dumps(dict(student=student.json))
				return render_template('student_view.html',student = student, title = "Student List")
			elif request.method == 'PUT':
				student = edit_parser(student,request)
				student.put()
				return 'Value Updated', 204
			elif request.method == 'DELETE':
				student.delete()
				return 'Item deleted', 204
			else:
				return 'Method Not Allowed'
	else:
		if request.method == 'GET':
			student_list = Student.query().fetch(1000)
			entries=None
			if student_list:
				entries = [student.dto() for student in student_list]
			if request.values.get('json'):
				return json.dumps(dict(student=entries))
			return render_template('student.html',student_entries = entries, title = "Student List")
		elif request.method == 'POST':
			student = Student()
			student = new_parser(student,request)
			student.put()
			url = '/student/'
			if request.values.get('json'):
				url = '/student/json=true'
			return redirect(url)
		else:
			return abort(405)

@student_view.route('/student/add/')
def student_add_controller():
	#this is the controller to add new model entries
	return render_template('student_add.html', title = "Add New Entry")

@student_view.route('/student/edit/<id>')
def student_edit_controller(id):
	#this is the controller to edit model entries
	student_item = Student.query(Student.id==id).get()
	return render_template('student_edit.html', student_item = student_item, title = "Edit Entries")

@student_view.route('/student/upload')
def student_upload_controller():
	return render_template('student_excel.html')

@student_view.route('/student/upload/process', methods=["GET","POST"])
def student_upload_process_controller():
	file = request.files['file']
	rows = get_row_values(file)
	rows=rows[1:]
	for column in rows:
		new_student = Student(
					id=generate_key(),
					name=column[0],
					email=column[1],
					username=column[2],
					password=column[3])
		new_student.put()
	return render_template('all_done.html')

@student_view.route('/login', methods=["GET","POST"])
def do_login():
	payload = json.loads(request.data)
	student = Student.query(Student.username==payload["username"], Student.password==payload["password"]).get()
	if student:
		return json.dumps(dict(id=student.id))
	return abort(404)

