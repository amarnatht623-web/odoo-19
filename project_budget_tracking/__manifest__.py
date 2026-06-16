{
    'name': 'project budget tracking',
    'depends': ['base','project','hr_timesheet'],
    'version':'1.0',
    'application': True,
    'data': [
        'views/project_task_views.xml',
        'data/project_mail_template.xml',
        'data/ir_cron_data.xml'
             ]
}