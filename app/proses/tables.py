import django_tables2 as tables
from .models import ProseBook
from django.db.models import F, Func
import re


class ProseTable(tables.Table):

    def get_col_name(self):
        return 'Proses'

    @staticmethod
    def order_prose_text(query_set, is_descending):
        query_set = query_set.annotate(
            field_lower=Func(F('prose_text ').strip("'"), function='LOWER')
        ).order_by(('-' if is_descending else '') + 'field_lower')
        return query_set, True

    prose = tables.Column(verbose_name='Proses', order_by='prose_text')
    book = tables.Column(verbose_name='MS and Item no.')
    volume = tables.Column(
        verbose_name="IMEP volume",
        attrs={
            "td": {"align": "center", 'style': 'text-align: center'}
        }
    )

    class Meta:
        model = ProseBook
        template_name = 'django_tables2/bootstrap4.html'
        exclude = {'id'}


class IncipitsTable(ProseTable):
    def get_col_name(self):
        return 'Incipits'

    prose = tables.Column(verbose_name='Incipit', )


class ExcipitsTable(ProseTable):
    prose = tables.Column(
        verbose_name="Reverse Explicit",
        attrs={
            "td": {"align": "right", 'style': 'text-align: right'}
        }
    )


class RubriksTable(ProseTable):
    prose = tables.Column(
        verbose_name="Rubriks",
        attrs={
            "td": {"align": "right", 'style': 'text-align: right'}
        }
    )


class TitlesTable(ProseTable):
    prose = tables.Column(
        verbose_name="Titles",
        attrs={
            "td": {"class": "campl-col-title",
                   'is-printed': lambda record: record.prose.printed},
            'col-name': 'title'
        }
    )

    @staticmethod
    def render_prose(record):
        return record.prose.prose_text

    class Meta:
        model = ProseBook
        template_name = 'django_tables2/bootstrap4.html'
        exclude = {'id'}


class GeneralIndexTable(ProseTable):
    prose = tables.Column(
        verbose_name="Text",
        attrs={
            "td": {"align": "right", 'style': 'text-align: right'}
        }
    )
