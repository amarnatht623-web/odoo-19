# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.orm.decorators import readonly


class BookLine(models.Model):
    '''all fields and functions related to BookLine'''
    _name = 'book.line'
    _description = 'book Line'

    book_line_id = fields.Many2one('checkout',string="book name",required=True)
    books_id = fields.Many2one('books',string="books",required=True,domain=[('book_status','=','Available')])
    sales_price = fields.Float(compute="_compute_sales_price",required=True,readonly=False)
    cost_price = fields.Float(compute="_compute_cost_price",required=True,readonly=False)
    books_status = fields.Char(compute="_compute_book_status",required=True)
    books_author = fields.Char(related="books_id.book_authors_id.name",required=True)
    books_genres = fields.Char(related="books_id.book_genre_ids.name",required=True)
    issued_book_date = fields.Datetime(related="book_line_id.issued_date")
    return_book_date = fields.Datetime(related="book_line_id.return_date")
    checkout = fields.Char(related="book_line_id.reference_id")
    is_return_late = fields.Boolean(related="book_line_id.is_late_return")

    
    # @api.onchange('books_id')
    # def compute_sales(self):
    #     ''''''
    #     self.ensure_one()
    #     for record in self:
    #         record.cost_price = record.books_id.cost_price
    #         record.sales_price = record.books_id.sales_price
    #         record.books_status = record.books_id.book_status
    #         record.books_author = record.books_id.book_authors_id.name
    #         genres = record.books_id.book_genre_ids.mapped('name')
    #         record.books_genres =','.join(genres)

    # @api.depends('book_line_id.issued_date')
    # def compute_issued_date(self):
    #     for record in self:
    #         record.issued_book_date = record.book_line_id.issued_date
    # @api.depends('book_line_id.return_date')
    # def compute_return_date(self):
    #     for record in self:
    #         record.return_book_date = record.book_line_id.return_date

    @api.depends('books_id.books_name','books_id.book_status')
    def _compute_book_name(self):
        for record in self:
            if record.books_id.book_status == "Available":
                record.books_id = record.books_id.books_name

    @api.depends('books_id.cost_price')
    def _compute_cost_price(self):
        for record in self:
            record.cost_price = record.books_id.cost_price

    @api.depends('books_id.sales_price')
    def _compute_sales_price(self):
        for record in self:
            record.sales_price = record.books_id.sales_price
    #
    # @api.depends('books_id.book_authors_id.name')
    # def _compute_author(self):
    #     for record in self:
    #         record.books_author = record.books_id.book_authors_id.name
    #
    @api.depends('books_status')
    def _compute_book_status(self):
        for record in self:
            record.books_status = record.books_id.book_status


    # @api.depends('books_id.book_genre_ids.name')
    # def _compute_books_genres(self):
    #     for rec in self:
    #         genres = rec.books_id.book_genre_ids.mapped('name')
    #         rec.books_genres =','.join(genres)


    # @api.depends('book_line_id.reference_id')
    # def compute_reference_number(self):
    #     for rec in self:
    #         rec.checkout = rec.book_line_id.reference_id

    # @api.depends('book_line_id.is_late_return')
    # def compute_return_late(self):
    #     for rec in self:
    #         rec.is_return_late =rec.book_line_id.is_late_return