from google.appengine.ext import ndb
from helpers import generate_key
from ndbtools import ValidatedIntegerProperty
from ndbtools import ValidatedFloatProperty

class Teacher(ndb.Model):
	id = ndb.StringProperty()
	name = ndb.StringProperty()
	email = ndb.StringProperty()

	# data transfer object to form JSON
	def dto(self):
		return dict(
				id = self.id,
				name = self.name,
				email = self.email)

	def get_schedule(self):
		from models import Schedule
		classes = Schedule.query(Schedule.teacher_id == self.id).fetch(1000)
		return classes if classes else []