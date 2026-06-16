from odoo import fields, models, api

class HospitalDepartment(models.Model):
    _name = 'hospital.department'
    _rec_name = 'name'

    name = fields.Char("Department name")
    doctor_ids = fields.Many2many('hr.employee',string="doctor name")