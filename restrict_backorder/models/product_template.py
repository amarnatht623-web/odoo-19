from odoo import models,fields,api
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_backorder = fields.Boolean('backorder')

