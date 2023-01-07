from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.dateparse import parse_date

from .models import *
from datetime import datetime
from django import forms

form = ""
form_data = ""
tables = ""
table_number = 0
data = ""
mas_table_number = []
active_button = 0

min = str(datetime.now())[0:10]


def all_buttons(reset = False):
    k = 1
    global mas_table_number
    input_all_buttons = ""
    if reset:
        mas_table_number.clear()
    for table in tables:
        if mas_table_number:
            input_all_buttons += '<div class="buttons">\n'
            for post in mas_table_number:
                if post == table.table_number:
                    input_all_buttons += f'\t<button class="buttons" disabled name="button{k}">{table.table_number}</button>\n'
                    break
            else:
                input_all_buttons += f'\t<button class="buttons" name="button{k}">{table.table_number}</button>\n'
            input_all_buttons += '</div>\n'

        else:
            input_all_buttons += '<div class="buttons">\n'
            input_all_buttons += f'\t<button class="buttons" name="button{k}">{table.table_number}</button>\n'
            input_all_buttons += '</div>\n'
        k += 1
    return input_all_buttons


def work_button(request):
    global table_number
    table_number, active_buttons = fill_form2(request)
    return render(request, 'reservation/home.html', {'form': form, 'form_data': form_data, 'tables': tables, 'mas_table_number': mas_table_number, 'buttons': all_buttons(), 'active_buttons': active_buttons})

def home(request):
    global form, tables, mas_table_number, form_data
    form = AddForm()
    form_data = DataForm()
    date = fill_form(request)
    tables = Tables.objects.all()
    mas_table_number.clear()
    if type(date) != str:
        print("Error str")
        return render(request, 'reservation/home.html', {'form': form, 'form_data': form_data, 'tables': tables, 'buttons': all_buttons(True)})
    int_data = parse_date(date)

    try:
        posts = Order.objects.filter(data=int_data)
        for post in posts:
            rezes = Order.objects.get(id=post.id).table_number.all()
            for rez in rezes:
                mas_table_number.append(rez.table_number)
        print(mas_table_number)
        return render(request, 'reservation/home.html', {'form': form, 'form_data': form_data, 'tables': tables, 'mas_table_number': mas_table_number, 'buttons': all_buttons()})
    except:
        print("posts are empty")
        return render(request, 'reservation/home.html', {'form': form, 'form_data': form_data, 'tables': tables, 'buttons': all_buttons(True)})


def fill_form(request):
    global data
    if request.method == "POST":
        data = request.POST.get("data")
        print(data)
        return data


def fill_form2(request):
    global active_button
    if request.method == "POST":
        for i in range(len(tables)):
            if request.POST.get(f'button{i + 1}') == '' and active_button == i+1:
                active_button = 0
                return 0, False
            if request.POST.get(f'button{i+1}') == '':
                active_button = i+1
                print(i+1)
                return i+1, True


def send_email(email, data):
    text = get_template('reservation/email.html')
    html = get_template('reservation/email.html')
    context = {'data': data}
    subject = 'Вам новое сообщение.'
    from_email = 'from@example.com'
    text_content = text.render(context)
    html_content = html.render(context)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()



def work_field(request):
    global table_number, data
    if request.method == "POST":
        addform = AddForm(request.POST)
        if addform.is_valid():
            name = request.POST.get("name")
            email = request.POST.get("email")
            try:
                new_field = Tables.objects.get(table_number=table_number)
                new_field.order_set.create(name=name, email=email, data=data)
                send_email(email, data)
            except:
                print('Data not written to the database')
        table_number = 0
        data = ""
    return render(request, 'reservation/home.html', {'form': form, 'form_data': form_data, 'tables': tables, 'buttons': all_buttons(True)})


class AddForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'email']
        widgets = {
                   'name': forms.TextInput(attrs={'size': 44, 'name': 'name'}),
                   'email': forms.EmailInput(attrs={'size': 44, 'name': 'email'}),
                   }

    def clean_name(self):
        name = self.cleaned_data['name']
        if name == '':
            print('error')
            return
        return name

class DataForm(forms.Form):
    data = forms.DateField(widget=forms.TextInput(attrs={'min': min, 'max': '2023-12-01', 'type': 'date', 'name': 'data'}))
