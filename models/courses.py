from mongoengine import *
from models.users import User
from datetime import datetime

fmt = "%Y-%m-%dT%H:%M:%SZ"

class Course(Document):
    eb_id = StringField(required=True)
    instructor = ReferenceField(User)
    name = StringField(required=True)
    description = StringField(required=True)
    # location = GeoPointField(required=True)
    category = StringField()
    # difficulty = IntField()
    start = DateTimeField()
    end = DateTimeField()
    student_list = ListField(ReferenceField(User))
    capacity = IntField()
    is_cancelled = BooleanField(default=False)

    def to_dict(self):
        dictionary = self.to_mongo()
        dictionary['instructor'] = User.objects.get(id=dictionary['instructor']).to_dict()
        dictionary['student_list'] = [User.objects.get(id=student).to_dict() for student in dictionary['student_list']]
        dictionary = {k: v for (k, v) in dictionary.items() if k != '_id'}
        dictionary['start'] = dictionary['start'].isoformat(' ')
        dictionary['end'] = dictionary['end'].isoformat(' ')
        return dictionary

    def enroll_user(self, user_id):
        user = User.objects.get(eb_id=user_id)
        try:
            user_course_history = CourseHistory.objects(user=user)[0]
        except IndexError:
            user_course_history = CourseHistory(user=user)
        user_course_history.courses += [self]
        self.student_list += [user.id]
        self.capacity -= 1
        self.save()


class CourseHistory(Document):
    user = ReferenceField(User)
    courses = ListField(ReferenceField(Course), default=[])
