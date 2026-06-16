from datetime import timedelta

from odoo import fields,models,api

class PropertyOffers(models.Model):
    _name = "property.offers"
    _description = "Property Offers"

    price = fields.Float(string="price")
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[('Accepted','Accepted'),('Refused','Refused')]
    )
    partner_id = fields.Many2one('res.partner',string="Salesperson",required=True)
    property_id = fields.Many2one('real.estate',string="Property",required=True)

    validity = fields.Integer(default=0)
    date_deadline = fields.Date(compute="_compute_date_deadline",inverse="inverse_deadline")

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline= fields.Date.today() + timedelta(days = record.validity)
    def inverse_deadline(self):
        for record in self:
            createdate = record.create_date.date()
            delta = record.date_deadline - createdate
            record.validity = delta.days

            # delta = record.date_deadline - fields.Date.today()
            # record.validity = delta.days

