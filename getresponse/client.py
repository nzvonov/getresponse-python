import logging
import requests
from getresponse.enums import HttpMethod, ObjType
from .account import AccountManager
from .campaign import CampaignManager
from .contact import ContactManager
from .excs import UniquePropertyError, NotFoundError

logging.basicConfig(level=logging.INFO)

account_manager = AccountManager()
campaign_manager = CampaignManager()
contact_manager = ContactManager()


class GetResponse(object):
    API_BASE_URL = 'https://api.getresponse.com/v3'
    TIMEOUT = 8

    def __init__(self, *args, **kwargs):
        self.api_key = args[0]
        self.session = requests.Session()

        self.session.headers.update({
            'X-Auth-Token': 'api-key {}'.format(self.api_key),
            'Content-Type': 'application/json'
        })

    def accounts(self, params=None):
        """Retrieves account information

        Args:
            params:
                fields: List of fields that should be returned. Id is always returned.
                Fields should be separated by comma

        Examples:
            accounts({"fields": "firstName, lastName"})

        Returns:
            object: Account
        """
        return self._request('/accounts', ObjType.ACCOUNT, payload=params)

    def ping(self):
        """Checks if API Key is working

        Returns:
            bool: True for success, False otherwise
        """
        return True if self.accounts() else False

    def get_campaigns(self, params=None):
        """Retrieve campaigns information

        Args:
            params:
                query: Used to search only resources that meets criteria.
                You can specify multiple parameters, then it uses AND logic.

                fields: List of fields that should be returned. Id is always returned.
                Fields should be separated by comma

                sort: Enable sorting using specified field (set as a key) and order (set as a value).
                You can specify multiple fields to sort by.

                page: Specify which page of results return.

                perPage: Specify how many results per page should be returned

        Examples:
            get_campaigns({"query": {"name": "XYZ"}})

        Returns:
            list: Campaign
        """
        return self._request('/campaigns', ObjType.CAMPAIGN, payload=params)

    def get_campaign(self, campaign_id, params=None):
        """Retrieves campaign information

        Args:
            campaign_id: ID of the campaign

            params:
                fields: List of fields that should be returned. Id is always returned.
                Fields should be separated by comma

        Returns:
            object: Campaign
        """
        return self._request('/campaigns/{}'.format(campaign_id), ObjType.CAMPAIGN, payload=params)

    def create_campaign(self, body):
        """Creates a campaign

        Args:
            body: data of the campaign

        Examples:
            create_campaign({"name": "XYZ"})

        Returns:
            object: Campaign
        """
        return self._request('/campaigns', ObjType.CAMPAIGN, HttpMethod.POST, body)

    def update_campaign(self, campaign_id, body):
        """Updates a campaign

        Args:
            campaign_id: ID of the campaign

            body: data of the campaign

        Examples:
            create_campaign("123", {"name": "XYZ"})

        Returns:
            object: Campaign
        """
        raise self._request('/campaigns/{}'.format(campaign_id), ObjType.CAMPAIGN, HttpMethod.POST, body)

    def get_campaign_contacts(self, campaign_id, params=None):
        """Retrieve contacts from a campaign

        Args:
            campaign_id: ID of the campaign

            params:
                query: Used to search only resources that meets criteria.
                You can specify multiple parameters, then it uses AND logic.

                fields: List of fields that should be returned. Id is always returned.
                Fields should be separated by comma

                sort: Enable sorting using specified field (set as a key) and order (set as a value).
                You can specify multiple fields to sort by.

                page: Specify which page of results return.

                perPage: Specify how many results per page should be returned

        Examples:
            get_campaign_contacts("123", {"query": {"name": "XYZ"}})

        Returns:
            list: Contact
        """
        raise self._request('/campaigns/{}/contacts'.format(campaign_id), ObjType.CONTACT)

    def get_contacts(self, params=None):
        """Retrieve contacts from all campaigns

        Args:
            params:
                query: Used to search only resources that meets criteria.
                You can specify multiple parameters, then it uses AND logic.

                fields: List of fields that should be returned. Id is always returned.
                Fields should be separated by comma

                sort: Enable sorting using specified field (set as a key) and order (set as a value).
                You can specify multiple fields to sort by.

                page: Specify which page of results return.

                perPage: Specify how many results per page should be returned

                additionalFlags: Additional flags parameter with value 'exactMatch' will search contacts
                with exact value of email and name provided in query string. Without that flag matching
                is done via standard 'like' comparison, what could be sometimes slow.

        Examples:
            get_contacts({"query": {"name": "XYZ"}})

        Returns:
            list: Contact
        """
        return self._request('/contacts', ObjType.CONTACT, payload=params)

    def get_contact(self, contact_id, params=None):
        """Retrieves contact information

        Args:
            contact_id: ID of the contact

            params:
                fields: List of fields that should be returned. Id is always returned.
                Fields should be separated by comma

        Examples:
            get_contacts({"fields": "name, email"})

        Returns:
            object: Contact
        """
        return self._request('/contacts/{}'.format(contact_id), ObjType.CONTACT, payload=params)

    def create_contact(self, body):
        """Creates a contact

        Args:
            body: data of the contact

        Examples:
            create_contact({"email": "XYZ", "campaign": {"campaign_id": "XYZ"}})

        Returns:
            bool: True for success, False otherwise
        """
        return self._request('/contacts', ObjType.CONTACT, HttpMethod.POST, body)

    def update_contact(self, contact_id, body):
        """Updates a contact

        Args:
            contact_id: ID of the contact

            body: data of the contact

        Examples:
            update_contact("123", {"name": "XYZ"})

        Returns:
            object: Contact
        """
        raise self._request('/contacts/{}'.format(contact_id), ObjType.CONTACT, HttpMethod.POST, body)

    def delete_contact(self, contact_id, params=None):
        """Deletes a contact

        Args:
            contact_id: ID of the contact

            params:
                messageId: ID of message

                ipAddress: User unsubscribe IP address

        Examples:
            delete_contact("123", {"messageId": "XYZ"})

        Returns:
            bool: True for success, False otherwise
        """
        return self._request('/contacts/{}'.format(contact_id), ObjType.CONTACT, HttpMethod.DELETE, payload=params)

    def get_rss_newsletter(self, rss_newsletter_id):
        raise NotImplementedError

    def send_newsletter(self):
        return NotImplementedError

    def send_draft_newsletter(self):
        return NotImplementedError

    def search_contacts(self):
        return NotImplementedError

    def get_contacts_search(self):
        return NotImplementedError

    def add_contacts_search(self):
        return NotImplementedError

    def delete_contacts_search(self):
        return NotImplementedError

    def get_contact_activities(self):
        return NotImplementedError

    def get_webforms(self):
        return NotImplementedError

    def get_webform(self):
        return NotImplementedError

    def get_forms(self):
        return NotImplementedError

    def get_form(self):
        return NotImplementedError

    def get_custom_fields(self):
        return NotImplementedError

    def get_custom_field(self):
        return NotImplementedError

    def set_custom_field(self):
        return NotImplementedError

    def get_billing_info(self):
        return NotImplementedError

    def _request(self, api_method, obj_type, http_method=HttpMethod.GET, body=None, payload=None):
        if http_method == HttpMethod.GET:
            response = self.session.get(
                self.API_BASE_URL + api_method, params=payload, timeout=self.TIMEOUT)
            if response.status_code != 200:
                return None
            return self._create_obj(obj_type, response.json())

        if http_method == HttpMethod.POST:
            response = self.session.post(
                self.API_BASE_URL + api_method, json=body, params=payload, timeout=self.TIMEOUT)
            if response.status_code == 400:
                error = response.json()
                if error['code'] == 1001:
                    raise NotFoundError(error['message'])
            if response.status_code == 409:
                # Error cuando el ID no es único.
                error = response.json()
                raise UniquePropertyError(error['message'])
            if response.status_code == 202:
                # Respuesta exitosa para un objeto que no se crea inmediatamente.
                return True
            return self._create_obj(obj_type, response.json())

        if http_method == HttpMethod.DELETE:
            response = self.session.delete(
                self.API_BASE_URL + api_method, params=payload, timeout=self.TIMEOUT)
            if response.status_code == 204:
                # Respuesta exitosa para un objeto que no se borra inmediatamente.
                return True
            return None

    def _create_obj(self, obj_type, data):
        if obj_type == ObjType.ACCOUNT:
            obj = account_manager.create(data)
        elif obj_type == ObjType.CAMPAIGN:
            obj = campaign_manager.create(data)
        elif obj_type == ObjType.CONTACT:
            obj = contact_manager.create(data)
        return obj