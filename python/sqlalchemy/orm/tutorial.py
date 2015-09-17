# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import ForeignKey

# マッピング定義のためのベースクラス
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))

    # こっちに定義してある方が自然かも？
    addresses = relationship("Address", order_by="Address.id", backref="user")

    def __repr__(self):
        return "<User(id=%s, name='%s', fullname='%s', password='%s')>" % (
            self.id, self.name, self.fullname, self.password)


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))  # 指定はテーブル名ぽい

    # relation指定.クラス名ぽい
    # backref指定はUserクラスからの参照キー名ぽい
    # user = relationship("User", backref=backref('addresses', order_by=id))

    def __repr__(self):
        return "<Address(email_address='%s')>" % (self.email_address)

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

    # queryオブジェクトを作るとflushされる = DB更新される = idがつく
    my_user = session.query(User).filter_by(name='maki').first()
    print('--- after query ---')
    print(my_user)
    print(maki)

    print(maki is my_user)  # もはや同じものをさしているっぽい

    # レコードかきかえ
    maki.password = 'hogehuga'  # この時点で更新してる
    print('--- after update ---')
    print(my_user)

    session.commit()

    print('--- after commit ---')
    print(my_user)

    # 複数insert
    session.add_all([
        User(name='nico', fullname='nico yazawa', password='25252'),
        User(name='eli', fullname='eli ayase', password='KKE')
        ])
    maki.password = 'imiwakannai'  # この時点で更新してる

    # pending確認
    # 新規追加レコードはnew
    # updateレコードはdirtyにはいるっぽい
    print('--- before commit ---')
    print(session.new)
    print(session.dirty)
    session.commit()
    print('--- after commit ---')
    print(session.new)
    print(session.dirty)

    # where-inでselect
    print(session.query(User).filter(User.name.in_(['maki', 'nico'])).all())

    # rollback
    # queryはdbを更新するのではなく，DBデータを参考にpython世界を書き換えるぽい
    # commitして初めて更新される
    # commitするまではrollbackできるぜ！
    print('--- rollback ---')
    nise_maki = User(name='nise maki', fullname='nise maki', password='nico')
    session.add(nise_maki)
    print(session.query(User).all())
    session.rollback()  # commit前ならroolback可能
    print(session.query(User).all())

    # querying
    # queryの引数は select 対象と思えば良いかも
    print('--- querying ---')
    for user in session.query(User).order_by(User.id):
        print(user)

    # カンマは重要
    print('--- querying ---')
    for name, in session.query(User.name).order_by(User.id):
        print(name)

    # select対象外でもfilter処理自体はできる
    print('--- querying ---')
    for name, in session.query(User.name).order_by(User.id):
        print(name)

    # 複数指定すると KeyedTuppleで帰る
    print('--- querying ---')
    for row in session.query(User, User.name).order_by(User.id):
        print(row)

    # key名のaliasもできる sample見ろ

    # query filtering
    # 基本的にはfilterが表現力豊か
    print('--- filtering ---')
    for name, in session.query(User.name).\
            filter(User.fullname == 'maki nishikino'):
        print(name)

    # filterでつかえるもの
    # equals
    # query.filter(User.name == 'ed')
    # not equals
    # query.filter(User.name != 'ed')
    # like
    # query.filter(User.name.like('%ed'))
    # in
    # query.filter(User.name.in_(['ed','maki']))
    # not in
    # query.filter(~User.name.in_(['ed','maki']))
    # null
    # query.filter(User.name == None)
    # not null
    # query.filter(User.name != None)
    # and
    # query.filter(User.name == 'maki', User.age == '17')
    # or
    # query.filter(or_(User.name == 'maki', User.age == '17'))

    # address追加以降
    print('--- address ---')
    print(maki.addresses)
    maki.addresses = [
        Address(email_address='maki@example.com')
        ]
    print(maki.addresses[0])
    print(maki.addresses[0].user)

    # 追加情報の保存
    print(session.query(Address).filter(Address.user_id == 1).all())
    session.add(maki)
    session.commit()
    print(session.query(Address).filter(Address.user_id == 1).all())

    # join(inner)
    print('--- join ---')
    for u in session.query(User)\
            .join(Address)\
            .filter(Address.email_address == 'maki@example.com')\
            .all():
        print(u)
    # user以外のデータとれないの？と思うかもしれないが
    # relationshipのかたちでlinkしているのでUserさえあればなんでもできるんだなこれが
