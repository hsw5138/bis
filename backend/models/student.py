from google.appengine.ext import ndb
from ndbtools import ValidatedIntegerProperty
from ndbtools import ValidatedFloatProperty

class Student(ndb.Model):
	id = ndb.StringProperty()
	name = ndb.StringProperty()
	username = ndb.StringProperty()
	password = ndb.StringProperty()
	email = ndb.StringProperty()

	# data transfer object to form JSON
	def dto(self):
		return dict(
				id = self.id,
				name = self.name,
				username = self.username,
				password = self.password,
				email = self.email)

	def get_schedule(self):
		from models import Schedule
		classes = Schedule.query(Schedule.student_id == self.id).fetch(100000)
		return classes if classes else []