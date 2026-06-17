# -*- coding: utf-8 -*-
from itertools import product

from reportlab.graphics.barcode import widgets

from odoo import models,fields,api,_
from odoo.orm.fields_numeric import Integer


class Books(models.Model):
    '''all the fields and functions related to Books'''
    _name = 'books'
    # _inherit = 'product.product'
    _description = 'Books'
    _rec_name = 'books_name'


    books_name = fields.Char(required=True,string="Title")
    book_name_res = fields.Many2one('product.product')
    image = fields.Image(string=' ',)
    attachment_filename = fields.Char(string='Attachment Filename')
    book_id = fields.Char("book id", default=lambda self: _('New'),
                         copy=False, readonly=True, tracking=True)
    book_isbn = fields.Char()
    sales_price = fields.Float()
    cost_price = fields.Float()
    book_status = fields.Selection([('Available','Available'),('Unavailable','Unavailable'),('Comming soon','Comming soon')]
    )
    book_authors_id = fields.Many2one('authors',string='Author',inverse_name="authors_book_ids")
    book_publishers_id = fields.Many2one('publishers',string='publisher')
    book_genre_ids = fields.Many2many('genres',string="book genres")
    _unique_book_isbn = models.Constraint('UNIQUE(book_isbn)','isbn number already exist')
    book_count = fields.Integer(string="book count",default=0)
    book_description = fields.Html("description")

    @api.model_create_multi
    def create(self, vals_list):
        '''create sequence number'''
        for vals in vals_list:
            if vals.get('book_id', _("New")) == _("New"):
                vals['book_id'] = self.env['ir.sequence'].next_by_code(
                    'books')
                print('uh',vals['book_id'])
            res = self.env['product.product'].create({
                'name':vals.get('books_name'),
                'list_price':vals.get('sales_price'),
                'type': 'consu'
            })
            vals['book_name_res'] = res.id
        return super().create(vals_list)

