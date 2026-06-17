# -*- coding: utf-8 -*-
from odoo import models,fields

class Authors(models.Model):
    '''all related fields related to Authors'''
    _name = 'authors'
    _description = 'Authors'

    name = fields.Char(string="Authors name",required=True)
    description = fields.Char()
    authors_book_ids = fields.One2many('books',string='book author',inverse_name="book_authors_id")
