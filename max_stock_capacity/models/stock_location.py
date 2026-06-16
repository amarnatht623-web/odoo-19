from odoo import fields, models, api
class StockLocation(models.Model):
    _inherit = 'stock.location'

    max_stock = fields.Float(string="max stock")
