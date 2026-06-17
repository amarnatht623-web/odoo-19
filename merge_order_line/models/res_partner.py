from odoo import fields, models, api
class ResPartner(models.Model):
    _inherit = 'res.partner'

    def assign_user(self):
        print("d")
        for record in self:
            user = self.env.user
            user.user_ids = [(fields.Command.link(record.id))]
