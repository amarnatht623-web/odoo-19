from odoo import models,fields,api
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    project_task_id = fields.Many2one('project.project',string="projects")