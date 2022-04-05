import xlrd
from django.core.management.base import BaseCommand
from xlrd import XLRDError
from proses.models import *
from proses.import_file import *


class Command(BaseCommand):
    help = 'Import file: type=explicit|incipit|subject|title -f --file <filename>'

    def add_arguments(self, parser):
        parser.add_argument('type', type=str, help='explicit|incipit|subject|title')
        parser.add_argument('-f', '--file', type=str, help='Name of file to import', )

    def handle(self, *args, **kwargs):
        upload_type = kwargs['type']
        filename = kwargs['file']
        f = open(filename, "rb")
        file_content= f.read()
        import_file_content(filename, file_content, upload_type)
