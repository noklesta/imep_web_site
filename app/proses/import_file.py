import xlrd
import logging
from xlrd import XLRDError
from .models import *


def import_file_content(filename, contents, upload_type):
    book = xlrd.open_workbook(file_contents=contents, filename=filename, formatting_info=1)
    fonts = book.font_list
    for sheet in book.sheets():
        n_rows = sheet.nrows
        n_cols = sheet.ncols
        if n_cols >= 3:
            for row in range(0, n_rows - 1):
                try:
                    prose_text = sheet.cell(row, 0).value
                    xf = book.xf_list[sheet.cell_xf_index(row, 0)]
                    printed_italic = fonts[xf.font_index].italic
                    if prose_text:
                        book_name_text = sheet.cell(row, 1).value
                        if book_name_text:
                            book_names = book_name_text.split(sep=';')
                            vol = sheet.cell(row, 2).value
                            if vol:
                                v = int(sheet.cell(row, 2).value)
                                for bn in book_names:
                                    bk = get_book_from_name(bn)

                                    if bk:
                                        prs = Prose.objects.get_or_create(prose_text=prose_text,
                                                                          prose_text_sort=prose_text.strip("'"),
                                                                          type=upload_type,
                                                                          printed=printed_italic,
                                                                          )
                                        pr = prs[0]
                                        queryset = ProseBook.objects.filter(
                                            prose__type=upload_type,
                                            prose__prose_text=prose_text,
                                            prose__prosebook__book__book_name=bn,
                                        )
                                        if queryset.count() == 0:
                                            ProseBook.objects.create(prose=pr, book=bk[0], volume=bk[0].book_vol)
                except XLRDError as err:
                    logging.getLogger('appname').warning(msg=err.__str__() + prose_text)


def import_file(contents, upload_type):
    book = xlrd.open_workbook(file_contents=contents)
    for sheet in book.sheets():
        n_rows = sheet.nrows
        n_cols = sheet.ncols
        if n_cols >= 3:
            for row in range(0, n_rows - 1):
                try:
                    prose_text = sheet.cell(row, 0).value
                    if prose_text:
                        book_name_text = sheet.cell(row, 1).value
                        if book_name_text:
                            book_names = book_name_text.split(sep=';')
                            vol = sheet.cell(row, 2).value
                            if vol:
                                v = int(sheet.cell(row, 2).value)
                                for bn in book_names:
                                    bk = get_book_from_name(bn)
                                    if bk:
                                        prs = Prose.objects.get_or_create(prose_text=prose_text,
                                                                          type=upload_type)
                                        pr = prs[0]
                                        queryset = ProseBook.objects.filter(
                                            prose__type=upload_type,
                                            prose__prose_text=prose_text,
                                            prose__prosebook__book__book_name=bn)
                                        if queryset.count() == 0:
                                            ProseBook.objects.create(prose=pr, book=bk[0], volume=v)
                except XLRDError as err:
                    logging.getLogger('appname').warning(msg=err.__str__() + prose_text)
