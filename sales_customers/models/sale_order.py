from odoo import models,fields,api
from odoo.orm.decorators import readonly


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    allowed_tags_ids = fields.Many2many('res.partner.category',string="jd",compute="onchange_partner")

    @api.depends()
    def onchange_partner(self):
        print('dss')
        tags = self.env['ir.config_parameter'].sudo().get_param('res.config.settings.customer_tag_id')
        print(tags)
        tags_ids = eval(tags) if tags else []
        for rec in self:
            rec.allowed_tags_ids = [(fields.Command.set(tags_ids))]
            print(rec.allowed_tags_ids)

