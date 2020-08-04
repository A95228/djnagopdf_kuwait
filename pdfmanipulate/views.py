from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from pdfrw import PdfReader, PdfWriter, IndirectPdfDict
from django.core.files.base import ContentFile
from django.http import FileResponse
import io
import os

class HomePageView(TemplateView):
    template_name = 'Home/home.html'


def ProcessView(request):
    if request.method == 'POST':
        # name = request.FILES['origin_file']
        origin_file = request.FILES['origin_file']
        # save_as = request.FILES['save_as']
        page_index = request.POST['page_index']
        add_file = request.FILES['add_file']
        print('---------start----------',page_index)
        response=process(origin_file, add_file,int(page_index)-1, 'subset.pdf')
        print('-----------end--------',response)

    # concatenate(paths=origin_file,output=origin_file)
    with open('subset.pdf', "rb") as f:
        data = f.read()
        response = HttpResponse(data, content_type = 'application/pdf')
        response['Content-Length'] = os.path.getsize('subset.pdf')
        response['Content-Disposition'] = 'attachment; filename=%s' % 'subset.pdf'
        return response


    # return HttpResponse(data, content_type='application/pdf')


def process(origin_file,add_file, number_of_pages, output):
    origin_file_obj = PdfReader(origin_file)
    add_file_obj = PdfReader(add_file)


    total_pages_add = len(add_file_obj.pages)
    print('---------total_pages_add----------',total_pages_add)

    total_pages_origin = len(origin_file_obj.pages)
    print('---------total_pages_origin----------', total_pages_origin)


    sub_pages_origin =len(origin_file_obj.pages)-number_of_pages
    print('---------sub_pages_origin----------', sub_pages_origin)

    writer = PdfWriter()

    for page in range(number_of_pages):
        if page <= total_pages_origin:
            writer.addpage(origin_file_obj.pages[page])

    for page in range(total_pages_add):
        if page <= total_pages_add:
            writer.addpage(add_file_obj.pages[page])

    for page in range(sub_pages_origin):
        if page <= sub_pages_origin:
            # print(page+number_of_pages)
            writer.addpage(origin_file_obj.pages[page+number_of_pages])

    writer.write(output)
    # return writer