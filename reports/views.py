import csv
from django.utils.dateparse import parse_date
from django.shortcuts import get_object_or_404
from reports.forms import ReportForm
from django.http import JsonResponse
from reports.utils import get_rep_image_path
from profiles.models import Profile
from reports.models import Report
from sales.models import Sale, Position, CSV
from products.models import Product
from customers.models import Customer
from django.views.generic import ListView, DetailView, TemplateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Generating pdf libraries and imports
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = "reports/main.html"
    context_object_name = 'reports'

class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = "reports/detail.html"
    context_object_name = 'report'


class UploadTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/from_file.html'

@login_required
def csv_upload(request):
    
    if request.method == 'POST':
        file_name = request.FILES.get('file').name
        csv_file = request.FILES.get('file')
        csv_obj, created = CSV.objects.get_or_create(file_name=file_name)

        if created:
            csv_obj.csv_file = csv_file
            csv_obj.save()

            with open(csv_obj.csv_file.path, 'r') as f:
                reader = csv.reader(f)
                reader.__next__()

                for row in reader:
                    transaction_id = row[1]
                    product = row[2]
                    quantity = int(row[3])
                    customer = row[4]
                    date = parse_date(row[5])

                    #Find product
                    try:
                        product_obj = Product.objects.get(name__iexact=product)
                    except Product.DoesNotExist:
                        product_obj = None

                    if product_obj is not None:
                        customer_obj, _ = Customer.objects.get_or_create(name=customer)
                        salesman_obj = Profile.objects.get(user=request.user)
                        position_obj = Position.objects.create(
                            product=product_obj,
                            quantity=quantity,
                            created=date
                        )

                        sale_obj, _ = Sale.objects.get_or_create(
                            transaction_id=transaction_id,
                            customer=customer_obj,
                            salesman=salesman_obj,
                            created=date
                        )
                        sale_obj.positions.add(position_obj)
                        sale_obj.save()
                return JsonResponse({'exist': False})
        else:
            return JsonResponse({'exist': True})
    return JsonResponse({})

@login_required
def create_report(request):
    if request.is_ajax():
        img = request.POST.get('image')
        image = get_rep_image_path(img)
        form = ReportForm(request.POST)
        if form.is_valid():
            profile = Profile.objects.get(user=request.user)
            instance = form.save(commit=False)
            instance.image = image
            instance.author = profile
            instance.save()
            return JsonResponse({'msg': 'Report Save!'})

    return JsonResponse({})

@login_required
def generate_pdf_view(request, pk):

    report = get_object_or_404(Report, pk=pk)

    template_path = 'reports/pdf.html'
    context = {'report': report}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    #Direct download pdf
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    #Display reports content in pdf file
    response['Content-Disposition'] = 'filename="report.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
