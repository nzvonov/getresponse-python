class Contact(object):
    def __init__(self, *args, **kwargs):
        self.id = args[0]
        self.href = None
        self.name = None
        self.email = None
        self.note = None
        self.day_of_cycle = None
        self.origin = None
        self.created_on = None
        self.changed_on = None
        self.campaign = None
        self.timezone = None
        self.ip_address = None
        self.activities = None
        self.scoring = None


class ContactManager(object):
    def __init__(self):
        self.contacts = {}

    def create(self, obj):
        if isinstance(obj, list):
            _list = []
            for item in obj:
                campaign = self._create(**item)
                self.contacts[campaign.id] = campaign
                _list.append(campaign)
            return _list

        campaign = self._create(**obj)
        self.contacts[campaign.id] = campaign
        return campaign

    def get(self, contact_id):
        return self.contacts.get(contact_id, None)

    def _create(self, *args, **kwargs):
        contact = Contact(kwargs['contactId'])
        if 'href' in kwargs:
            contact.href = kwargs['href']
        if 'name' in kwargs:
            contact.name = kwargs['name']
        if 'email' in kwargs:
            contact.email = kwargs['email']
        if 'note' in kwargs:
            contact.note = kwargs['note']
        if 'dayOfCycle' in kwargs:
            contact.day_of_cycle = kwargs['dayOfCycle']
        if 'origin' in kwargs:
            contact.origin = kwargs['origin']
        if 'createdOn' in kwargs:
            contact.created_on = kwargs['createdOn']
        if 'changedOn' in kwargs:
            contact.changed_on = kwargs['changedOn']
        if 'campaign' in kwargs:
            contact.campaign = kwargs['campaign']
        if 'timeZone' in kwargs:
            contact.timezone = kwargs['timeZone']
        if 'ipAddress' in kwargs:
            contact.ip_address = kwargs['ipAddress']
        if 'activities' in kwargs:
            contact.activities = kwargs['activities']
        if 'scoring' in kwargs:
            contact.scoring = kwargs['scoring']
        return contact