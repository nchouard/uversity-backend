from flask_restful import Resource, reqparse
from services.instructors import create_instructor
from models.instructors import Instructor as InstructorModel

post_parser = reqparse.RequestParser()
post_parser.add_argument('user')


class Instructor(Resource):
    def get(self, id):
        instructor = InstructorModel.objects(id__exists=id)[0]
        instructor = instructor.to_dict()
        return {'instructor': instructor}

    def put(self):
        #   This method should be used in the case of updating reviews.
        pass

    def post(self):
        args = post_parser.parse_args()
        instructor_args = args
        instructor = create_instructor(instructor_args)
        return {'instructor': instructor}

    def delete(self):
        args = post_parser.parse_args()
        Instructor.delete_review(args)
        return True
