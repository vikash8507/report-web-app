import uuid, base64
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from customers.models import Customer
from profiles.models import Profile

def gen_transaction_id():
    id = str(uuid.uuid4()).replace('-', '')[:12]
    return id

def get_customer_from_id(value):
    return Customer.objects.get(id=value).name

def get_salesman_from_id(value):
    return Profile.objects.get(id=value).user.username

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_chart(chart_type, data, results_type, **kwargs):
    plt.switch_backend('AGG')
    if results_type == '#1':
        key = 'transaction_id'
    else:
        key = 'created'

    df = data.groupby(key, as_index=False)['total_price'].agg('sum')

    if chart_type == '#2':
        plt.pie(data=df, x='total_price', labels=df[key].values)
    elif chart_type == '#3':
        plt.plot(df[key], df['total_price'], color='green', marker='o', linestyle='dashed')
    else:
        # plt.bar(df[key], df['total_price'])
        sns.barplot(x=key, y='total_price', data=df)

    plt.tight_layout()
    chart = get_graph()
    return chart

    