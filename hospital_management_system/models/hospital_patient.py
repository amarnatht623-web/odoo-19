from dateutil.relativedelta import relativedelta

from odoo import fields, models, api
from datetime import timedelta, date
from odoo.orm.fields_temporal import Date


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _rec_name = 'name'

    name = fields.Char(string="patient name")
    date_of_birth = fields.Date(string="Date of birth")
    age = fields.Integer(string="Age",compute="compute_age",store=True)
    gender = fields.Selection([('Male','Male'),('Female','Female'),('Others','Others')])
    blood_group = fields.Selection([('A+','A+'),('B+','B+'),('O+','O+'),('A-','A-'),('B-','B-'),('O-','O-')])
    mobile = fields.Char("Mobile no")
    department_id = fields.Many2one("hospital.department",string="department")
    appointment_ids = fields.One2many('hospital.appointment',inverse_name="patient_id")
    draft = fields.Selection([('Draft','Draft'),('Active','Active'),('Discharge','Discharge')],string="Draft",compute="change_to_discharge",store=True)
    appointment_count = fields.Integer(string="appointment count",compute="compute_appointment_count",store=True)
    treatment_progress = fields.Float(string="treatment progress",compute="compute_treatment_progress",store=True)

    @api.depends('appointment_ids')
    def compute_appointment_count(self):
        print("hi")
        for rec in self:
            rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id','=',rec.id)])
            print(rec.appointment_count)
            print(rec.date_of_birth)

    @api.depends('date_of_birth')
    def compute_age(self):
        for rec in self:
            print("f")
            if type(rec.date_of_birth) != bool:
                today = date.today()
                rec.age = today.year - rec.date_of_birth.year
                print(rec.age)

    @api.depends('appointment_count','appointment_ids.state')
    def compute_treatment_progress(self):
        for rec in self:
            completed = self.env['hospital.appointment'].search_count(['&',('state','=','Completed'),('patient_id','=',rec.id)])
            print("g",completed)
            if completed != 0 and rec.appointment_count != 0:
                rec.treatment_progress = (completed/rec.appointment_count)*100

    @api.depends('appointment_ids.state')
    def change_to_discharge(self):
        for rec in self.appointment_ids:
            if rec.state == 'Completed':
                self.write({
                    'draft':'Discharge'
                })


