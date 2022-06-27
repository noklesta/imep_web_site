from urllib.parse import quote
from django import forms
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from django.views import generic
from django_tables2 import RequestConfig
from django.db.models import Q

import requests

from .import_file import *
from .tables import *

UPLOAD_TYPES = [
    ('explicit', 'Explicits, Books and Volumes'),
    ('incipit', 'Incipits, Books and Volumes'),
    ('subject', 'General Index'),
    ('title', 'Titles, Rubrics and Colophons'),

]

VIEW_TYPES = {'explicit': 'Reverse Explicits',
              'incipit': 'Incipits',
              'subject': 'General Index',
              'title': 'Titles, Rubrics and Colophons',
              }


def index(request):
    num_explicits = Prose.objects.filter(type='explicit').count()
    num_incipits = Prose.objects.filter(type='incipit').count()
    num_subjects = Prose.objects.filter(type='subject').count()
    num_titles = Prose.objects.filter(type='title').count()
    return render(request, 'proses/index.html', {'num_explicits': num_explicits,
                                                 'num_incipits': num_incipits,
                                                 'num_subjects': num_subjects,
                                                 'num_titles': num_titles,
                                                 "index_home":"active"})


class DetailView(generic.DetailView):
    model = Prose
    template_name = 'proses/detail.html'


class UploadFileForm(forms.Form):
    file = forms.FileField()
    type = forms.CharField(label='Type of file', widget=forms.Select(choices=UPLOAD_TYPES))


def prose_table(request):
    name = request.resolver_match.url_name
    breadcrumbs = {}
    breadcrumbs[0] = dict(name=VIEW_TYPES[name], url=request.path)

    if 'query' in request.GET:
        search_val = request.GET['query']
    else:
        search_val = None

    if search_val and len(search_val)>0:
        response = requests.get('https://tekstlab.uio.no/imep_search', params={'query': search_val})
        fuzzy_search_ids = response.text.split(',')
        pbs = ProseBook.objects.filter(Q(prose__type=name, prose__prose_text__iregex=search_val.strip()) | Q(prose__type=name, prose_id__in=fuzzy_search_ids))

        breadcrumbs[1] = dict(name='Query: ' + search_val, url=request.path + '?query=' + search_val)
    else:
        pbs = ProseBook.objects.filter(prose__type=name)
        search_val = None

    if name == 'incipit':
        table = IncipitsTable(pbs)
    elif name == 'explicit':
        table = ExcipitsTable(pbs)
    elif name == 'title':
        table = TitlesTable(pbs)
    elif name == 'subject':
        table = GeneralIndexTable(pbs)

    RequestConfig(request, paginate={'per_page': 25}).configure(table)
    return render(request, 'proses/mytable.html',
                  {'site_name': VIEW_TYPES[name],
                   'table_name':
                       '' if search_val is None else
                       'Found ' + str(pbs.count()) + ' ' + VIEW_TYPES[name] + ' containing: ' + search_val,
                   'table': table,
                   'breadcrumbs': breadcrumbs,
                   'query_text': "" if search_val is None else search_val,
                   name : "active"}
                    )


def search(request):
    if 'query' in request.GET:
        message = 'You searched for: %r' % request.GET['query']
    else:
        message = 'Please enter text to search for.'
    return HttpResponse(message)


def volume_index(request):
    template_name = 'proses/volume_index.html'
    return render(request, template_name)


def import_sheet(request):
    if request.method == "POST":

        form = UploadFileForm(request.POST,
                              request.FILES)
        if form.is_valid():
            upload_type = form.cleaned_data['type']
            file_handle = request.FILES['file']
            import_file_content(file_handle.name, file_handle.file.read(), upload_type)
            return HttpResponse("OK")
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        'proses/upload_form.html',
        {'form': form})