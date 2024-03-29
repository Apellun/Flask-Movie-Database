from flask_restx import Namespace, Resource
from flask import request
from project.container import movies_service
from project.setup.api.models import movie
from project.setup.api.parsers import page_parser

api = Namespace('movies')


@api.route('/')
class MoviesView(Resource):
    @api.expect(page_parser)
    @api.marshal_with(movie, as_list=True, code=200, description='OK')
    def get(self):
        """
        Gets all movies.
        """
        if request.args.get("status") == "new":
            return movies_service.get_all_new(**page_parser.parse_args())
        return movies_service.get_all(**page_parser.parse_args())


@api.route('/<int:movie_id>/')
class MovieView(Resource):
    @api.response(404, 'Not Found')
    @api.marshal_with(movie, code=200, description='OK')
    def get(self, movie_id: int):
        """
        Gets movie by id.
        """
        return movies_service.get_item(movie_id)