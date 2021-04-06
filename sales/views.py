import pandas as pd
from django.shortcuts import render
from django.views import generic
from sales.models import Sale
from sales.forms import SalesSearchForm
from reports.forms import ReportForm
from reports.models import Report
from sales.utils import get_customer_from_id, get_salesman_from_id, get_chart

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def home_view(request):
    sales_df = None
    positions_df = None
    merged_df = None
    df = None
    chart = None
    report_form = None
    no_data = None
    if request.method == 'POST':
        form = SalesSearchForm(request.POST)
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            chart_type = form.cleaned_data['chart_type']
            results_type = form.cleaned_data['results_type']
            sales_qs = Sale.objects.filter(created__date__gte=date_from, created__date__lte=date_to)
            if len(sales_qs) > 0:
                sale_df = pd.DataFrame(sales_qs.values())
                sale_df['customer_id'] = sale_df['customer_id'].apply(get_customer_from_id)
                sale_df['salesman_id'] = sale_df['salesman_id'].apply(get_salesman_from_id)
                sale_df['created'] = sale_df['created'].apply(lambda d: d.strftime("%d-%m-%Y"))
                sale_df['updated'] = sale_df['updated'].apply(lambda d: d.strftime("%d-%m-%Y"))
                sale_df.rename({'customer_id': 'customer', 'salesman_id': 'salesman', 'id': 'sales_id'}, axis=1, inplace=True)
                positions_data = []
                for sale in sales_qs:
                    for position in sale.get_positions():
                        pos = {
                            'position_id': position.id,
                            'product': position.product.name,
                            'quantity': position.quantity,
                            'price': position.price,
                            'sales_id': position.get_sale_id(),
                        }
                        positions_data.append(pos)
                position_df = pd.DataFrame(positions_data)
                merged_df = pd.merge(sale_df, position_df, on='sales_id')
                df = merged_df.groupby('transaction_id', as_index=False)['total_price'].agg('sum')
                
                chart = get_chart(chart_type, sale_df, results_type)

                merged_df = merged_df.to_html()
                positions_df = position_df.to_html()
                sales_df = sale_df.to_html()
                df = df.to_html()

                report_form = ReportForm()
            else:
                no_data = 'No data is availabel in this date'
        else:
            form = SalesSearchForm(request.POST)
    else:
        form = SalesSearchForm()

    context = {
        'search_form': form,
        'sales_df': sales_df,
        'positions_df': positions_df,
        'merged_df': merged_df,
        'df': df,
        'chart': chart,
        'report_form': report_form,
        'no_data': no_data,
    }
    return render(request, 'sales/home.html', context)


class SaleListView(LoginRequiredMixin, generic.ListView):
    model = Sale
    template_name = 'sales/main.html'
    context_object_name = 'sales'

class SaleDetailView(LoginRequiredMixin, generic.DetailView):
    model = Sale
    template_name = 'sales/detail.html'
    context_object_name = 'sale'