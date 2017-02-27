import json

from flask import url_for
from flask_restful import abort, reqparse, Resource, Api, fields, marshal

from bookzen import app, Books, str_handler


api = Api(app)

_version = 'v1.0'

resource_fields = {
        'name': fields.String,
        'name_unidecode': fields.String,
        'image_uri': fields.String,
        'price': fields.String,
        'website': fields.String(attribute='spider'),
        'author': fields.String,
        'description': fields.String,
        'url': fields.String}


class BooksListAPI(Resource):
    def get(self):
        # See more at http://flask-restful-cn.readthedocs.io/en/0.3.5/reqparse.html
        parser = reqparse.RequestParser()
        parser.add_argument('keyword', type=str, help="Name of book you want to find",
                            required=True)
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('per_page', type=int, default=10)
        args = parser.parse_args()

        # Query with keyword, order by price from low to high, then
        # paginate results.
        keyword = args.get('keyword')
        page = args.get('page')
        per_page = args.get('per_page')
        query = Books.objects.search_text(str_handler(keyword)).order_by('+price'). \
            paginate(page=page, per_page=per_page)

        books = [marshal(json.loads(i.to_json()), resource_fields) for i in query.items]

        query_args = {'keyword': keyword, 'per_page': per_page}

        # Paginate logic
        if len(books) == 0 or len(query.items) == 0:
            abort(404, message="Can not found any book with keyword: {}".format(args.get("keyword")))
        elif query.has_next is True and query.has_prev is False:
            query_args['page'] = query.next_num
            return {'books': books, 'next': url_for('books', **query_args), 'previous': ''}
        elif query.has_next is False and query.has_prev is True:
            query_args['page'] = query.next_num
            return {'books': books, 'next': '', 'previous': url_for('books', **query_args)}
        elif query.has_next is True and query.has_prev is True:
            return {'books': books, 'next': url_for('books', page=query.next_num, **query_args),
                    'previous': url_for('books', page=query.prev_num, **query_args)}
        else:
            return {'books': books, 'next': '', 'previous': ''}


api.add_resource(BooksListAPI, '/bookzen/api/{0}/books'.format(_version), endpoint='books')


if __name__ == '__main__':
    app.run(debug=True)
