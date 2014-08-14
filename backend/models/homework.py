from google.appengine.ext import ndb
from helpers import generate_key
from ndbtools import ValidatedIntegerProperty
from ndbtools import ValidatedFloatProperty

class Homework(ndb.Model):
	id = ndb.StringProperty()
	title = ndb.StringProperty()
	due_date = ndb.DateProperty()
	description = ndb.StringProperty()
	schedule_id = ndb.StringProperty()

	# data transfer object to form JSON
	def dto(self):
		return dict(
				id = self.id,
				title = self.title,
				due_date = self.due_date.isoformat(),
				description = self.description,
				schedule_id = self.schedule_id)

	def json(self):
		return dict(
				id = self.id,
				title = self.title,
				due_date = self.due_date.isoformat(),
				description = self.description,
				schedule_id = self.get_schedule().name)

	def get_schedule(self):
		from models import Schedule
		classes = Schedule.query(Schedule.id == self.schedule_id).get()
		return classes if classes else None