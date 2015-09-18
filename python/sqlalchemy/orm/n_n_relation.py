# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, aliased
from sqlalchemy import ForeignKey

# マッピング定義のためのベースクラス
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    # こっちに定義してある方が自然かも？
    tags = relationship("Tag", secondary='association', backref='users')

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
association_table = Table('association', Base.metadata,
        Column('user_id', Integer, ForeignKey('users.id')),
        Column('tag_id', Integer, ForeignKey('tags.id')),
        )

if __name__ == '__main__':
    # DBへの接続
    engine = create_engine('sqlite:///:memory:', echo=False)

    # table schema 作成
    Base.metadata.create_all(engine)

    # セッションクラスの作成
    Session = sessionmaker()
    Session.configure(bind=engine)
    # セッションインスタンスの作成
    session = Session()

    # レコードの作成
    # users
    maki = User(name='maki')
    nico = User(name='nico')
    eli = User(name='eli')

    session.add_all([
        maki,
        nico,
        eli
        ])

    # tags
    cool = Tag(name='cool')
    cute = Tag(name='cute')
    pure = Tag(name='pure')
    dere = Tag(name='dere')

    session.add_all([
        cool,
        cute,
        pure,
        dere
        ])

    session.commit()

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

    # relation add by ids
    print('--- id insert ---')
    user_id = 1
    tag_ids = [1, 2, 3]

    user = session.query(User).filter(User.id == user_id).first()
    tags = session.query(Tag).filter(Tag.id.in_(tag_ids)).all()
    user.tags.extend(tags)

    print(session.query(User).filter(User.id == user_id).first())
    session.rollback()

    print('--- id insert sub query ---')
    stmt = session.query(Tag).filter(Tag.id.in_(tag_ids))
    user.tags.extend(stmt)
    print(session.query(User).filter(User.id == user_id).first())
