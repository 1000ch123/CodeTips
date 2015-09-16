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
        return "<User(id=%s, name='%s', fullname='%s', password='%s')>" % (
            self.id, self.name, self.fullname, self.password)


if __name__ == '__main__':
    print(sqlalchemy.__version__)

    # DBへの接続
    engine = create_engine('sqlite:///:memory:', echo=False)\

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
    print('--- before insert ---')
    print(maki)
    session.add(maki)  # この時点ではpending
    print('--- after insert ---')
    print(maki)

    # queryオブジェクトを作るとflushされる！=DB更新される
    my_user = session.query(User).filter_by(name='maki').first()
    print('--- after query ---')
    print(my_user)
    print(maki)

    print(maki is my_user)  # もはや同じものをさしているっぽい

    # レコードかきかえ
    maki.password = 'hogehuga'  # この時点で更新してる
    print('--- after update ---')
    print(my_user)
    print(maki)

    session.commit()

    print('--- after commit ---')
    print(my_user)
