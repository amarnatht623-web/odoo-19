from odoo import fields, models, api
from odoo.addons.test_convert.tests.test_env import record


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_product = fields.Boolean(string="is product")

    customer_products_id = fields.Many2many('product.template',string="products name")

    @api.model_create_multi
    def create(self, vals_list):
        print(id)
        for vals in vals_list:
            if vals['is_product']:
                print("hfhf")
                res = self.env['product.template'].create({
                    'name': vals.get('name'),
                })
                vals['customer_products_id'] = res
        return super().create(vals_list)



