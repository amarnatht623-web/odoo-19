from odoo import fields, models, api
from odoo.exceptions import ValidationError


class HospitalPrescriptionLine(models.Model):
    _name = 'hospital.prescription.line'

    appointment_id = fields.Many2one('hospital.appointment',string="appointment")
    product_id = fields.Many2one('product.product',string="product")
    dosage = fields.Char()
    days = fields.Integer()
    quantity = fields.Float()
    unit_price = fields.Float()
    _unique_product = models.Constraint('UNIQUE(product_id,appointment_id)','medicine already added')

    @api.onchange('product_id')
    def compute_unit_price(self):
        for rec in self:
            rec.unit_price = rec.product_id.list_price



    @api.constrains('product_id')
    def _prevent_duplicate(self):
        for rec in self:
            duplicate = self.search([('appointment_id','=',rec.appointment_id.id),('product_id','=',rec.product_id.id),('id','!=',rec.id)])
            print(duplicate)
            if duplicate:
                raise ValidationError('duplicate medicines in prescription')
            if rec.quantity == 0:
                raise ValidationError('0 quantity')





