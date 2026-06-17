from odoo import fields, models, api
class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model_create_multi
    def create(self, vals_list):
        sup = super().create(vals_list)

        print(id)
        for vals in vals_list:
            print("hfhf")
            res = self.env['project.project'].create({
                'name':vals['name'],
                'allow_billable':'True',
                'partner_id':sup.id
            })
        return sup

