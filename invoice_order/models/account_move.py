from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    copy_order_id = fields.Many2one('stock.picking', string="copy")

    def confirm_invoice(self):
        print('f')
        products = self.env['stock.picking'].search([('id', '=', self.copy_order_id)])
        print(products.move_ids.product_id)

        for record in self:
            print('dn')
            print(record.id)
            record.line_ids = [(fields.Command.create({
                'product_id': products.id,
            }))]
        # if len(self.invoice_line_ids) > 0:
            # if self.line_ids_product_id in products:
            # raise ValidationError('d')

    def action_post(self):
        print('f')
        for record in self.line_ids:
            if record.product_id:
                if record.quantity == 0:
                    raise ValidationError('d')
        return super().action_post()
