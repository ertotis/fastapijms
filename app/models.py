from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String
#good practice to record when things are created

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content= Column(String, nullable=False)
    published=Column(Boolean, nullable=False, server_default='True')
    created_at = Column(TIMESTAMP (timezone=True), nullable=False, server_default=text('now()'))
    owner_id= Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable= False)

    owner = relationship("User")
    

class User(Base):
    __tablename__ = "users"
    email=Column(String, nullable=False, unique=True)
    password= Column (String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP (timezone=True),
                         nullable=False, server_default=text('now()'))
    phone_number = Column(String)


class Vote(Base):
    __tablename__="votes"
    post_id= Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"),
    primary_key=True, nullable=False)
    user_id= Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, 
    nullable=False)