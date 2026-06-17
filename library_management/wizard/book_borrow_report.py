# -*- coding: utf-8 -*-
import io
from odoo import api,fields,models,_
from datetime import datetime, date
from odoo.tools import date_utils, json_default
import json
from dateutil.rrule import rrule, DAILY
from odoo.exceptions import ValidationError
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class BookBorrowReport(models.TransientModel):
     _name = 'book.borrow.report'
     _description = 'book borrow report'


     member_id = fields.Many2one('res.partner',string="member")
     from_date = fields.Date(string="from date")
     to_date = fields.Date(string="to date")
     book_name_id = fields.Many2one('books',string="books")
     book_genres_id = fields.Many2one('genres',string="book genres")
     sorting_option = fields.Selection([('issued_date','Checkout date'),('due_date','Due dates')])
     sorted_by = fields.Selection([('ASC','Ascending order'),('DESC','Descending order')])


     def confirm_pdf_report(self):
          list = []
          query = """select reference_id,p1.name as member_name,a1.name as auther_name,b1.books_name as book_name,g1.name as genres_name,due_date,issued_date,return_date from checkout as ch
                 inner join res_partner as p1 on p1.id = ch.partner_id
				 inner join book_line as bl on bl.book_line_id = ch.id
				 inner join books as b1 on b1.id = bl.books_id
				 left join authors as a1 on a1.id = b1.book_authors_id
			   	 inner join books_genres_rel as bg on bg.books_id = b1.id
				 left join genres as g1 on g1.id = bg.genres_id where 1=1
		  	 """
          if self.member_id:
               query +="AND p1.id = %s "
               list.append(self.member_id.id)
               print(list)
          if self.book_name_id:
               query += "AND b1.id = %s"
               list.append(self.book_name_id.id)
               print(list)
          if self.from_date:
               query += """ AND Date(return_date) >= %s and Date(return_date) <= %s"""
               list.append(self.from_date)
               list.append(self.to_date)
          if self.book_genres_id:
               query += "AND g1.id = %s"
               list.append(self.book_genres_id.id)
          if self.sorting_option:
               query += f"ORDER BY {self.sorting_option} {self.sorted_by}"


          self.env.cr.execute(query,tuple(list)),
          report = self.env.cr.dictfetchall()
          names = []
          books = []
          genres = []
          for record in report:
               if record['member_name'] not in names:
                    names.append(record['member_name'])
          for record in report:
               if record['book_name'] not in books:
                    books.append(record['book_name'])
          for record in report:
               if record['genres_name'] not in genres:
                    genres.append(record['genres_name'])
          data = {'report': report,'names':names,'len_name':len(names),'books':books,'len_books':len(books),'genres':genres,'len_genres':len(genres)}

          return self.env.ref('library_management.action_report_book_borrow_form').report_action(None, data=data)


     def confirm_xlsx_report(self):
          """
          Returns report action for the XLSX Attendance report
          Raises: ValidationError: if From Date > To Date
          Raises: ValidationError: if there is no attendance records
          Returns:
              dict:  the XLSX report action
          """
          data = {
               'member_id':self.member_id.id,
               'from_date': self.from_date,
               'to_date': self.to_date,
               'book_name_id': self.book_name_id.id,
               'book_genres_id':self.book_genres_id.id,
               'sorting_option':self.sorting_option,
               'sorted_by':self.sorted_by
          }
          print("data",data)
          return {
               'type': 'ir.actions.report',
               'data': {'model': 'book.borrow.report',
                        'options': json.dumps(data, default=json_default),
                        'output_format': 'xlsx',
                        'report_name': 'book report',
                        },
               'report_type': 'xlsx',
          }

     def get_xlsx_report(self, data, response):

          query = """select reference_id,p1.name as member_name,a1.name as auther_name,b1.books_name as book_name,b1.book_id as isbn,g1.name as genres_name,due_date,issued_date,return_date from checkout as ch
                           inner join res_partner as p1 on p1.id = ch.partner_id
          				 inner join book_line as bl on bl.book_line_id = ch.id
          				 inner join books as b1 on b1.id = bl.books_id
          				 left join authors as a1 on a1.id = b1.book_authors_id
          			   	 inner join books_genres_rel as bg on bg.books_id = b1.id
          				 left join genres as g1 on g1.id = bg.genres_id where 1=1
          		  	 """
          list = []
          if data['member_id']:
               query += "AND p1.id = %s"
               list.append(data['member_id'])
          if data['book_name_id']:
               query += "AND b1.id = %s"
               list.append(data['book_name_id'])
          if data['from_date']:
               query += """ AND Date(return_date) >= %s and Date(return_date) <= %s"""
               list.append(data['from_date'])
               list.append(data['to_date'])
          if data['book_genres_id']:
               query += "AND g1.id = %s"
               list.append(data['book_genres_id'])
          if data['sorting_option']:
               query += f"ORDER BY {data['sorting_option']} {data['sorted_by']}"

          self.env.cr.execute(query,tuple(list))
          docs = self.env.cr.dictfetchall()
          print(docs)
          names = []
          books = []
          genres = []
          for record in docs:
               if record['member_name'] not in names:
                    names.append(record['member_name'])
          for record in docs:
               if record['book_name'] not in books:
                    books.append(record['book_name'])
          for record in docs:
               if record['genres_name'] not in genres:
                    genres.append(record['genres_name'])
          output = io.BytesIO()
          workbook = xlsxwriter.Workbook(output, {'in_memory': True})
          sheet = workbook.add_worksheet('docs')

          border = workbook.add_format({'border': 1})
          head = workbook.add_format(
               {'bold': True, 'font_size': 20, 'align': 'center'})
          subhead = workbook.add_format({'align':'center','bold':True,'font_size': 12,'border':1})
          date_size = workbook.add_format(
               {'font_size': 12, 'align': 'center','border':1})
          sheet.merge_range('C1:K3', 'Library Management', head)
          sheet.set_column(1, 1, 15)
          sheet.set_column(2, 2, 20)
          sheet.set_column(3, 3, 25)
          sheet.set_column(4, 4, 15)
          sheet.set_column(5, 5, 20)
          sheet.set_column(6, 6, 20)
          sheet.set_column(7, 7, 20)
          sheet.set_column(8, 8, 20)
          sheet.set_column(9,9,20)
          if len(names)==1:
               sheet.write(4,1,'Member name:',subhead)
               sheet.write(4, 2,names[0], date_size)
          if len(books)==1:
               sheet.write(5, 1, 'books name', subhead)
               sheet.write(5, 2, books[0], date_size)
          if len(genres) == 1:
               sheet.write(6, 1, 'genres', subhead)
               sheet.write(6, 2, genres[0], date_size)

          col=1
          sheet.write(8, col, 'Reference no',subhead)
          col=col+1
          if len(names)!=1:
               sheet.write(8,col,'member name',subhead)
               col = col + 1
          if len(books) != 1:
               sheet.write(8, col, 'books name', subhead)
               col = col + 1
          if len(genres) != 1:
               sheet.write(8, col, 'Genres', subhead)
               col = col + 1
          sheet.write(8, col, 'ISBN NO', subhead)
          col = col + 1
          sheet.write(8, col, 'Author name', subhead)
          col = col + 1
          sheet.write(8, col, 'Checkout date', subhead)
          col=col+1
          sheet.write(8, col, 'return date', subhead)

          row = 9

          for rec in docs:
               checkout_date = rec['issued_date']
               return_date = rec['return_date']
               print(type(checkout_date))
               col=1
               sheet.write(row,col,rec['reference_id'],date_size)
               col+=1
               if len(names)!=1:
                    sheet.write(row,col,rec['member_name'],date_size)
                    col += 1
               if len(books) != 1:
                    sheet.write(row,col,rec['book_name'],date_size)
                    col += 1
               if len(genres) != 1:
                    sheet.write(row, col, rec['genres_name'], date_size)
                    col += 1
               sheet.write(row, col, rec['isbn'], date_size)
               col += 1
               sheet.write(row,col,rec['auther_name'],date_size)
               col += 1
               if checkout_date is not None:
                    sheet.write(row, col,checkout_date.strftime('%Y-%m-%d'), date_size)
                    col += 1
               if return_date is not None:
                    sheet.write(row, col,return_date.strftime('%Y-%m-%d'), date_size)
               row=row+1

          workbook.close()
          output.seek(0)
          response.stream.write(output.read())
          output.close()