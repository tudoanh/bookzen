import json
import random
import time

from flask import url_for
from flask_cors import CORS
from flask_restful import abort, reqparse, Resource, Api, fields, marshal
import requests

from bookzen import app, Books, str_handler


app.config['ERROR_404_HELP'] = False
api = Api(app)
CORS(app)

_version = 'v1.0'

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


class InstagramBot:
    url = 'https://www.instagram.com/'
    url_login = 'https://www.instagram.com/accounts/login/ajax/'
    url_tag = 'https://www.instagram.com/explore/tags/{}/?__a=1'
    url_media_detail = 'https://www.instagram.com/p/{}/?__a=1'
    url_user_detail = 'https://www.instagram.com/{}/?__a=1'
    user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
    accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
    login_status = False
    user_login = app.config['INSTAGRAM_USER']
    user_password = app.config['INSTAGRAM_PASSWORD']
    s = requests.Session()

    def login(self):
        print('Trying to login ...')
        self.s.cookies.update({'sessionid': '', 'mid': '', 'ig_pr': '1',
                               'ig_vw': '1920', 'csrftoken': '',
                               's_network': '', 'ds_user_id': ''})
        self.login_post = {'username': self.user_login,
                           'password': self.user_password}
        self.s.headers.update({'Accept-Encoding': 'gzip, deflate',
                               'Accept-Language': self.accept_language,
                               'Connection': 'keep-alive',
                               'Content-Length': '0',
                               'Host': 'www.instagram.com',
                               'Origin': 'https://www.instagram.com',
                               'Referer': 'https://www.instagram.com/',
                               'User-Agent': self.user_agent,
                               'X-Instagram-AJAX': '1',
                               'X-Requested-With': 'XMLHttpRequest'})
        r = self.s.get(self.url)
        self.s.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
        time.sleep(2 * random.random())
        login = self.s.post(self.url_login, data=self.login_post,
                            allow_redirects=True)
        self.s.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
        self.csrftoken = login.cookies['csrftoken']
        time.sleep(2 * random.random())

        if login.status_code == 200:
            r = self.s.get('https://www.instagram.com/')
            finder = r.text.find(self.user_login)
            if finder != -1:
                self.login_status = True
                log_string = 'Login success!'
                print(log_string)
            else:
                self.login_status = False
                print('Login error! Check your login data!')
        else:
            print('Login error! Connection error!')

    def get_media_by_tag(self, tag):
        """ Get media ID set, by your hashtag """
        if self.login_status:
            url_tag = self.url_tag.format(tag)
            r = self.s.get(url_tag)
            return r.json()
        else:
            return {'error': 'Can not login'}

    def get_media_info(self, media_id):
        if self.login_status:
            media_url = self.url_media_detail.format(media_id)
            r = self.s.get(media_url)
            return r.json()
        else:
            return {'error': 'Can not login'}


class GetInstagramTagFeed(Resource):
    insta = InstagramBot()
    insta.login()

    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('keyword', type=str, help="Book name or author, can not emty",
                            required=True)
        args = parser.parse_args()

        keyword = keyword_to_hashtag(args.get('keyword'))

        data = self.insta.get_media_by_tag(keyword)
        feed = data['tag']['media']['nodes']

        for media in feed:
            media['media_info'] = self.insta.get_media_info(media['code'])

        return {'entries': feed}


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

if __name__ == '__main__':
    app.run(debug=True)
