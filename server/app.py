#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session, request
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session.clear()
    return make_response(jsonify({'message': '200: Successfully cleared session data.'}), 200)

@app.route('/articles')
def index_articles():
    articles = []
    for article in Article.query.all():
        articles.append(article.to_dict())
    return make_response(jsonify(articles), 200)

@app.route('/articles', methods=['POST'])
def create_article():
    data = request.get_json()
    if data:
        value = data.get('some_key')
        if value:
            new_article = Article(title=value)
            db.session.add(new_article)
            db.session.commit()
            return make_response(jsonify(new_article.to_dict()), 201)
        else:
            return {'message': '400: Missing title.'}, 400
    else:
        return {'message': '400: Invalid JSON.'}, 400

@app.route('/articles/<int:id>')
def show_article(id):

    article = Article.query.filter(Article.id == id).first()

    if not article:
        return {'message': '404: Article not found.'}, 404

    viewed_articles = session.get('viewed_articles', [])
    if id not in viewed_articles:
        if len(viewed_articles) >= 3:
            return make_response(jsonify({'message': 'Maximum pageview limit reached'}), 401)
        viewed_articles.append(id)
        session['viewed_articles'] = viewed_articles
    
    session['page_views'] = len(viewed_articles)
    
    return make_response(jsonify(article.to_dict()), 200)

if __name__ == '__main__':
    app.run(port=5555)