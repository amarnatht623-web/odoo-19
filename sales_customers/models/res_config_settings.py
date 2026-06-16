from ast import literal_eval

from odoo import fields, models, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    customer_tag_id = fields.Many2many('res.partner.category')

    @api.model
    def get_values(self):
        """Get the values from settings."""
        res = super(ResConfigSettings, self).get_values()
        icp_sudo = self.env['ir.config_parameter'].sudo()
        customer_tag_id = icp_sudo.get_param('res.config.settings.customer_tag_id')
        res.update(
            customer_tag_id =[(6, 0, literal_eval(customer_tag_id))] if customer_tag_id else False,
        )
        return res

    def set_values(self):
        """Set the values. The new values are stored in the configuration parameters."""
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.customer_tag_id',
            self.customer_tag_id.ids)
        return res


