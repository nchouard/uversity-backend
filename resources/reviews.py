from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
import services.reviews as reviews
from models.reviews import Review as ReviewModel

post_parser = reqparse.RequestParser()

post_parser.add_argument('comment')
post_parser.add_argument('instructor_id')
post_parser.add_argument('class_name')
post_parser.add_argument('environment_rating', type=int)
post_parser.add_argument('organization_rating', type=int)
post_parser.add_argument('clarity_rating', type=int)
post_parser.add_argument('expertise_rating', type=int)


class Review(Resource):
    def get(self, resource_id):
        review = ReviewModel.objects(id__exists=resource_id)[0]
        review = review.to_dict()
        return {'review': review}

    def put(self, review_args):
        args = post_parser.parse_args()
        review_args = args
        review = reviews.update_review(review_args)
        review.save()

    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        review_args = post_parser.parse_args()
        review_args['poster'] = user_id
        review = reviews.create_review(review_args)
        return {'review': review}

    @jwt_required
    def delete(self, id):
        review = ReviewModel.objects.get(id=id)
        review.delete_review()
        return True


class ReviewList(Resource):
    @jwt_required
    def get(self, instructor_id):
        review_list = reviews.get_reviews(instructor_id)
        return {'reviews': review_list}
