# -*- coding: utf-8 -*-
from email.policy import default
from odoo import fields, models, api
from odoo.orm.decorators import readonly


class ResPartner(models.Model):
    _inherit = 'res.partner'
    checkout_count = fields.Integer(string="checkout count",
                                    compute='compute_checkout_count',
                                    default=0)
    late_return = fields.Integer(string="late return",compute="compute_late_returns")
    book_max = fields.Integer(string="max book",default=lambda self:int(self.env['ir.config_parameter'].get_param('res_partner.book_max')),readonly=False)
    company_id = fields.Many2one('res.company',store=True,copy=False,default=lambda self:self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda
                                      self: self.env.user.company_id.currency_id.id)
    penalty = fields.Char(compute="compute_penalty")
    @api.model_create_multi
    def create(self,vals_list):
        book_max1 = int(self.env['ir.config_parameter'].get_param('res.partner.book_max'))
        if book_max1 > 0:
            for val in vals_list:
                val['book_max'] = book_max1
        return super().create(vals_list)

    def compute_checkout_count(self):
        '''compute total count of checkout '''
        for record in self:
            record.checkout_count = self.env['book.line'].search_count(
                [('book_line_id.partner_id', '=', self.id)])

    def compute_late_returns(self):
        '''compute total count of late returns'''
        for record in self:
            record.late_return = self.env['checkout'].search_count([('partner_id','=',self.id),('is_late_return','=',True)])

    def compute_penalty(self):
        '''calculate the total penalty of the customer '''
        for record in self:
            # record.penalty = 10
            penalty1 = self.env['checkout'].search([('partner_id','=',record.id)])
            penalty2 = penalty1.mapped('penalty')
            record.penalty = sum(map(int,penalty2))
    def action_view_checkout_history(self):
        """smart button for checkout history of each customer"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "book.line",
            "name": "checkout history",
            "views": [[False, "list"], [False, "form"]],
            "domain": [('book_line_id.partner_id', '=', self.id)],
        }


    def action_view_due_date_history(self):
        '''smart button for due date history of each customer'''
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "checkout",
            "name": "overdue history",
            "views": [[False, "list"], [False, "form"]],
            "domain": [('partner_id','=',self.id),('is_late_return','=',True)],
            "target":"current"
        }
    def action_view_penalty(self):
        '''penalty'''
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "checkout",
            "name": "overdue history",
            "views": [[False, "list"], [False, "form"]],
            "domain": [('partner_id','=',self.id),('is_late_return','=',True)],
            "target":"current"
        }



