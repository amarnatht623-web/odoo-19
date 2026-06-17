# -*- coding: utf-8 -*-
from odoo import models,fields,api,_

class AccountMove(models.Model):
    '''all  functions and fields related to this model'''
    _inherit = 'account.move'
    def write(self,vals):
        '''Once the invoice for a return is paid, update the book's status to make it available for borrowing again.'''
        res = super().write(vals)
        for record in self:
            if record.payment_state == 'paid':
                checkout = self.env['checkout'].search([('invoice_id','=',self.id)])
                for record in checkout:
                    record.book_name_ids.books_id.book_status = 'Available'
