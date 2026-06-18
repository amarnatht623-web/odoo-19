from odoo import fields, models, api,_
from datetime import timedelta, date,datetime

from odoo.exceptions import ValidationError,UserError
from odoo.orm.decorators import onchange


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _rec_name = 'ref_no'

    patient_id = fields.Many2one('hospital.patient',string="patient name")
    ref_no = fields.Char("reference no", default=lambda self: _('New'),copy=False,readonly=True)
    appointment_datetime = fields.Datetime(string="appointment date",required=True)
    consultation_fee = fields.Float()
    doctor_id = fields.Many2one('hr.employee','doctor name')
    dept_doctor_ids = fields.Many2many('hr.employee',string="doctor name")
    department_id = fields.Many2one('hospital.department',string="department")
    symptoms = fields.Text()
    diagnosis = fields.Text()
    prescription_ids = fields.One2many('hospital.prescription.line',string="prescription",inverse_name='appointment_id')
    medicine_total = fields.Float(compute="compute_medicine_total",store=True)
    total_bill = fields.Float(compute="compute_total_bill",store=True)

    state = fields.Selection([('Draft','Draft'),('Scheduled','Scheduled'),('Consultation','Consultation'),('Completed','Completed'),('Cancelled','Cancelled')],copy=False,required=True,default='Draft')

    @api.model_create_multi
    def create(self, vals_list):
        '''sequence number generation'''
        for vals in vals_list:
            if vals.get('ref_no', _("New")) == _("New"):
                vals['ref_no'] = self.env['ir.sequence'].next_by_code(
                    'hospital.appointment')
                print(vals['ref_no'])
        return super().create(vals_list)

    @api.onchange('appointment_datetime')
    def show_warning_date_time(self):
        for rec in self:
            today = datetime.today()

            if type(rec.appointment_datetime) != bool:
                if date.today() > rec.appointment_datetime.date():
                    raise ValidationError('please enter correct date and time')
                else:
                    pass
            else:
                pass
        # duplicate = self.search([])
        # print("u",duplicate)

    @api.onchange('department_id')
    def filter_doctor(self):
        if self.department_id:
            doc = self.env['hospital.department'].search([('id','=',self.department_id)])

            self.dept_doctor_ids = doc.doctor_ids

        else:
            self.dept_doctor_ids = False

    @api.constrains('patient_id','appointment_datetime')
    def prevent_multiple_appointments(self):
        for rec in self:
            duplicate = self.search(['&',('id','!=',rec.id),('patient_id','=',rec.patient_id),('appointment_datetime','=',rec.appointment_datetime)])

            if  duplicate:
                raise ValidationError('check your date and time')


    @api.constrains('doctor_id','appointment_datetime')
    def prevent_overlap_doctor(self):
        for rec in self:
            duplicate=self.search(['&',('id','!=',rec.id),('doctor_id','=',rec.doctor_id),('appointment_datetime','=',rec.appointment_datetime)])

            if duplicate:
                raise ValidationError('overlapping appointments!! check your date and time')
    @api.ondelete(at_uninstall=False)
    def prevent_deletion(self):
        for rec in self:
            if rec.state == 'Completed':
                raise UserError(_("you can't delete this record"))



    def Schedule_confirm(self):
        self.write(({
            'state':'Scheduled'
        }))
    def start_consultation(self):
        for rec in self:
            if not  rec.patient_id or  not rec.doctor_id:
                raise ValidationError(' please select patient and doctor')
        self.write({
            'state':'Consultation'
        })
    def complete_consultation(self):
        for rec in self:
            if not rec.diagnosis or not rec.prescription_ids:
                raise ValidationError("diagnosis and prescription must be required")
        self.write({
            'state':'Completed'
        })
    def cancel_appointment(self):
        self.write({
            'state':'Cancelled'
        })
    @api.depends('prescription_ids.quantity','prescription_ids.unit_price')
    def compute_medicine_total(self):

        total=0
        for rec in self.prescription_ids:
            qty = rec.quantity
            unit_price =rec.unit_price
            total += qty*unit_price

        self.medicine_total = total

    @api.depends('consultation_fee','medicine_total')
    def compute_total_bill(self):
        for rec in self:
            rec.total_bill = rec.consultation_fee + rec.medicine_total
