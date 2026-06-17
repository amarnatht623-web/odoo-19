from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

class CustomModel(CustomerPortal):

    @http.route( ['/my/donations'],type='http',auth='user',website=True)
    def portal_my_donations(self, **kw):

        books = request.env['books'].sudo().search([
            ('create_uid', '=', request.env.user.id)
        ])

        return request.render(
            'library_management.portal_my_donations',
            {
                'books': books,
            }
        )

    @http.route(['/my/donations/<int:book_id>'],type='http',auth='user',website=True )
    def portal_donation_detail(self, book_id, **kw):
        book = request.env['books'].sudo().browse(book_id)
        return request.render(
            'library_management.portal_donation_detail',
            {
                'book': book,
            }
        )











    # def _prepare_home_portal_values(self, counters):
    #     values = super()._prepare_home_portal_values(counters)
    #
    #     values['donation_count'] = request.env['books'].sudo().search_count([
    #         ('create_uid', '=', request.env.user.id)
    #     ])
    #     print(request.env['books'].sudo().search_count([
    #         ('create_uid', '=', request.env.user.id)
    #     ]))
    #     return values
