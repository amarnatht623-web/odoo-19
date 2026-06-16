from odoo import fields, models, api
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # product_qty = fields.Char()

    def button_validate(self):
        for rec in self:
            incoming_qty = 0
            product_name = []
            for record in rec.move_ids:
                incoming_qty += record.product_uom_qty
                product_name.append(record.product_id.name)

            stock_max = self.location_dest_id.max_stock
            product_quantity = sum(self.location_dest_id.quant_ids.mapped('quantity'))

            total_product = incoming_qty + product_quantity
            surplus = total_product - stock_max
            if total_product > stock_max:
                raise ValidationError(f"products : {product_name} \n"
                                      f"incoming quantity : {incoming_qty}\n"
                                      f"available product quantity: {product_quantity} \n"
                                      f"maximum capacity : {stock_max}\n"
                                      f"surplus : {surplus}")
            else:
                pass
            return super().button_validate()

    # def action_confirm(self):
    #     stock_max = self.location_dest_id.max_stock
    #     prdt_qty = sum(self.location_dest_id.quant_ids.mapped('quantity'))
    #     self.write({
    #         'product_qty':prdt_qty
    #     })
    #     print(prdt_qty)







