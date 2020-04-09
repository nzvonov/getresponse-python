# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from getresponse.entity import Entity, EntityManager


class Contact(Entity):
    def __init__(self, *args, **kwargs):
        super(Contact, self).__init__(*args, **kwargs)
        self.email = None
        self.note = None
        self.day_of_cycle = None
        self.origin = None
        self.created_on = None
        self.changed_on = None
        self.campaign = None
        self.time_zone = None
        self.ip_address = None
        self.activities = None
        self.scoring = None
        self.engagement_score = None

    def __unicode__(self, *args, **kwargs):
        return super(Contact, self).__unicode__(email=self.email)


class ContactManager(EntityManager):

    object_class = Contact
    id_field_in_kwargs = 'contactId'
    date_fields_in_kwargs = ('createdOn', 'changedOn', )

    def __init__(self, campaign_manager, *args, **kwargs):
        super(ContactManager, self).__init__(*args, **kwargs)
        self.campaign_manager = campaign_manager

    def _create(self, *args, **kwargs):
        contact = super(ContactManager, self)._create(*args, **kwargs)
        contact.campaign = self.campaign_manager.create(**contact.campaign)
        return contact
