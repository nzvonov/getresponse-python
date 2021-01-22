# -*- encoding: utf-8 -*-
from getresponse.entity import Entity, EntityManager


class CustomField(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field_type = None
        self.value_type = None
        self.type = None
        self.hidden = None
        self.values = None
        self.format = None


class CustomFieldManager(EntityManager):

    object_class = CustomField
    id_field_in_kwargs = 'customFieldId'
    bool_fields_in_kwargs = ('hidden', )
