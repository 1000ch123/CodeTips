# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column,\
    Integer, String, DateTime, Table, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy import ForeignKey


# マッピング定義のためのベースクラス
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    tags = relationship("Tag", secondary='association', backref='users')

    def __repr__(self):
        return "<User:%s (%s)>" % (self.name, [x.name for x in self.tags])


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __repr__(self):
        return "<Tag:%s (%s)>" % (self.name, [x.name for x in self.users])


association_table = Table('association', Base.metadata,
                          Column('user_id', Integer, ForeignKey('users.id')),
                          Column('tag_id', Integer, ForeignKey('tags.id')),
                          Column('created_at', Integer, default=100)
                          )


@event.listens_for(User.tags, 'append', retval=True)
def receive_append(target, value, initiator):
    session = Session()
    target = session.query(Tag).filter(Tag.id == value).one()
    return target

# DBへの接続
engine = create_engine('sqlite:///:memory:', echo=False)
Base.metadata.create_all(engine)
# セッションクラスの作成
Session = scoped_session(sessionmaker())
Session.configure(bind=engine)

if __name__ == '__main__':
    session = Session()

    # master登録
    nico = User(name='nico')
    cool = Tag(name='cool')
    cute = Tag(name='cute')

    session.add(nico)
    session.add_all([cool, cute])
    session.commit()

    print('--- master ---')
    for i in session.query(User).all():
        print(i)

    # relation 登録
    nico.tags = [1, 2]

    print('--- adapt relation ---')
    print(session.query(User).filter(User.name == 'nico').one())
    for i in session.query(Tag).all():
        print(i)
