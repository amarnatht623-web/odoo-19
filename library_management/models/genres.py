# -*- coding: utf-8 -*-
from odoo import fields,models

class Genres(models.Model):
    '''all fields related to Genres'''
    _name = 'genres'
    _description = 'genres'


    name = fields.Char(required=True)
    book_genres_ids = fields.Many2many('books',string="",inverse_name='book_genre_ids')



