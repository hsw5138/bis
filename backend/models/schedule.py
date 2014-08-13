from google.appengine.ext import ndb
from helpers import generate_key
from ndbtools import ValidatedIntegerProperty
from ndbtools import ValidatedFloatProperty
from datetime import date

class Schedule(ndb.Model):
	id = ndb.StringProperty()
	name = ndb.StringProperty()
	subject_id = ndb.StringProperty()
	student_id = ndb.StringProperty()
	teacher_id = ndb.StringProperty()

	# data transfer object to form JSON
	def dto(self):
		return dict(
				id = self.id,
				name = self.name,
				subject_id = self.subject_id,
				student_id = self.student_id,
				teacher_id = self.teacher_id)
		
	def json(self):
		return dict(
				id = self.id,
				name = self.name,
				subject = self.get_subject().name,
				student = self.get_student().name,
				teacher = self.get_teacher().name)

	def get_subject(self):
		from models import Subject
		subject = Subject.query(Subject.id==self.subject_id).get()
		return subject if subject else None

	def get_student(self):
		from models import Student
		student = Student.query(Student.id==self.student_id).get()
		return student if student else None

	def get_teacher(self):
		from models import Teacher
		teacher = Teacher.query(Teacher.id==self.teacher_id).get()
		return teacher if teacher else None

	def get_homework(self):
		from models import Homework
		homework = Homework.query(Homework.schedule_id == self.id).fetch(100)
		if homework:
			homework = [work for work in homework if work.due_date >= date.today()]
		return homework if homework else []