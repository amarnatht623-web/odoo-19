from odoo import models,fields,api
from odoo.orm.decorators import readonly


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_email = fields.Char(related="partner_id.email",readonly=False)
    customer_phone = fields.Char(related='partner_id.phone',readonly=False)
    total_sale_order_count = fields.Integer(compute='compute_sale_order_count',store=True)

    @api.depends('partner_id')
    def compute_sale_order_count(self):
        count = self.search_count([('partner_id','=',self.partner_id),('state','=','sale')])
        self.write({
            'total_sale_order_count':count
        })

    def check_button(self):
        if self.customer_phone:
            self.write({
                'customer_phone':'999'
            })
        new = self.partner_id.search([])

        print("Count:",len(new))
        print('******Customers****')
        for record in new:
            print(record.name)
            if not record.phone:
                record.write({
                    'phone': '777'
                })

        for record in self:
            new_product=self.env.ref('sales_and_customer.new_product_2')
            print(new_product.id)
            record.order_line = [(fields.Command.clear())]
            record.order_line = [(fields.Command.create({
                'product_id':new_product.id,
                'name':new_product.name,
                'price_unit':new_product.list_price
            }))]













