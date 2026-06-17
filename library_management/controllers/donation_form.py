from odoo import http
from odoo.http import request
import base64


class DonationForm(http.Controller):
    @http.route('/website/donation/form', type='http', auth='public', website=True)
    def customer_form(self, **kw):
        """Render the customer creation form"""
        author_name = request.env['authors'].sudo().search([])
        print(author_name)
        book_status = request.env['books'].sudo().search([])

        return request.render('library_management.donation_form_customer',{'author_name':author_name,'book_status':book_status})
    @http.route('/website/donation/create', type='http', auth='public', methods=['POST'], website=True, csrf=True)
    def create_customer(self, **post):
        print(post)
        """Handle form submission and create a new customer"""
        books_name = post.get('books_name')
        book_description = post.get('book_description')
        author_name = post.get('author_name')
        book_status = post.get('book_status')
        attachment = request.httprequest.files.getlist('book_image_att')
        if not books_name:
            # If name is missing, redirect back to form with an error message
            return request.render('library_management.donation_form_customer', {
                'error': 'Name is required!'
            })
        request.env['books'].sudo().create({
            'books_name': books_name,
            'book_description':book_description,
            'book_authors_id':author_name,
            'book_status':book_status,
    })
        return request.render('library_management.donation_success_template')
