# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import logging

from getresponse.enums import HttpMethod, ObjType

import requests

from .account import AccountManager
from .campaign import CampaignManager
from .contact import ContactManager
from .custom_field import CustomFieldManager
from .excs import (
    AuthenticationError,
    ExternalError,
    ForbiddenError,
    ManyRequestsError,
    NotFoundError,
    UniquePropertyError,
    ValidationError
)

logger = logging.getLogger(__name__)


class GetResponse(object):
    DEFAULT_PAGE = 1
    MAX_DATA_SIZE_LIMIT = 1000

    API_BASE_URL = 'https://api.getresponse.com/v3'

    PREPARE_PARAMS_FIELDS = ('query', 'sort', 'fields',)

    HTTP_ERRORS = (
        requests.codes.bad_request,  # 400
        requests.codes.unauthorized,  # 401
        requests.codes.forbidden,  # 401
        requests.codes.not_found,  # 404
        requests.codes.conflict,  # 409
        requests.codes.too_many_requests,  # 429
    )

    GR_CODE_UNIQUE_ERRORS = (1008,)
    GR_CODE_EXTERNAL_ERRORS = (1010,)
    GR_CODE_AUTHENTICATION_ERRORS = (1014,)
    GR_CODE_NOTFOUND_ERRORS = (1001, 1013,)
    GR_CODE_MANY_REQUESTS_ERRORS = (1015, 1016,)
    GR_CODE_FORBIDDEN_ERRORS = (1002, 1009, 1017, 1018, 1023,)
    GR_CODE_VALIDATION_ERRORS = (1000, 1003, 1004, 1005, 1006, 1007, 1011, 1012, 1021,)

    GR_ERRORS = {
        GR_CODE_UNIQUE_ERRORS: UniquePropertyError,
        GR_CODE_EXTERNAL_ERRORS: ExternalError,
        GR_CODE_AUTHENTICATION_ERRORS: AuthenticationError,
        GR_CODE_NOTFOUND_ERRORS: NotFoundError,
        GR_CODE_MANY_REQUESTS_ERRORS: ManyRequestsError,
        GR_CODE_FORBIDDEN_ERRORS: ForbiddenError,
        GR_CODE_VALIDATION_ERRORS: ValidationError,
    }

    def __init__(self, api_key, timeout=8):
        self.api_key = api_key
        self.timeout = timeout

        self.account_manager = AccountManager()
        self.campaign_manager = CampaignManager()
        self.contact_manager = ContactManager(self.campaign_manager)
        self.custom_field_manager = CustomFieldManager()

        self.managers = {
            ObjType.ACCOUNT: self.account_manager,
            ObjType.CAMPAIGN: self.campaign_manager,
            ObjType.CONTACT: self.contact_manager,
            ObjType.CUSTOM_FIELD: self.custom_field_manager,
        }

        self.session = requests.Session()
        self.session.headers.update({
            'X-Auth-Token': 'api-key {}'.format(self.api_key),
            'Content-Type': 'application/json'
        })

    @classmethod
    def __prepare_params(cls, params):

        def prepare_key_and_value(key, value):
            key = '[{}]'.format(key)
            if isinstance(value, dict):
                list_ = []
                for deep_key, deep_value in value.items():
                    for deep_key, deep_value in prepare_key_and_value(deep_key, deep_value):
                        list_.append((key + deep_key, deep_value))
                return list_

            return [(key, value)]

        for field in cls.PREPARE_PARAMS_FIELDS:
            field_data = params.get(field)
            if field_data is not None:
                del params[field]
                if field == 'fields':
                    params[field] = ','.join(field_data)
                else:
                    for key, value in field_data.items():
                        for param_key, param_value in prepare_key_and_value(key, value):
                            param_key = '{}{}'.format(field, param_key)
                            params[param_key] = param_value

        return params

    def __check_response(self, response):
        if response.status_code in self.HTTP_ERRORS:
            error_data = response.json()
            error_code = error_data.get('code')
            error_message = error_data.get('message')
            for error_code_tuple, error_class in self.GR_ERRORS.items():
                if error_code in error_code_tuple:
                    raise error_class(message=error_message, response=error_data)
            raise Exception(error_message)

    def _request(self, api_method, obj_type=None, http_method=HttpMethod.GET, body=None, payload=None):
        if payload is not None:
            payload = self.__prepare_params(payload)

        request_data = {
            'url': self.API_BASE_URL + api_method,
            'params': payload,
            'timeout': self.timeout,
        }

        http_func = http_method.name.lower()
        if http_method == HttpMethod.POST:
            request_data['json'] = body

        if http_func is not None:
            response = getattr(self.session, http_func)(**request_data)
            logger.debug("\"%s %s\" %s", http_method.name, response.url, response.status_code)
            response_process_func = '_' + http_func
            self.__check_response(response)
            return getattr(self, response_process_func)(response, obj_type)

    def _get(self, response, obj_type, *args, **kwargs):
        if response.status_code != requests.codes.ok:
            return None

        return self._create_obj(obj_type, response.json())

    def _post(self, response, obj_type, *args, **kwargs):
        if response.status_code == requests.codes.accepted:
            return True

        return self._create_obj(obj_type, response.json())

    def _delete(self, response, *args, **kwargs):
        if response.status_code == requests.codes.no_content:
            return True

        return None

    def _create_obj(self, obj_type, data):
        manager = self.managers.get(obj_type)
        if manager is None:
            return data

        method = 'create_list' if isinstance(data, list) else 'create'
        create_func = getattr(manager, method)

        return create_func(data) if method == 'create_list' else create_func(**data)

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
        return self._request('/campaigns/{}'.format(campaign_id), ObjType.CAMPAIGN, HttpMethod.POST, body)

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
        return self._request('/campaigns/{}/contacts'.format(campaign_id), ObjType.CONTACT, payload=params)

    def get_campaign_size_statistics(self, campaign_id, params=None):
        """Returns the number of the total added and removed subscribers,
        grouped by default or by time period.

        Args:
            campaign_id: ID of the campaign

            params:
                query: Used to search only resources that meets criteria.
                You can specify multiple parameters, then it uses AND logic.

        Examples:
            get_campaign_size_statistics("123", {"query": {"groupBy": "hour"}})

        Returns:
            list: dicts
        """
        request_url = '/campaigns/statistics/list-size/?query[campaignId]={}'.format(campaign_id)
        return self._request(request_url, payload=params)

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
        return self._request('/contacts/{}'.format(contact_id), ObjType.CONTACT, HttpMethod.POST, body)

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

    def get_custom_fields(self, params=None):
        """Retrieve custom fields for contacts

                Args:
                    params:
                        fields: List of fields that should be returned. Id is always returned.
                        Fields should be separated by comma

                        sort: Enable sorting using specified field (set as a key) and order (set as a value).
                        You can specify multiple fields to sort by.

                        page: Specify which page of results return.

                        perPage: Specify how many results per page should be returned
                Examples:
                    get_custom_fields({"fields": "name, fieldType"})

                Returns:
                    list: CustomField
                """
        return self._request('/custom-fields', ObjType.CUSTOM_FIELD, payload=params)

    def get_custom_field(self, custom_field_id, params):
        """Retrieve a custom field for contacts

                Args:
                    params:
                        fields: List of fields that should be returned. Id is always returned.
                        Fields should be separated by comma

                        sort: Enable sorting using specified field (set as a key) and order (set as a value).
                        You can specify multiple fields to sort by.

                        page: Specify which page of results return.

                        perPage: Specify how many results per page should be returned
                Examples:
                    get_custom_fields({"fields": "name, fieldType"})

                Returns:
                    list: CustomField
                """
        return self._request('/custom-fields/{}'.format(custom_field_id), ObjType.CUSTOM_FIELD, payload=params)

    def create_custom_field(self):
        return NotImplementedError

    def update_custom_field(self):
        return NotImplementedError

    def delete_custom_field(self):
        return NotImplementedError

    def get_rss_newsletter(self, rss_newsletter_id):
        return NotImplementedError

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

    def get_billing_info(self):
        return NotImplementedError


class GetResponseEnterprise(GetResponse):
    def __init__(self, api_key, api_domain, api_base_url='https://api3.getresponse360.com/v3', **kwargs):
        super(GetResponseEnterprise).__init__(api_key, **kwargs)
        self.API_BASE_URL = api_base_url
        self.session.headers.update({'X-Domain': api_domain})
