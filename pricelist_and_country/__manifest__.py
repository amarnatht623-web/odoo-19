{
    'name': 'pricelist and country',
    'depends': ['base','sale_management'],
    'version':'1.0',
    'application': True,
    'data': [
             'views/sale_order_view.xml',
             'views/sale_menus.xml',
             'security/ir.model.access.csv']
}