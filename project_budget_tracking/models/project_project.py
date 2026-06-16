from odoo import models,fields,api
class ProjectProject(models.Model):
    _inherit = 'project.project'

    # proj = fields.Char(string="f")

    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    proj_budget = fields.Monetary(string="project budget",compute='compute_budget_spend',store=True,readonly=False)
    budget_spend = fields.Monetary(string="budget spend")
    # budget_percentage = fields.Char()
    @api.depends('task_ids.timesheet_ids.unit_amount')
    def compute_budget_spend(self):
        for record in self:
            total_cost = 0
            print('record:',record.id)
            timesheet = self.env['account.analytic.line'].search([('project_id','=',record.id)])
            print('timesheet:',timesheet)
            for rec in timesheet:
                print("time sheet")
                employee = rec.employee_id
                print('employee:',employee.name)
                rate = employee.hourly_cost
                print('rate:',rate)
                total_cost += rec.unit_amount * rate
            print('total:',total_cost)
            record.budget_spend = total_cost
            if record.budget_spend > (record.proj_budget * (0.8 / 100) * 100):
                print("hi")
                record.message_post(body="Warning,budget exceeded 80%")
            else:
                print("he;;;")
                self.action_send_mail()

    def action_send_mail(self):
        '''email'''
        records = self.search([])
        for record in records:
            template = self.env.ref('project_budget_tracking.email_template_project')
            email_values = {'email_from': self.env.user.email}
            template.send_mail(record.id, force_send=True, email_values=email_values)

    def send_project_mail(self):
        for record in self:
            if record.budget_spend > (record.proj_budget * (0.8 / 100) * 100):
                self.action_send_mail()





