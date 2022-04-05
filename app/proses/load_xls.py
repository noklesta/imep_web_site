from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def add_argument(self, parser):
        parser.add_argument('xls_file', nargs='+', type=str)
