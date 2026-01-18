#!/usr/bin/env python3
import pytest
from app import app, db
from models import Article, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Seed data
            user1 = User(name='John Doe')
            db.session.add(user1)
            db.session.commit()

            article1 = Article(author='Author 1', title='Title 1', content='Content 1', preview='Preview 1', minutes_to_read=5, user_id=user1.id)
            article2 = Article(author='Author 2', title='Title 2', content='Content 2', preview='Preview 2', minutes_to_read=10, user_id=user1.id)
            article3 = Article(author='Author 3', title='Title 3', content='Content 3', preview='Preview 3', minutes_to_read=15, user_id=user1.id)
            article4 = Article(author='Author 4', title='Title 4', content='Content 4', preview='Preview 4', minutes_to_read=20, user_id=user1.id)
            db.session.add_all([article1, article2, article3, article4])
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))