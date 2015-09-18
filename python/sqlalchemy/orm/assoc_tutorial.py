from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Association(Base):
    __tablename__ = 'association'
    parent_id = Column(Integer, ForeignKey('parent.id'), primary_key=True)
    child_id = Column(Integer, ForeignKey('child.id'), primary_key=True)
    child = relationship("Child", backref="parents")


class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    children = relationship("Association", backref="parent")


class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)


# create parent, append a child via association
p = Parent()
c = Child()
a = Association()

# どっちでもいけるよ
# a.child = c
# p.children.append(a)
a.parent = p
c.parents.append(a)

print(p.children)
print(c.parents)

# iterate through child objects via association, including association
# attributes
for assoc in p.children:
    print(assoc.child)
    print(assoc.parent)
    print(assoc.child.parents)
