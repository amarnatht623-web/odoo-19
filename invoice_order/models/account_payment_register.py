from ast import literal_eval

from odoo import fields,models,api
from odoo.exceptions import ValidationError


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    # copy = fields.Char('copy',compute="_compute_communication")


    @api.depends('can_edit_wizard', 'amount')
    def _compute_communication(self):
        # The communication can't be computed in '_compute_from_lines' because
        # it's a compute editable field and then, should be computed in a separated method.
        for wizard in self:
            if wizard.can_edit_wizard and wizard.installments_mode == 'full' or wizard.custom_user_amount:
                lines = wizard.line_ids
            else:
                lines = wizard._get_total_amounts_to_pay(wizard.batches)['lines']
                print(lines)
            wizard.communication = wizard._get_communication(lines) +','+ self.line_ids.move_id.copy_order_id.name












