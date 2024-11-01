from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.backend.db import Base, engine
#from app.models.user import User
class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    slug = Column(String, unique=True, index=True)
    
    user = relationship("User", back_populates="tasks")
    
    def __repr__(self):
        return f"gh"


#from sqlalchemy import Table
from sqlalchemy.schema import CreateTable
#tasks_table = Table('tasks', Base.metadata)
print(CreateTable(Task.__table__ ))
#print(CreateTable(tasks_table).compile(engine))