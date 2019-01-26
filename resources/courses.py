from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
import services.eventbrite as eb
import services.courses as courses
import services.users as users

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('start', type=dict)
parser.add_argument('end', type=dict)
parser.add_argument('capacity', type=int)
parser.add_argument('category')

start_parser = reqparse.RequestParser()
start_parser.add_argument('timezone', location='start')
start_parser.add_argument('utc', location='start')

end_parser = reqparse.RequestParser()
end_parser.add_argument('timezone', location='end')
end_parser.add_argument('utc', location='e')


class Course(Resource):
    @jwt_required
    def get(self, course_id):
        try:
            course = courses.get_course(course_id)
        except IndexError:
            return {'error': True, 'message': 'Course not found!'}, 403
        return {'course': course}

    @jwt_required
    def post(self):
        args = parser.parse_args()
        start_args = start_parser.parse_args(args)
        end_args = start_parser.parse_args(args)
        user_id = get_jwt_identity()
        oauth_token = users.get_user(user_id)['oauth_token']
        event_args = {'event': {'name': {'html': '<p>{}<p>'.format(args['name'])},
                                'start': {'timezone': start_args['timezone'], 'utc': start_args['utc']},
                                'end': {'timezone': end_args['timezone'], 'utc': end_args['utc']},
                                'currency': 'USD', 'capacity': args['capacity']}}
        event_id = eb.create_event(oauth_token, event_args).id
        args['eb_id'] = event_id
        args['start'] = start_args['utc']
        args['end'] = end_args['utc']
        course = courses.create_course(args)
        return {'course': course}

    @jwt_required
    def put(self):
        pass

    def delete(self):
        pass


# Methods for a list of courses
class CourseList(Resource):
    @jwt_required
    def get(self, category):
        if category:
            course_list = courses.get_courses_by_category(category)
        else:
            course_list = courses.get_courses()
        return {'courses': course_list}
