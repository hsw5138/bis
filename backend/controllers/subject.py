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

from models import Subject
from xl_uploader import get_row_values
from helpers import generate_key

subject_view = Blueprint('subject_view', __name__)

########### subject REST controller ###########

@subject_view.route('/subject/',methods=['GET','POST'],defaults={'id':None})
@subject_view.route('/subject/<id>',methods=['GET','PUT','DELETE'])
def subject_controller(id):
	name = request.values.get('name')

	if id:
		subject = Subject.query(Subject.id==id).get()
		if subject:
			if request.method == 'GET':
				if request.values.get('json'):
					return json.dumps(dict(subject=subject.json))
				return render_template('subject_view.html',subject = subject, title = "Subject List")
			elif request.method == 'PUT':
				subject = edit_parser(subject,request)
				subject.put()
				return 'Value Updated', 204
			elif request.method == 'DELETE':
				subject.delete()
				return 'Item deleted', 204
			else:
				return 'Method Not Allowed'
	else:
		if request.method == 'GET':
			subject_list = Subject.query().fetch(1000)
			entries=None
			if subject_list:
				entries = [subject.dto() for subject in subject_list]
			if request.values.get('json'):
				return json.dumps(dict(subject=entries))
			return render_template('subject.html',subject_entries = entries, title = "Subject List")
		elif request.method == 'POST':
			subject = Subject()
			subject = new_parser(subject,request)
			subject.put()
			url = '/subject/'
			if request.values.get('json'):
				url = '/subject/json=true'
			return redirect(url)
		else:
			return abort(405)

@subject_view.route('/subject/add/')
def subject_add_controller():
	#this is the controller to add new model entries
	return render_template('subject_add.html', title = "Add New Entry")

@subject_view.route('/subject/edit/<id>')
def subject_edit_controller(id):
	#this is the controller to edit model entries
	subject_item = Subject.query(Subject.id==id).get()
	return render_template('subject_edit.html', subject_item = subject_item, title = "Edit Entries")

@subject_view.route('/subject/upload')
def subject_upload_controller():
	return render_template('subject_excel.html')

@subject_view.route('/subject/upload/process', methods=["GET","POST"])
def subject_upload_process_controller():
	file = request.files['file']
	rows = get_row_values(file)
	rows=rows[1:]
	for column in rows:
		new_subject = Subject(
					id=generate_key(),
					name=column[0])
		new_subject.put()
	return render_template('all_done.html')