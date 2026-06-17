# -*- coding: utf-8 -*-
from email.policy import default

from odoo import fields,models

class ResConfigSettings(models.TransientModel):
    '''all fields related to ResConfigSettings'''
    _inherit = 'res.config.settings'
    # _description = 'Settings'

    borrowing_book_days = fields.Integer(string="borrowing days",config_parameter='checkout.due_date')
    hourly_penalty = fields.Integer(string='Hourly penalty',config_parameter='checkout.penalty')
    reminder_days = fields.Char(string="Reminder days",store=True,config_parameter='checkout.days_reminder')
    max_book = fields.Integer(String="maximum books",config_parameter='res_partner.book_max')
    max_late_returns = fields.Integer(string="maximum  returns",config_parameter='checkout.maximum_late_returns',store=True)
