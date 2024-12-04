from datetime import datetime
from models.courses import Course
from models.users import User
from services.instructors import create_instructor

fmt = "%Y-%m-%dT%H:%M:%SZ"
# Services for Course
def get_course(course_id):
    course = Course.objects.get(eb_id=course_id)
    return course.to_dict()


def get_courses():
    courses = [course.to_dict() for course in Course.objects()]
    return courses


def get_courses_by_category(category):
    courses = [course.to_dict() for course in Course.objects(category=category)]
    return courses


def create_course(course_args):
    if not User.objects.get(eb_id=course_args['instructor']):
        instructor = create_instructor(course_args['instructor'])
    else:
        instructor = User.objects.get(eb_id=course_args['instructor'])

    course = Course(eb_id=course_args['eb_id'],
                    name=course_args['name'],
                    description=course_args['description'],
                    start=course_args['start'],
                    end=course_args['end'],
                    capacity=course_args['capacity'],
                    category=course_args['category'],
                    instructor=instructor
                    )
    course.save()
    return course.to_dict()

  
def update_course(course_id, course_args):
    course = Course.objects.get(eb_id=course_id)
    course.name = course_args['name']
    course.description = course_args['description'],
    course.start = datetime.strptime(course_args['start'], "%Y-%m-%dT%H:%M:%SZ")
    course.end = datetime.strptime(course_args['end'], "%Y-%m-%dT%H:%M:%SZ")
    course.capacity = course_args['capacity']
    course.save()
    return course.to_dict()


def delete_course(course_id):
    course = Course.objects.get(eb_id=course_id)
    course.delete()
    return True


def cancel_course(course_id):
    course = Course.objects.get(eb_id=course_id)
    course.is_cancelled = True
    return True


def enroll_user_in_course(course_id, user_id):
    course = Course.objects.get(eb_id=course_id)
    course.enroll_user(user_id)
    return course.to_dict()
