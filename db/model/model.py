from sqlalchemy import Column, BigInteger, String, Enum
from sqlalchemy.orm import declarative_base

from db.enum.enums import Category, Language

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(Enum(Category), default=Category.SCIENTIST)
    lang = Column(Enum(Language), default=Language.ENGLISH)

    def copy_data(self, other_usr: 'User'):
        self.name = other_usr.name
        self.category = other_usr.category
        self.lang = other_usr.lang

    def __str__(self):
        return f"User(id={self.id}, name={self.name}, category={self.category.name}, lang={self.lang.name})"
