from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship  
from app.backend.db import Base, engine
from sqlalchemy.schema import CreateTable

# from app.models.task import Task
# Base = mapper_registry.generate_base()
class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True) 
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    slug = Column(String, unique=True, index=True)
    #task_id = Column(Integer, ForeignKey('tasks.id'), nullable=True)
    tasks = relationship("Task", back_populates='users')

    def __init__(self):
        pass
    def __repr__(self):
        return f""

# from sqlalchemy import Table
# users_table = Table('users', Base.metadata)
CreateTable(User.__table__)
