# -*- coding: utf-8 -*-
"""Recruiter model module."""
from sqlalchemy import *
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, DateTime, LargeBinary
from sqlalchemy.orm import relationship, backref

from weeehire.model import DeclarativeBase, metadata, DBSession


class Recruiter(DeclarativeBase):
    __tablename__ = 'recruiters'

    uid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(32), nullable=False)
    telegram = Column(Unicode(32), nullable=False)


__all__ = ['Recruiter']
