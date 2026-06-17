from odoo import fields,models,api
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    purchase_prd_ids = fields.Many2many('product.product',string="product")
    purchase_qty = fields.Float('quantity')

    def product_confirm(self):
        print(self.id)
        for record in self.purchase_prd_ids:
            # print(self.order_line.product_id)
            # print(record.id)
            if record.id  not in self.order_line.product_id.ids:
                self.order_line = [(fields.Command.create({
                    'product_id': record.id,
                    'product_qty':self.purchase_qty,
                }))]
            else:
                for rec in self.order_line:
                    print(rec)
                    # print(self.purchase_qty)
                    # print(rec.product_id)
                    if rec.product_id.id == record.id:
                        print(rec.product_qty)
                        rec.product_qty += self.purchase_qty
                        # print(rec.product_qty)



        # product1 = []
        # for record in self.purchase_prd_ids:
        #     product1.append(record)
        #     if record not in product1:
        #         print(record)
        #         for rec in self:
        #             rec.order_line.write({
        #                 'product_qty':rec.purchase_qty+1
        #             })
        #     else:
        #         for rec in self:
        #             rec.order_line = [(fields.Command.create({
        #                 'product_id': record.id,
        #                 'product_qty':rec.purchase_qty,
        #             }))]
            # print(rec.order_line.product_id.id)
            # # if rec.order_line.product_id:
            # #     print('hd')

