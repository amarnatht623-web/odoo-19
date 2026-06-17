# -*- coding: utf-8 -*-
from odoo import fields,  models
class FormAttachment(models.Model):
   _name = 'form.attachment'
   _description = 'Form Attachment'
   name = fields.Char(string='Description', required=True)
   attachment = fields.Binary(string='Attachment', required=True)
   attachment_filename = fields.Char(string='Attachment Filename')
