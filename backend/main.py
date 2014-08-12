# do not change the following basic imports and configurations  if you still want to use box.py
import settings

from flask import Flask
app = Flask(__name__)
app.config.from_object('settings')

from controllers import base_view, teacher_view, student_view, subject_view, homework_view, schedule_view

app.register_blueprint(base_view)
app.register_blueprint(teacher_view)
app.register_blueprint(student_view)
app.register_blueprint(subject_view)
app.register_blueprint(homework_view)
app.register_blueprint(schedule_view)