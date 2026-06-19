{
    'name': 'Hospital Appointment & Patient Management System',
    'depends': ['base','product','hr'],
    'version':'1.0',
    'application': True,
    'data': [
        'views/hospital_patient_views.xml',
        'security/ir.model.access.csv',
        'views/hospital_department_views.xml',
        'views/hospital_appointment_views.xml',
        'views/hospital_prescription_line_views.xml',
        'data/ir_sequence_data.xml',
        'views/hr_employee_views.xml',
        'views/hospital_menu.xml',
    ]
}
