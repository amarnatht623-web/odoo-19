from odoo import fields, models, api
class ResPartner(models.Model):
    _inherit = 'res.partner'

    associated_products = fields.Many2many('product.product',string="products")

