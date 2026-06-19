{
    'name': 'invoice order',
    'depends': ['base','sale_management'],
    'version':'1.0',
    'application': True,
    'data': [
        'views/account_move_views.xml',
        'views/res_partner_views.xml',
        'data/ir_sequence_data.xml'
    ]
}