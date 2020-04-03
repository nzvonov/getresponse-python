# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from dateutil.parser import parse as parse_date


class Entity(object):
    def __init__(self, _id, *args, **kwargs):
        self.id = _id
        self.href = None
        self.name = None

    def get_name(self):
        return self.name

    def __repr__(self):
        return "<{}(id='{}', name='{}'".format(self.__class__.__name__, self.id, self.get_name())


class EntityManager(object):

    object_class = Entity
    id_field_in_kwargs = None
    date_fields_in_kwargs = []
    bool_fields_in_kwargs = []

    def __init__(self, *args, **kwargs):
        super(EntityManager, self).__init__(*args, **kwargs)

    @staticmethod
    def __get_fields_list(obj):
        obj_fields_list = obj.__dict__.keys()
        obj_fields_list.remove('id')
        fields_list = []
        splitter = '_'
        for obj_field in obj_fields_list:
            kwargs_field = obj_field
            if splitter in obj_field:
                split_field = obj_field.split(splitter)
                titled_words = map(lambda word: word.title(), split_field[1:])
                kwargs_field = ''.join(split_field[:1] + titled_words)
            fields_list.append((obj_field, kwargs_field))
        return fields_list

    def create(self, obj):
        if isinstance(obj, list):
            _list = []
            for item in obj:
                entity = self._create(**item)
                _list.append(entity)
            return _list

        entity = self._create(**obj)
        return entity

    def _create(self, *args, **kwargs):
        entity_id = kwargs.get(self.id_field_in_kwargs)
        entity = self.object_class(_id=entity_id)
        fields_list = self.__get_fields_list(entity)

        test = set(kwargs.keys()).difference(set(field[1] for field in fields_list))
        print test

        for obj_field, kwargs_field in fields_list:
            field_data = kwargs.get(kwargs_field)
            if field_data is not None:
                if kwargs_field in self.date_fields_in_kwargs:
                    field_data = parse_date(field_data)
                if kwargs_field in self.bool_fields_in_kwargs:
                    field_data = field_data == 'true'
            setattr(entity, obj_field, field_data)
        return entity
