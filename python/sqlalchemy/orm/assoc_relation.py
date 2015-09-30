# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import ForeignKey

# マッピング定義のためのベースクラス
Base = declarative_base()


# 中間テーブルがextra columnを持つときはassoc objを持つ必要あり
class Association(Base):
    __tablename__ = 'association'
    user_id = Column(Integer, ForeignKey('users.id'))
    tag_id = Column(Integer, ForeignKey('tags.id'))
    id = Column(Integer, primary_key=True)
    tag = relationship('Tag', backref='users')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    tags = relationship("Association", backref='user')


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))


def init_db():
    # DBへの接続
    engine = create_engine('sqlite:///:memory:', echo=False)

    # table schema 作成
    Base.metadata.create_all(engine)
    return engine


def get_session(engine):
    # セッションクラスの作成
    Session = sessionmaker()
    Session.configure(bind=engine)
    # セッションインスタンスの作成
    session = Session()
    return session


def insert_data(session):
    # レコードの作成
    # users
    tag_names = ['maki', 'nico', 'eli']
    for tag_name in tag_names:
        user = User(name=tag_name)
        session.add(user)

    # tags
    tag_names = ['cool', 'cute', 'pure', 'dere']
    for tag_name in tag_names:
        tag = Tag(name=tag_name)
        session.add(tag)

    maki = session.query(User).filter(User.name == 'maki').first()
    cool = session.query(Tag).filter(Tag.name == 'cool').first()
    a = Association()
    a.tag = cool
    maki.tags.append(a)

    session.commit()


def op(session):
    maki = session.query(User).filter(User.name == 'maki').first()
    cool = session.query(Tag).filter(Tag.name == 'cool').first()
    cute = session.query(Tag).filter(Tag.name == 'cute').first()
    dere = session.query(Tag).filter(Tag.name == 'dere').first()

    # relation add
    #maki.tags.extend([cool, cute, dere])
    a = Association()
    a.tag = cool
    maki.tags.append(a)
    session.commit()
    for u in session.query(User).all():
        print(u)

    # relation delete
    #maki.tags.remove(dere)
    session.commit()
    for u in session.query(User).all():
        print(u)

    # relation clear
    maki.tags.clear()
    session.commit()
    for u in session.query(User).all():
        print(u)

if __name__ == '__main__':
    engine = init_db()
    session = get_session(engine)
    insert_data(session)
    op(session)
