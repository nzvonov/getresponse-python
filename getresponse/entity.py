# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict

from dateutil.parser import parse as parse_date

from six import text_type


class Entity(object):
    def __init__(self, _id, *args, **kwargs):
        self.id = _id
        self.name = None
        self.href = None

    def __unicode__(self, *args, **kwargs):
        params = OrderedDict({'id': self.id, 'name': self.get_name()})
        params.update(kwargs)
        format_str = map(lambda param: "{}='{}'".format(param[0], param[1]), params.items())
        return ", ".join(format_str)

    def __repr__(self):
        try:
            obj_str = text_type(self)
        except (UnicodeEncodeError, UnicodeDecodeError):
            obj_str = '[Bad Unicode data]'
        return '<{}({})>'.format(self.__class__.__name__, obj_str).encode(encoding='utf-8', errors='strict')

    def get_name(self):
        return self.name


class EntityManager(object):

    object_class = Entity
    id_field_in_kwargs = None
    date_fields_in_kwargs = []
    bool_fields_in_kwargs = []

    @staticmethod
    def __get_fields_list(obj):
        obj_fields_list = obj.__dict__.keys()
        obj_fields_list.remove('id')
        splitter = '_'
        for obj_field in obj_fields_list:
            kwargs_field = obj_field
            if splitter in obj_field:
                split_field = obj_field.split(splitter)
                titled_words = map(lambda word: word.title(), split_field[1:])
                kwargs_field = ''.join(split_field[:1] + titled_words)
            yield obj_field, kwargs_field

    def _create(self, *args, **kwargs):
        entity_id = kwargs.get(self.id_field_in_kwargs)
        entity = self.object_class(_id=entity_id)
        for obj_field, kwargs_field in self.__get_fields_list(entity):
            field_data = kwargs.get(kwargs_field)
            if field_data is not None:
                if kwargs_field in self.date_fields_in_kwargs:
                    field_data = parse_date(field_data)
                if kwargs_field in self.bool_fields_in_kwargs:
                    field_data = field_data == 'true'
            setattr(entity, obj_field, field_data)
        return entity

    def create(self, obj):
        return self._create(**obj)

    def create_list(self, objs):
        for obj in objs:
            yield self.create(**obj)
