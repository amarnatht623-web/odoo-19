from calendar import month

from dateutil.relativedelta import relativedelta

from odoo import models,fields,api
from datetime import timedelta

class RealEstate(models.Model):
    _name ='real.estate'
    _description = "Real Estate"

    name = fields.Char(required=True)
    description = fields.Text(default="heloo")
    post_code = fields.Char()
    Date_availability= fields.Datetime(default= lambda self: fields.Datetime.today() + relativedelta(months=3),copy=False)
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    Gardens = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=False)
    garden_orientation = fields.Selection(
        string='type',
        selection=[('north','North'),('south','South')]
    )
    status = fields.Selection(
        [('New','New'),('outgoing','outgoing'),('done','done'),('cancel','cancel')],
    )
    property_type_id = fields.Many2one('property.type')
    partner_id = fields.Many2one("res.partner", string="Buyer")
    user_id = fields.Many2one("res.users", string="Salesperson",default=lambda self: self.env.user)
    property_tags_id = fields.Many2many('property.tags')
    offers_id = fields.One2many('property.offers','property_id')


    total_area = fields.Float(compute='_compute_total_area')
    best_offers = fields.Float(compute='_compute_best_offer')

    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area


    @api.depends('offers_id.price')
    def _compute_best_offer(self):
        for record in self:
            price_list = record.mapped('offers_id.price')
            if len(price_list) > 0:
                record.best_offers = max(price_list)
            else:
                record.best_offers   = 0


