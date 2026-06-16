{
    'name': 'sales customers',
    'depends': ['base','sale_management'],
    'version':'1.0',
    'application': True,
    'data': [
             'views/res_config_settings_views.xml',
             'views/sale_order_views.xml'
             ]
}