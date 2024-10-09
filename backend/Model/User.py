from base import Base
from marshmallow import Schema
from sqlalchemy import Column, Integer, String

class User(Base):

    __tablename__ = 'user'

    id = Column(Integer,primary_key=True)
    username = Column(String(255))
    password = Column(String(255))

# Schema For Serialization
class UserSchema(Schema):
    class Meta:
        fields = ('id', 'username', 'password')