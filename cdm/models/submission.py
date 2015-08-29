# -*- coding: utf-8 -*-

from sqlalchemy_utils import ArrowType
from sqlalchemy import Column, Integer, String, Boolean
from cdm import db
from cdm.models import ModelMixin

__all__ = ('Repo',)


class Submission(db.Model, ModelMixin):
    __tablename__ = 'submission'

    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    link = Column(String(200))
    created_on = Column(ArrowType)
    submitted = Column(Boolean, default=False)

    def __init__(self, title, link, created_on):
        self.title = title
        self.created_on = created_on
        self.link = link

    def __repr__(self):
        return self.title