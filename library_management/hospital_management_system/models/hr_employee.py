from odoo import fields, models, api
class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_doctor = fields.Boolean()
    specialization = fields.Char()
    is_available = fields.Boolean()
