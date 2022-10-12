from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from pms.forms import SignUpForm, DrugForm, OrderForm
from pms.models import Drug, Order


def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            total_drugs = Drug.objects.all().order_by('id')
            total_orders_of_each_drug = [Order.objects.filter(drugs=drug).order_by('id').count() for drug in
                                         total_drugs]
            return render(request, 'pms/index.html',
                          {'total_drugs': total_drugs, 'total_orders': total_orders_of_each_drug})
        else:
            return render(request, 'pms/orders/my-orders.html',
                          {'orders': Order.objects.filter(buyer_id=request.user.id)})
    else:
        return redirect('login')


def signout(request):
    logout(request)
    return redirect('login')


def signin(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('homepage')
        else:
            return render(request, 'pms/login.html', context={'errors': "Invalid Credentials, Please try again!"})
    else:
        return render(request, 'pms/login.html')


def signup(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            # TODO add a flush message in login form
            return redirect('login')
        else:
            return render(request, 'pms/signup.html', context={'errors': signup_form.errors})
    return render(request, 'pms/signup.html')


def drugs(request):
    if request.user.is_authenticated:
        return render(request, 'pms/drugs/drugs.html', {'drugs': Drug.objects.all()})
    else:
        return redirect('login')


def drugs_list(request):
    # TODO make this for users and admin
    return render(request, 'pms/drugs/drug-list.html',
                  {'drugs': Drug.objects.all(), 'admin': request.user.is_superuser})


def search_drug(request):
    if request.GET['search']:
        searched_drugs = Drug.objects.filter(name__icontains=request.GET['search'])
    else:
        searched_drugs = Drug.objects.all()
    return render(request, 'pms/drugs/drug-list.html', {'drugs': searched_drugs, 'admin': request.user.is_superuser})


def show_drug(request, drug_id):
    return render(request, 'pms/drugs/show_drug.html', {'drug': get_object_or_404(Drug, id=drug_id)})


def update_drug(request, drug_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            drug_form = DrugForm(request.POST, instance=get_object_or_404(Drug, id=drug_id))
            if drug_form.is_valid():
                drug_form.save()
                # TODO redirect to show
                return redirect('drugs_list')
        return render(request, 'pms/drugs/update.html',
                      {'form': DrugForm(instance=get_object_or_404(Drug, id=drug_id)),
                       'drug': get_object_or_404(Drug, id=drug_id)})
    else:
        return redirect('login')


def delete_drug(request, drug_id):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            drug = get_object_or_404(Drug, id=drug_id)
            drug.delete()
        return redirect('drugs_list')
    else:
        return redirect('login')


def add_drug(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            drug_form = DrugForm(request.POST)
            if drug_form.is_valid():
                drug_form.save()
                # TODO add a flush message in login form
                return redirect('drugs')
        drug_form = DrugForm()
        return render(request, 'pms/drugs/add_drug.html', {'form': drug_form})
    else:
        return redirect('login')


def orders(request):
    if not request.user.is_superuser:
        return render(request, 'pms/orders/my-orders.html', {'orders': Order.objects.filter(buyer_id=request.user.id)})


def place_order(request, drug_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                drug = get_object_or_404(Drug, id=drug_id)
                if form.cleaned_data['quantity'] <= drug.stock:
                    drug.stock = drug.stock - form.cleaned_data['quantity']
                    drug.save()
                    form.save()
                    return redirect('homepage')
                else:
                    form.add_error('quantity', f'Failed to order! Stock is only {drug.stock}')
                    return render(request, 'pms/drugs/place_order.html', {'form': form})
            else:
                return render(request, 'pms/drugs/place_order.html', {'form': form})
        form = OrderForm(
            initial={'buyer': request.user,
                     'date': timezone.now().date(),
                     'drugs': get_object_or_404(Drug, id=drug_id)
                     })
        return render(request, 'pms/drugs/place_order.html', {'form': form, })
    else:
        return redirect('login')


def order_bill(request, order_id):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'pms/orders/bill.html', {
            'name': f'{request.user.first_name} {request.user.last_name}',
            'order_id': order.id,
            'drug_id': order.drugs.first().id,
            'drug_name': order.drugs.first().name,
            'unit_price': order.drugs.first().price,
            'quantity': order.quantity,
            'total_price': order.drugs.first().price * order.quantity
        })

    else:
        return redirect('login')


def sales_data(request):
    total_drugs = Drug.objects.all().order_by('id')
    total_orders_of_each_drug = [Order.objects.filter(drugs=drug).order_by('id').count() for drug in total_drugs]
    return JsonResponse(
        {"total_drugs": [f'{drug.id} {drug.name}' for drug in total_drugs], "total_orders": total_orders_of_each_drug})


def has_notification(request):
    if request.user.is_superuser:
        all_drugs = Drug.objects.all()
        for drug in all_drugs:
            if drug.is_expired():
                return JsonResponse({"notification": True, "msg": "Update the expired drugs!"})
            if drug.stock < 1:
                return JsonResponse({"notification": True, "msg": "Update the stock of the drugs!"})
        return JsonResponse({"notification": False})
    else:
        pass
