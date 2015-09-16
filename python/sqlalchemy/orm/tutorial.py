# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# マッピング定義のためのベースクラス
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password)


if __name__ == '__main__':
    print(sqlalchemy.__version__)

    # DBへの接続
    engine = create_engine('sqlite:///:memory:', echo=True)\

    # table schema 作成
    print(Base.metadata.create_all(engine))

    # レコードの作成
    maki = User(name='maki', fullname='maki nishikino', password='niconico')
    print(maki)

    # セッションクラスの作成
    Session = sessionmaker()
    Session.configure(bind=engine)
    # セッションインスタンスの作成
    session = Session()

    # レコード登録
    session.add(maki)

    my_user = session.query(User).filter_by(name='maki').first()
    print(my_user)

    maki.password = 'hogehuga'
    print(my_user)
    session.commit()
    print(my_user)
