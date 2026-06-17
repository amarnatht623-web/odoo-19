from odoo import fields, models, api
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        print('hf')
        for rec in self.move_ids:
            print(self.picking_type_id.code == 'outgoing')
            if self.picking_type_id.code == 'outgoing':
                if not rec.product_id.is_backorder:
                    if rec.product_uom_qty > rec.quantity:
                        print('fj')
                        raise ValidationError('no backorder')

        return super().button_validate()

