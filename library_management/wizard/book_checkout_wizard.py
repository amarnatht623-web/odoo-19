# -*- coding: utf-8 -*-
from odoo import api,fields,models
from odoo.exceptions import ValidationError
from odoo.orm.decorators import readonly
class BookCheckoutWizard(models.TransientModel):
    '''all functions and fields related to BookCheckoutWizard'''
    _name = 'book.checkout.wizard'
    _description = 'book checkout wizard'

    recommend_ids = fields.Many2many('books',string="recommend books",domain=[('book_status','=','Available')])
    name_book_id = fields.Many2one('checkout',string="book name")


    @api.depends('recommend_ids.book_status')
    def _book_available(self):
        self.recommend_ids.book_status = "Unavailable"


    def Confirm_orders(self):
        book_len_wiz = len(self.recommend_ids.mapped('books_name'))

        book_max_count = self.name_book_id.diff_book
        if book_len_wiz <= book_max_count:
            for record in self:
                checkout = record.name_book_id
                lines=[]
                for book in record.recommend_ids:
                    if book not in lines:
                        lines.append(fields.Command.create({'books_id':book.id}))
                    else:
                        continue
            checkout.write({
                'book_name_ids':lines,
            })
            self._book_available()
        else:
            raise ValidationError(f"book must be lessthan {book_max_count}")



