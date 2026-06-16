from itertools import product

from odoo import fields,models,api
from odoo.release import description


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    # task_stage = fields.Selection([('new','new'),('in progress'),('done','done')])

    def button_confirm(self):
        for record in self:
            total_qty = 0
            total_val = 0
            for rec in record.order_line:
                products = []
                total_qty += rec.product_qty
                total_val += rec.price_subtotal
                project = rec.product_id.product_tmpl_id.project_task_id
                products.append(rec.product_id.name)
                stage = self.env['project.task.type'].search([('name','=','In Progress')])
                if project:
                    description = (f'product qty:{total_qty}'
                                   f'sub total:{total_val}')
                    task = self.env['project.task'].create({
                        'display_name':"purchase order",
                        'project_id':project.id,
                        'description':description,
                        'stage_id':stage.id
                    })
                    task.message_post(body=f"Products names {products}")
                    for rec in record.order_line:
                        task1 = self.env['project.task'].create({
                            'name':rec.product_id.name,
                            'project_id':project.id,
                            'parent_id':task.id
                        })
                    break
        return super().button_confirm()



