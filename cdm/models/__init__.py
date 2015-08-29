# -*- coding: utf-8 -*-

from cdm import db


class ModelMixin(object):

    def __repr__(self):
        return unicode(self.__dict__)

    def save(self):
        """ Save instance to database.
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Delete instance.
        """
        db.session.delete(self)
        db.session.commit()
