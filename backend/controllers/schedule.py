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

from models import Schedule, Student, Teacher, Subject
from xl_uploader import get_row_values
from helpers import generate_key

schedule_view = Blueprint('schedule_view', __name__)

########### schedule REST controller ###########

@schedule_view.route('/schedule/',methods=['GET','POST'],defaults={'id':None})
@schedule_view.route('/schedule/<id>',methods=['GET','PUT','DELETE'])
def schedule_controller(id):
	name = request.values.get('name')
	subject_id = request.values.get('subject_id')
	student_id = request.values.get('student_id')
	teacher_id = request.values.get('teacher_id')

	if id:
		schedule = Schedule.query(Schedule.id==id).get()
		if schedule:
			if request.method == 'GET':
				if request.values.get('json'):
					return json.dumps(dict(schedule=schedule.json))
				return render_template('schedule_view.html',schedule = schedule, title = "Schedule List")
			elif request.method == 'PUT':
				schedule = edit_parser(schedule,request)
				schedule.put()
				return 'Value Updated', 204
			elif request.method == 'DELETE':
				schedule.delete()
				return 'Item deleted', 204
			else:
				return 'Method Not Allowed'
	else:
		if request.method == 'GET':
			schedule_list = Schedule.query().fetch(1000)
			entries=None
			if schedule_list:
				entries = [schedule.dto() for schedule in schedule_list]
			if request.values.get('json'):
				return json.dumps(dict(schedule=entries))
			return render_template('schedule.html',schedule_entries = entries, title = "Schedule List")
		elif request.method == 'POST':
			schedule = Schedule()
			schedule = new_parser(schedule,request)
			schedule.put()
			url = '/schedule/'
			if request.values.get('json'):
				url = '/schedule/json=true'
			return redirect(url)
		else:
			return abort(405)

@schedule_view.route('/schedule/add/')
def schedule_add_controller():
	#this is the controller to add new model entries
	students = Student.query().fetch(1000)
	teachers = Teacher.query().fetch(1000)
	subjects = Subject.query().fetch(1000)
	return render_template('schedule_add.html', title = "Add New Entry", students=students, teachers=teachers, subjects=subjects)

@schedule_view.route('/schedule/edit/<id>')
def schedule_edit_controller(id):
	#this is the controller to edit model entries
	schedule_item = Schedule.query(Schedule.id==id).get()
	return render_template('schedule_edit.html', schedule_item = schedule_item, title = "Edit Entries")
