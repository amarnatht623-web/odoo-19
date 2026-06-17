{
    'name': 'library management',
    'depends': ['base','sales_team','contacts','account','stock'],
    'version':'1.0',
    'application': True,
    'data': [
             'security/library_security_groups.xml',
             'report/book_borrow_report_template.xml',
             'report/book_borrow_report.xml',
             'data/ir_cron_data.xml',
             'data/mail.template_model.xml',
             'data/producct_demo.xml',
             'view/books_views.xml',
             'security/ir.model.access.csv',
             'view/authors_views.xml',
             'view/publishers_views.xml',
             'view/genres_view.xml',
             'view/checkout_views.xml',
             'data/ir_sequence_data.xml',
             'data/library_genres_demo.xml',
             'view/res_config_settings_views.xml',
             'view/book_line_views.xml',
             'wizard/book_checkout_wizard_views.xml',
             'view/res_partner.xml',
             'wizard/book_borrrow_report_views.xml',
             'view/donation_form.xml',
             'view/form_attachment_views.xml',
             'view/custom_portal_template_views.xml',
             'view/book_menu.xml',
             ],
    'assets':{
        'web.assets_backend':[
            'library_management/static/src/js/book_report.js'
        ]
    }
    # 'qweb': [
    #          'view/res_partner.xml',
    #          ],
}
