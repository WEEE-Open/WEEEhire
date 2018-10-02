# -*- coding: utf-8 -*-
"""Option model module."""
from sqlalchemy import *
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, DateTime, LargeBinary
from sqlalchemy.orm import relationship, backref

from weeehire.model import DeclarativeBase, metadata, DBSession


class Option(DeclarativeBase):
    __tablename__ = 'options'

    key = Column(Unicode(255), primary_key=True, unique=True)
    value = Column(Unicode(255))

    @classmethod
    def get_value(cls, key):
        value = DBSession.query(cls).filter_by(key=key).first().value
        if value == "true":
            return True
        if value == "false":
            return False
        return value

__all__ = ['Option']
