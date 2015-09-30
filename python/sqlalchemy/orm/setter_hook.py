# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, event
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))

    def __repr__(self):
        return "<User(id=%s, name='%s', fullname='%s')>" % (
            self.id, self.name, self.fullname)


@event.listens_for(User.name, 'set', named=True, retval=True)
def receive_set(**kw):
    print('--- set event listener ---')
    target = kw['target']
    value = kw['value']
    print(target)
    print(value)
    print('--- return ---')
    return 'hoge'


if __name__ == '__main__':
    maki = User(name='maki')
    print(maki)
    maki.name = 'nicomaki'
    print(maki)
