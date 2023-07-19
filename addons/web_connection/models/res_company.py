from odoo import models, fields, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    web_config_id = fields.Many2one(comodel_name='web.connection', string=_('Web Config'))
