from django.db import models
import re
import logging

# pattern = re.compile(r'(.*)[\/ \.]([0-9]+) [. ]*[\[\]0-9\-–]*\[[A-Z ]*([0-9]+)\] *$')
pattern = re.compile(r'(\w+) (.+) (\[+[A-Za-z0-9-\[\][]*[ -]* *[0-9]+\]+)')

book_vol_lookup = {
    "Amp": 6,
    "Ashmole": 9,
    "BC": 6,
    "Bham": 15,
    "BL": 5,
    "BMaz": 7,
    "BN": 7,
    "BodL": 12,
    "Brogyntyn": 14,
    "BSteG": 7,
    "Caius": 17,
    "CCCC": 20,
    "CFM": 18,
    "Chetham's": 2,
    "Cph": 10,
    "CUL": 19,
    "Digby": 3,
    "Douce": 4,
    "EL": 1,
    "Fitz": 18,
    "Glo": 15,
    "Hfd": 15,
    "HM": 1,
    "HU": 1,
    "Huseby": 10,
    "Lambeth": 13,
    "Laud": 16,
    "LD": 6,
    "Lei": 15,
    "Lich": 15,
    "Llanstephan" : 14,
    "McC": 18,
    "NLW": 14,
    "Not": 15,
    "NY": 6,
    "Oxf": 8,
    "Pem": 18,
    "Peniarth": 14,
    "Ptb": 15,
    "RCDCA": 6,
    "Ripon": 6,
    "Rylands": 2,
    "Schøyen": 10,
    "Shf": 6,
    "Sion": 13,
    "Sotheby": 14,
    "Stockh": 10,
    "Swl": 15,
    "Trefeglwys": 14,
    "Trinity": 11,
    "Uppsala": 10,
    "Wor": 15,
    "York": 6,
    "e": 21,
    "Hatton": 21,
    "Sidney": 22,
    "TrinHall": 22,
    "Christ's": 22,
    "P'house": 22,
    "Emma": 22,
    "Jesus": 22,
    "Selwyn": 22,
    "Rawl": 23
}


def get_book_from_name(input_name=''):
    name = str.strip(input_name)
    if name.__len__() > 0:
        '''ignore pattern, just split on first space '''
        bk_sort_text = name.split(' ')[0]
        imep_vol = book_vol_lookup.get(bk_sort_text)
        if not imep_vol:
            imep_vol = 999
        return Book.objects.get_or_create(book_name=input_name,
                                          book_sort_text=bk_sort_text.lower(),
                                          # book_num=bk_num,
                                          book_vol=imep_vol)


# Create your models here.
class Book(models.Model):
    def __str__(self):
        return self.book_name

    book_name = models.CharField(max_length=255, default='')
    book_sort_text = models.CharField(max_length=255, default='')
    # book_num = models.IntegerField(default=0)
    book_vol = models.IntegerField(default=0)

    class Meta:
        ordering=('book_sort_text', 'book_name', 'book_vol')


class Prose(models.Model):
    # ...
    def __str__(self):
        return self.prose_text

    def get_absolute_url(self):
        return '/proses/%i/' % self.id

    prose_text = models.CharField(max_length=500)
    prose_text_sort = models.CharField(max_length=500)
    type = models.CharField(max_length=20, default='explicits')
    printed = models.BooleanField(default=False)

    class Meta:
        ordering = ['prose_text_sort', ]


class ProseBook(models.Model):
    def __str__(self):
        return self.prose.prose_text + ' ' + self.book.book_name + ' ' + str(self.volume)

    prose = models.ForeignKey(Prose, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    volume = models.IntegerField(default=0)

    class Meta:
        ordering = ['prose__prose_text_sort', 'book__book_sort_text', 'book__book_name' ]


