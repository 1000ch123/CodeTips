# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column,\
    Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


Base = declarative_base()


class User(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)


if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base.metadata.create_all(engine)
    Session = scoped_session(sessionmaker())
    Session.configure(bind=engine)

    session = Session()

    user = User(name=1, age='masa')  # name:String age:Integer
    print(user.name, user.age)  # instance作成できる

    session.add(user)
    session.commit()

    u = session.query(User).get(1)

    print(u.name, u.age)  # ふつうにcommit/fetchできてる.型判定どこいった
