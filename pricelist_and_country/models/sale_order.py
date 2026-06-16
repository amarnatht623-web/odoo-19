# -*- coding: utf-8 -*-
from odoo import models,fields,api
from odoo.orm.decorators import readonly


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id')
    def set_price_list(self):
        if self.partner_id and self.partner_id.country_id:
            price = self.env['country.pricelist'].search([('country_id','=',self.partner_id.country_id.id)])
            if price:
                self.pricelist_id = price.price_list_id.id
            else:
                self.pricelist_id = self.partner_id.property_product_pricelist.id
