from odoo import fields,models


class propertyType(models.Model):
    _name = 'property.type'
    _description = 'property type'

    name = fields.Char(required=True)

