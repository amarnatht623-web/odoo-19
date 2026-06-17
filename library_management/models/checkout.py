# -*- coding: utf-8 -*-
import warnings

from geoip2 import records
from odoo import fields,models,api,_
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

class CheckOut(models.Model):
    '''All the fields and functions related to checkOut'''
    _name = 'checkout'
    _rec_name = 'partner_id'
    _description = 'Checkout'

    partner_id = fields.Many2one("res.partner",string="Customer",required=True)
    # user_id = fields.Many2one('res.users',string="user")
    phone_no = fields.Char(related="partner_id.phone",readonly=False)
    partner_late_count = fields.Integer(related="partner_id.late_return")
    reference_id = fields.Char("reference", default=lambda self: _('New'),
                          copy=False, readonly=True)
    book_name_ids = fields.One2many('book.line',string="book name",inverse_name="book_line_id",required=True)
    issued_date = fields.Datetime()
    due_date = fields.Datetime()
    return_date = fields.Datetime()
    days_reminder = fields.Date()
    maximum_late_returns = fields.Integer(string="max late returns",default=lambda self:self.env['ir.config_parameter'].get_param('checkout.maximum_late_returns'))
    is_late_return = fields.Boolean()
    status = fields.Selection(selection=[
        ('Draft','Draft'),
        ('Checked out', 'Checked out'),
        ('Returned', 'Returned'),
        ('Overdue', 'Overdue'),
        ('Cancel','Cancel')

    ], string='Status', required=True, copy=False,
        tracking=True, default='Draft')
    penalty = fields.Char(string="penalty" ,compute='penalty_calc')
    diff_book = fields.Integer()
    invoice_id = fields.Many2one('account.move',string="invoice")
    payment_status = fields.Selection(related="invoice_id.payment_state")
    invoice_count = fields.Integer(compute="compute_invoice_count")

    def create_invoice(self):
        '''create invoice'''
        lines_for_invoice = []
        for record in self.book_name_ids:

            invoice_lines1 = fields.Command.create({
                'product_id':record.books_id.book_name_res.id,
                'price_unit':record.sales_price,
            })
            lines_for_invoice.append(invoice_lines1)
        for record in self:
            invoice_lines2 = fields.Command.create({
                'product_id':self.env.ref('library_management.consu_penalty_011').id,
                'price_unit':record.penalty
            })
            lines_for_invoice.append(invoice_lines2)
            invoice = self.env['account.move'].create({
                'ref': self.id,
                'move_type': 'out_invoice',
                'partner_id': self.partner_id.id,
                'invoice_line_ids': lines_for_invoice,
            })
            self.invoice_id = invoice

        return {
                    'name': 'Invoice',
                    'type': 'ir.actions.act_window',
                    'res_model': 'account.move',
                    'view_mode': 'form',
                    'view_type': 'form',
                    'target': 'current',
                    'res_id': invoice.id
                 }

    @api.depends('books_name_ids.books_id.book_status')
    def _book_available(self):
        self.book_name_ids.books_id.book_status = 'Unavailable'

    @api.depends('book_name_ids.books_status')
    def _book_unavailable(self):
        self.book_name_ids.books_id.book_status ='Available'

    def compute_invoice_count(self):
        '''compute total count of checkout '''
        for record in self:
            invoice_count1 = self.env['account.move'].search_count(
                [('ref', '=', self.id)])
            self.write({
                'invoice_count':invoice_count1
            })
    def action_view_invoice_history(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "name": "overdue history",
            "views": [[False, "list"], [False, "form"]],
            "domain": [('ref','=',self.id)],
        }
    def action_send_mail(self):
        '''email'''
        records = self.search([])
        for record in records:
            template = self.env.ref('library_management.email_template_name')
            email_values = {'email_from': self.env.user.email}
            template.send_mail(record.id, force_send=True, email_values=email_values)

    def _send_overdue_mail(self):
        """
        Automated method to send a follow-up email to partners.
        """
        for record in records:
            if record.due_date.date() < date.today():
                self.action_send_mail()

    def reminder_send_mail(self):
        '''email'''
        records = self.search([])
        for record in records:
            template = self.env.ref('library_management.email_template_name1')
            email_values = {'email_from': self.env.user.email}
            template.send_mail(record.id, force_send=True, email_values=email_values)


    def _reminder_days_mail(self):
        records = self.search([])
        for record in records:
            if record.days_reminder == date.today():
                self.reminder_send_mail()

    def _get_book_recommendation(self):
        '''Provide book recommendations when a member borrows or returns a book. Suggestions can be based on the author, genre, or popular books borrowed by others.'''
        books = self.book_name_ids.mapped('books_id')
        author = self.book_name_ids.mapped('books_author')
        genres = self.book_name_ids.mapped('books_genres')
        author_book = self.env['books'].search([('book_authors_id','in',author),('book_status','=','Available'),('id','not in',books.ids)])
        book_genres = self.env['books'].search([('book_genre_ids', 'in',genres),('book_status','=','Available'),('id','not in',books.ids)])
        popular_book = self.env['books'].search([('id','not in',books.ids),('book_status','=','Available')],order='book_count desc',limit=1)
        recommend_book = (author_book | book_genres | popular_book)
        return recommend_book.ids


    def book_confirm(self):
        '''Automatically set the checkout date, calculate the due date, and mark the book as unavailable.'''

        book_len = len(self.book_name_ids.books_id.mapped('books_name'))
        res = self.partner_id.book_max
        if self.partner_late_count <= self.maximum_late_returns:
            if book_len <= res:
                book_diff = res-book_len
                for record in self:
                    reminder_days = self.env['ir.config_parameter'].get_param('checkout.days_reminder')
                    borrow_days = self.env['ir.config_parameter'].get_param('checkout.due_date')
                    issued = fields.Datetime.now()
                    due = issued + timedelta(days = int(borrow_days))
                    reminder = due - timedelta(days=int(reminder_days))
                    record.write({
                        'status':"Checked out",
                        'issued_date':issued,
                        'due_date':due,
                        'days_reminder':reminder,
                        'diff_book':book_diff

                    })
                    # record.book_name_ids.books_id.book_count += 1
                self._book_available()
                self.action_send_mail()
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'recommendation',
                    'res_model': 'book.checkout.wizard',
                    'view_mode': 'form',
                    'target': 'new',
                    'context':{
                        'default_recommend_ids':self._get_book_recommendation(),
                        'default_name_book_id':self.id
                    }
                }
            else:
                raise ValidationError(f"borowing book must be lessthan {res}")
        else:
            raise ValidationError("Member reached their maximum return limit")

    @api.depends('due_date','return_date')
    def penalty_calc(self):
        '''penalty calculation'''
        penalty_hour = self.env['ir.config_parameter'].sudo().get_param('checkout.penalty')
        for record in self:
            if type(record.return_date)!=bool:
                if record.return_date > record.due_date:
                    hr_late = relativedelta(record.return_date,record.due_date).hours
                    day_late = relativedelta(record.return_date, record.due_date).days
                    record.penalty = hr_late*int(penalty_hour)+day_late*24*int(penalty_hour)
                else:
                    record.penalty = 0
            else:
                record.penalty=0
    @api.model_create_multi
    def create(self, vals_list):
        '''sequence number generation'''
        for vals in vals_list:
            if vals.get('reference_id', _("New")) == _("New"):
                vals['reference_id'] = self.env['ir.sequence'].next_by_code(
                    'checkout')
        return super().create(vals_list)

    def book_cancel(self):
        '''after click cancel button status is changed to Cancel'''
        self.write({
            'status':'Cancel'
        })
        self._book_available()
    def book_return(self):
        '''after click return button status is changed to return'''
        for record in self:
            self.write({
                'status':'Returned',
                'return_date':fields.Datetime.now(),
            })
            if record.return_date > record.due_date:
                self.write({
                    'is_late_return':record.partner_id
                })
