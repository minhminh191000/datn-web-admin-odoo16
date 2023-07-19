from odoo import models, _
from odoo.exceptions import ValidationError
import requests

class WebClient(models.AbstractModel):
    """
    For using this model, we just
    """
    _name = 'web.client'

    def authenticate(self, **kwargs):
        conn = self._get_connection_info()
        headers = {
            "Authorization": f"Bearer {conn.token}",
            "Content-Type": "application/json"  # Adjust the content type according to your API requirements
        }
        return conn.get('base_url'), headers

    def _get_connection_info(self):
        """

        :return:
        """
        config = self.env.user.company_id.web_config_id
        if config.id:
            return config.get_info()
        raise ValidationError(_('Please config Magento Connection'))

    def _call(self, method, endpoint, payloads, **kwargs) -> dict:
        """

        :param method:
        :param endpoint:
        :param payloads:
        :param kwargs:
        :return:
        """
        # TODO: Create logs for magento synchronization
        base_url, headers = self.authenticate()
        url_request = base_url + endpoint
        if method == 'POST' or method == 'post':
            request = requests.post(url_request, data=payloads, headers=headers)
        elif method == 'GET' or method == 'get':
            request = requests.get(url_request, headers=headers)
        elif method == 'PUT' or method == 'put':
            request = None
        elif method == 'DELETE' or method == 'delete':
            request = None
        else:
            raise ValidationError('Invalid method')

        return request

    def call(self, method, endpoint, payloads, **kwargs):
        return self._call(method, endpoint, payloads, **kwargs)

    @staticmethod
    def _process_response(response):
        pass

    def send_request(self, method, endpoint, payloads, **kwargs):
        """

        :param method:
        :param endpoint:
        :param payloads:
        :param kwargs:
        :return:
        """
        response = self._call(method, endpoint, payloads, **kwargs)
        response_handler = kwargs.get('response_handler')
        if response_handler is not None:
            response_handler = self._process_response
        return response_handler(response)
