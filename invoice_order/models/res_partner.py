from odoo import fields, models, api
from odoo.orm.decorators import readonly


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sale_text_ids = fields.One2many('sale.order',string="sale",inverse_name='partner_id')
    is_char = fields.Boolean()
    reference_no= fields.Char()

    @api.model_create_multi
    def create(self, vals_list):
        '''sequence number generation'''
        for vals in vals_list:
            if vals['is_char']:
                vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                    'res.partner')
                # if self.is_char:
            return super().create(vals_list)

    def write(self, vals):
        res = super().write(vals)
        for rec in self:
            if rec.is_char and not rec.reference_no:
                rec.reference_no = self.env['ir.sequence'].next_by_code(
                    'res.partner'
                )
            elif not rec.is_char and rec.reference_no:
                rec.reference_no = False

        return res








