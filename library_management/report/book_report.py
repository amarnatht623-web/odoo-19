from odoo import models,api
class BookReport(models.AbstractModel):
    _name = 'report.library_management.form_book_borrow_report'
    @api.model
    def _get_report_values(self, docids, data=None):
        print("hdhdhd")
        print("hhd")
        print(data['names'])
        print(data['len_name'])
        print(data)
        return {
            'doc_ids': docids,
            'data': data['report']

        }

