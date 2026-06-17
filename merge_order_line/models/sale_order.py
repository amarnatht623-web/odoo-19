from odoo import models,fields,api
from odoo.orm.decorators import readonly


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    def action_confirm(self):
        for record in self:
            product_line = {}
            for line in record.order_line:
                print(line.product_id)
        return super().action_confirm

