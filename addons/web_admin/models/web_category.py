from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class WebCategory(models.Model):
    _name = 'web.category'
    _description = 'Web Category'
        
    name = fields.Char(string=_('Name'), required=True)
    description = fields.Char(string=_('Description'))
    url_img = fields.Text(string=_('Url img'))
    status = fields.Boolean(string=_('Status'), default=True)
    code = fields.Char(string=_('Code'), required=True)
    image_html = fields.Text(string='Image HTML', compute='_compute_image_html')

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'The name must be unique!'),
        ('unique_code', 'unique(code)', 'The code must be unique!'),
    ]

    @api.depends('url_img')
    def _compute_image_html(self):
        for record in self:
            if record.url_img:
                record.image_html = f'<img src="{record.url_img}" alt="{record.name}" width="100px" height="70px"/>'
            else:
                record.image_html = False