from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(Integer, primary_key=True)
    actor = Column(String)
    location = Column(String)
    phone = Column(Integer)
    hired = Column(Boolean)
    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship("Role", back_populates="auditions")

    def call_back(self):
        self.hired = True

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    character_name = Column(String)

    auditions = relationship("Audition", back_populates="role")

    @property
    def actors(self):
        return [audition.actor for audition in self.auditions]

    @property
    def locations(self):
        return [audition.location for audition in self.auditions]

    def lead(self):
        hired_audition = next((audition for audition in self.auditions if audition.hired), None)
        if hired_audition:
            return hired_audition
        else:
            return 'no actor has been hired for this role'

    def understudy(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        if len(hired_auditions) >= 2:
            return hired_auditions[1]
        else:
            return 'no actor has been hired for understudy for this role'
