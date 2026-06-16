from odoo import models,fields

class CountryPricelist(models.Model):
    _name = 'country.pricelist'
    _rec_name = 'country_id'

    country_id = fields.Many2one('res.country',string="country",required=True,store=True)
    price_list_id = fields.Many2one('product.pricelist',string="pricelist",required=True,store=True)

