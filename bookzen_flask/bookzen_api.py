import json

from flask import url_for
from flask_cors import CORS
from flask_restful import abort, reqparse, Resource, Api, fields, marshal
import requests

from bookzen import app, Books, str_handler
# https://github.com/LevPasha/Instagram-API-python
from instagram.InstagramAPI import InstagramAPI


app.config['ERROR_404_HELP'] = False
api = Api(app)
CORS(app)

user_name = app.config['INSTAGRAM_USER']
user_password = app.config['INSTAGRAM_PASSWORD']
insta = InstagramAPI(user_name, user_password)
insta.login()

_version = 'v1.0'

INSTA_URL = "https://www.instagram.com/explore/tags/"

INSTA_MEDIA_INFO_API = "https://api.instagram.com/oembed/?url=https://www.instagram.com/p/"

resource_fields = {
        'id': fields.String(attribute='_id'),
        'name': fields.String,
        'name_unidecode': fields.String,
        'image_uri': fields.String,
        'price': fields.String,
        'website': fields.String(attribute='spider'),
        'author': fields.String,
        'description': fields.String,
        'url': fields.String}


def keyword_to_hashtag(keyword):
    return keyword.replace(" ", "")


def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z


class GetInstagramTagFeed(Resource):
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('keyword', type=str, help="Book name or author, can not emty",
                            required=True)
        args = parser.parse_args()

        keyword = keyword_to_hashtag(args.get('keyword'))

        response = requests.get(INSTA_URL + keyword)
        js = response.text.split(' = ')[-2].split(';</script>')[0]
        data = json.loads(js)
        feed = data['entry_data']['TagPage'][0]['tag']['media']['nodes']

        for media in feed:
            if insta.mediaInfo(media['id']):
                media_info = insta.LastJson

                media['media_info'] = media_info
            else:
                insta.getUsernameInfo(media['owner']['id'])
                user = insta.LastJson
                media['media_info'] = user

        return {'entries': feed}


class GetInstagramUserInfo(Resource):
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('user_id', type=int, help="Instagram User ID", required=True)
        args = parser.parse_args()

        user_id = args.get('user_id')

        if insta.getUsernameInfo(user_id):
            return {'user': insta.LastJson}
        else:
            abort(404, message="Can not find any user with ID: {}".format(args.get("user_id")),)


class GetInstagramMediaInfo(Resource):
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('media_id', type=int, help="Instagram Media ID", required=True)
        args = parser.parse_args()

        media_id = args.get('media_id')

        if insta.mediaInfo(media_id):
            return {'media': insta.LastJson}
        else:
            abort(404, message="Can not find any media with ID: {}".format(args.get("media_id")),)


class BooksListAPI(Resource):
    def get(self):
        # See more at http://flask-restful-cn.readthedocs.io/en/0.3.5/reqparse.html
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('keyword', type=str, help="Book name or author, can not emty",
                            required=True)
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('per_page', type=int, default=12)
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

        more_info = {
                "total_pages": query.pages,
                "per_page": query.per_page,
                "page": query.page,
                "total_books": query.total,
                }

        # Paginate logic
        if len(books) == 0 or len(query.items) == 0:
            abort(404, message="Can not found any book with keyword: {}".format(args.get("keyword")),)
        elif query.has_next is True and query.has_prev is False:
            query_args['page'] = query.next_num
            return merge_two_dicts(
                    {'books': books, 'next': url_for('books', **query_args), 'previous': ''},
                    more_info)
        elif query.has_next is False and query.has_prev is True:
            query_args['page'] = query.next_num
            return merge_two_dicts(
                    {'books': books, 'next': '', 'previous': url_for('books', **query_args)},
                    more_info)
        elif query.has_next is True and query.has_prev is True:
            return merge_two_dicts(
                    {'books': books, 'next': url_for('books', page=query.next_num, **query_args),
                                     'previous': url_for('books', page=query.prev_num, **query_args)},
                    more_info)
        else:
            return merge_two_dicts({'books': books, 'next': '', 'previous': ''},
                                   more_info)


api.add_resource(BooksListAPI, '/bookzen/api/{0}/books'.format(_version), endpoint='books')
api.add_resource(GetInstagramTagFeed, '/bookzen/api/{0}/insta_feed'.format(_version))
api.add_resource(GetInstagramUserInfo, '/bookzen/api/{0}/insta_user'.format(_version))
api.add_resource(GetInstagramMediaInfo, '/bookzen/api/{0}/insta_media'.format(_version))

if __name__ == '__main__':
    app.run(debug=True)
