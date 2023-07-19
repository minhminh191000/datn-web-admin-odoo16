from xlsxwriter import app

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import requests
import base64


class WebProduct(models.Model):
    _name = 'web.product'
    _description = _('Web product')

    name = fields.Char(string=_('Name'))
    description = fields.Text(string=_('Description'))
    rate = fields.Float(string=_('Rate'), default=1.0)
    price = fields.Integer(string=_('Price'))
    url_img = fields.Text(string=_('Avatar Image'))
    category_id = fields.Many2one('web.category', string=_('Category'))
    status = fields.Boolean(string=_('Status'), default=True)
    image_html = fields.Text(string='Image HTML', compute='_compute_image_html')

    @api.depends('url_img')
    def _compute_image_html(self):
        for record in self:
            if record.url_img:
                record.image_html = f'<img src="{record.url_img}" alt="{record.name}" width="100px" height="70px"/>'
            else:
                record.image_html = False

    @api.onchange('rate')
    def change_rate(self):
        for p in self:
            if p.rate < 1 or p.rate > 5:
                raise ValidationError('rate must be between 1 - 5')

    @api.model_create_multi
    def create(self, vals):
        res = super(WebProduct, self).create(vals)

    def _create_web_connect(self, vals):
        """

        TODO : Create product with web connections
        :param vals:
        :return:
        """
        if not self.env.company.web_config_id.token:
            web_conn = self.env['web.client']
            web_conn.send_request('POST', endpoint='/admin/api/v1/create-product', payload=vals)



