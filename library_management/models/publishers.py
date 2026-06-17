# -*- coding: utf-8 -*-
from odoo import models,fields
from odoo.orm.fields_relational import Many2one


class Publishers(models.Model):
    '''all fields related to Publishers'''
    _name = 'publishers'
    _description = 'publishers'

    name = fields.Char(string='Publisher name',required=True)
    address = fields.Char()
    published_book_ids = fields.One2many('books',string="published book",inverse_name='book_publishers_id')
    address_name = fields.Char( string="address name")
    country_id = fields.Many2one('res.country',string="Country")
    city = fields.Char(string='city')
    street = fields.Char(string="Street")
    street2 = fields.Char(string="street2")
    state_id = Many2one('res.country.state',string="state")
    zip = fields.Integer(string='zip')


