from odoo import models,fields,api
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    customer_name = fields.Char(string='customer_name')

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            print('')
            customer_names = self.env['res.partner'].search([('customer_products_id','=',record.id)])
            print(customer_names.name)
            print(record.customer_name)
            print(record.customer_name)
            if customer_names:
                customer_names.write({
                    'name':record.customer_name
                })


