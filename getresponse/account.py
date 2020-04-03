# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from getresponse.entity import Entity, EntityManager


class Account(Entity):
    def __init__(self, *args, **kwargs):
        super(Account, self).__init__(*args, **kwargs)
        self.first_name = None
        self.last_name = None
        self.email = None
        self.phone = None
        self.company_name = None
        self.state = None
        self.city = None
        self.street = None
        self.zip_code = None
        self.country_code = None
        self.industry_tag = None
        self.number_of_employees = None
        self.time_format = None
        self.time_zone = None

    def get_name(self):
        return '{} {}'.format(self.first_name or '', self.last_name or '')

    def __unicode__(self, *args, **kwargs):
        return super(Account, self).__unicode__(email=self.email)


class AccountManager(EntityManager):

    object_class = Account
    id_field_in_kwargs = 'accountId'
