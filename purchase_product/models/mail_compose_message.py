from ast import literal_eval

from odoo import fields,models,api
from odoo.exceptions import ValidationError


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    # message = fields.Many2one('purchase_order',string="message")

    def action_send_mail(self):
        print('fjf')
        print(self)
        print(self.res_ids)
        ress = literal_eval(self.res_ids)
        print(type(ress))
        message = self.env['purchase.order'].browse(ress[0])
        print(message)
        if not message.order_line:
            raise ValidationError('add atleast one product')
        return super().action_send_mail()

