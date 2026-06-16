# -*- coding: utf-8 -*-
from odoo import models,fields,api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_product = fields.Boolean("products")

    def create(self,vals_list):
        record = super(SaleOrder,self).create(vals_list)
        products = record.partner_id.associated_products
        if record.is_product:
            lines=[]
            for rec in products:
                line_vals= {
                    'product_id':rec.id,
                    'name':rec.name
                }
                lines.append((0,0,line_vals))
            record.write({
                'order_line':lines
            })
        return record
    def write(self,vals):
        products = self.partner_id.associated_products
        if vals.get('is_product') == False:
            for rec in self.order_line:
                if rec.product_id in products:
                    rec.unlink()

        return super().write(vals)


        # else:
        #     lines=[]
        #     for record in products:
        #         lines.append(fields.Command.create({
        #             'order_id':self.id,
        #             'product_id':record.id
        #         }))
        #         vals['order_line'] = lines











