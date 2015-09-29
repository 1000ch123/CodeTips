# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, aliased
from sqlalchemy import ForeignKey

from benchmarker import Benchmarker

# マッピング定義のためのベースクラス
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    # こっちに定義してある方が自然かも？
    tags = relationship("Association", backref='users')

    def __repr__(self):
        return "<User:%s (%s)>" % (self.name, self.tags)


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __repr__(self):
        return "<Tag:%s>" % self.name


# 中間テーブルが余計な情報持たないときはこれでok
# 中間テーブルがextra columnを持つときはassoc objを持つ必要あり
class Association(Base):
    __tablename__ = 'association'
    # user_id = Column(Integer, ForeignKey('users.id'), primary_key=True),
    # tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True),
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    tag_id = Column(Integer, ForeignKey('tags.id'))
    tag = relationship('Tag', backref='users')

with Benchmarker(width=20, cycle=10) as bench:

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
        maki.tags.extend([cool, cute, dere])
        session.commit()
        for u in session.query(User).all():
            print(u)

        # relation delete
        maki.tags.remove(dere)
        session.commit()
        for u in session.query(User).all():
            print(u)

        # relation clear
        maki.tags.clear()
        session.commit()
        for u in session.query(User).all():
            print(u)

    #@bench('id')
    def op_by_id(bm):
        engine = init_db()
        session = get_session(engine)
        insert_data(session)
        with bm:
            # relation add by ids
            print('--- id insert ---')
            user_id = 1
            tag_ids = [1, 2, 3]

            tags = session.query(Tag).filter(Tag.id.in_(tag_ids)).all()
            user = session.query(User).filter(User.id == user_id).first()
            user.tags.extend(tags)

            print(session.query(User).filter(User.id == user_id).first())
            session.rollback()

    #@bench('sq')
    def op_by_id_subquery(bm):
        engine = init_db()
        session = get_session(engine)
        insert_data(session)
        with bm:
            # relation add by ids
            print('--- id insert sub query ---')
            user_id = 1
            tag_ids = [1, 2, 3]

            stmt = session.query(Tag).filter(Tag.id.in_(tag_ids))
            user = session.query(User).filter(User.id == user_id).first()
            user.tags.extend(stmt)

            print(session.query(User).filter(User.id == user_id).first())
            session.rollback()

    #@bench('direct')
    def op_by_direct(bm):
        engine = init_db()
        session = get_session(engine)
        insert_data(session)
        with bm:
            # relation add by ids
            print('--- id insert directly ---')
            user_id = 1
            tag_ids = [1, 2, 3]

            stmt = session.query(Tag).filter(Tag.id.in_(tag_ids))
            user = session.query(User).filter(User.id == user_id).first()
            user.tags.extend(stmt)

            print(session.query(User).filter(User.id == user_id).first())
            session.rollback()


if __name__ == '__main__':
    engine = init_db()
    session = get_session(engine)
    insert_data(session)
    op(session)
    op_by_id(session)
    op_by_id_subquery(session)
