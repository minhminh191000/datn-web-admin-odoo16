from odoo import models, fields, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    web_config_id = fields.Many2one(comodel_name='web.connection',
                                        string=_('Magento Config'),
                                        related='company_id.web_config_id',
                                        readonly=False)
