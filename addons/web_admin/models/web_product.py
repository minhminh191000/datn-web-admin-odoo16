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
    image = fields.Image(string=_('Avatar Image'))
    category_id = fields.Many2one('web.category', string=_('Category'))
    status = fields.Boolean(string=_('Status'), default=True)
    code = fields.Char(string=_('Code'), required=True)
    image_html = fields.Text(string='Image HTML', compute='_compute_image_html')

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The name must be unique!'),
        ('unique_code', 'unique(code)', 'The code must be unique!'),
    ]



    # @api.depends('image')
    # def _compute_image_url(self):
    #     base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
    #     for product in self:
    #         if product.image:
    #             product.url_img = f"{base_url}/web/image/web.product/{product.id}/image"
    #         else:
    #             product.url_img = False

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
        res = super().create(vals)
        self._create_web_connect(res)
        return res

    def _create_web_connect(self, res):
        """

        TODO : Create product with web connections
        :param vals:
        :return:
        """
        vals = res._get_data()
        if res.env.company.web_config_id.token:
            web_conn = res.env['web.client']
            response = web_conn.send_request(method='POST', endpoint='/api/v1/product-product', payloads=vals)
            if response.status_code != 201:
                raise ValidationError('code {0} - {1}'.format(response.status_code, response.reason))

    def _get_image_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for product in self:
            if product.image:
                url_img = f"{base_url}/web/image/web.product/{product.id}/image"
            else:
                url_img = False
        return url_img

    def _get_data(self):
        list_product = []
        for product in self:
            data = {
                        "name": product.name,
                        "description": product.description,
                        "rate": product.rate,
                        "price": product.price,
                        "url_img": product.url_img or product._get_image_url(),
                        "category_id": product.category_id.id,
                        "status": product.status,
                        "code": product.code,
                        "code_category": product.category_id.code
                    }
            list_product.append(data)
        return list_product


