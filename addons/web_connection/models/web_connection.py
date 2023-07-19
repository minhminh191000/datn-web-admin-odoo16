from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import requests

import json
json.decoder


class WebConnection(models.Model):
    _name = 'web.connection'
    _description = _('Web Connection Config')

    name = fields.Char(string=_('Connection Name'), required=1)
    base_url = fields.Char(string=_('Base URL'), required=1)
    username = fields.Char(string=_('Username'))
    password = fields.Char(string=_('Password'))
    token = fields.Text(string=_('Token'), compute='_compute_set_token')
    active = fields.Boolean(string=_('is Active'), default=True)

    def get_info(self):
        self.ensure_one()
        if self.active:
            return {
                'name': self.name,
                'base_url': self.base_url,
                'username': self.username,
                'password': self.password,
                'token': self.token,
            }
        raise ValidationError(_('Web Connection for your company was disabled'))

    def get_payload(self):
        self.ensure_one()
        auth_payload = {
            "email": self.username,
            "password": self.password,
        }

        return auth_payload

    @classmethod
    def _web_api_connect(self, auth_url=False, payload=False):
        jwt_token = None
        if auth_url and payload:
            response = requests.post(auth_url, json=payload)
            if response.status_code == 200:
                # Authentication successful
                auth_data = response.json()
                jwt_token = auth_data["data"]["token"]["access"]
        return jwt_token

    @api.depends('username', 'base_url', 'password')
    def _compute_set_token(self):
        """

        TODO : how to connect api login -> token jwt
        Set the token web connection -> onchange username, base_url, password
        :return:
        """
        for auth in self:
            auth_url = auth.base_url + '/admin/api/v1/login'
            payload = self.get_payload()
            try:
                conn = self._web_api_connect(auth_url=auth_url, payload= payload)
                if conn:
                    auth.token = conn
                else:
                    auth.token = None
            except Exception:
                auth.token = None


