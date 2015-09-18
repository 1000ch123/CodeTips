from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Association(Base):
    __tablename__ = 'association'
    parent_id = Column(Integer, ForeignKey('parent.id'), primary_key=True)
    child_id = Column(Integer, ForeignKey('child.id'), primary_key=True)
    extra_data = Column(String(50))
    child = relationship("Child", backref="parent_assocs")


class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    children = relationship("Association", backref="parent")


class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)


# create parent, append a child via association
p = Parent()
a = Association(extra_data="some data")
a.child = Child()
p.children.append(a)

# iterate through child objects via association, including association
# attributes
for assoc in p.children:
    print(assoc.extra_data)
    print(assoc.child)
