{
    'name': 'customer_product',
    'depends': ['base','contacts','sale_management'],
    'version':'1.0',
    'application': True,
    'data': [
           'views/res_partner_views.xml',
           'views/product_template_views.xml'
    ]
}