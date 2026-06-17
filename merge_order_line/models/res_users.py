from odoo import models,fields,api
from odoo.orm.decorators import readonly


class ResUsers(models.Model):
    _inherit = 'res.users'

    user_ids = fields.Many2many('res.partner',string="user")

