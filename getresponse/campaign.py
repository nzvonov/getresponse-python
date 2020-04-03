# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from getresponse.entity import Entity, EntityManager


class Campaign(Entity):
    def __init__(self, *args, **kwargs):
        super(Campaign, self).__init__(*args, **kwargs)
        self.language_code = None
        self.is_default = None
        self.created_on = None
        self.description = None
        self.confirmation = None
        self.profile = None
        self.postal = None
        self.opting_types = None
        self.subscription_notifications = None

    def __unicode__(self, *args, **kwargs):
        return super(Campaign, self).__unicode__(is_default=self.is_default)


class CampaignManager(EntityManager):

    object_class = Campaign
    id_field_in_kwargs = 'campaignId'
    date_fields_in_kwargs = ['createdOn']
    bool_fields_in_kwargs = ['isDefault']
