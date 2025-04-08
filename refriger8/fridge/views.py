# fridge/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import FoodItem
from .forms import FoodItemForm
from django.urls import reverse

# views.py

def fridge_view(request):
    items = FoodItem.objects.all()

    # GET parameters
    sort = request.GET.get('sort')
    selected_category = request.GET.get('category', '')
    selected_storage = request.GET.get('storage', '')

    # Filter by category/storage
    if selected_category:
        items = items.filter(category=selected_category)
    if selected_storage:
        items = items.filter(storage_location=selected_storage)

    # Sorting
    if sort and sort != 'None':
        items = items.order_by(sort)
    else:
        items = items.order_by('storage_location', 'best_by')

    # Initialize the form with default storage
    initial_data = {'storage_location': selected_storage} if selected_storage else {}
    form = FoodItemForm(request.POST or None, initial=initial_data)

    if form.is_valid():
        form.save()
        # Preserve filters after adding
        redirect_url = reverse('fridge')
        params = []
        if selected_category:
            params.append(f"category={selected_category}")
        if selected_storage:
            params.append(f"storage={selected_storage}")
        if sort and sort != 'None':
            params.append(f"sort={sort}")
        if params:
            redirect_url += '?' + '&'.join(params)
        return redirect(redirect_url)

    context = {
        'items': items,
        'form': form,
        'categories': FoodItem.CATEGORY_CHOICES,
        'storage_locations': FoodItem.STORAGE_CHOICES,
        'selected_category': selected_category,
        'selected_storage': selected_storage,
        'sort': sort,
    }

    return render(request, 'fridge/fridge.html', context)



from django.shortcuts import get_object_or_404

def delete_item(request, pk):
    item = get_object_or_404(FoodItem, pk=pk)
    item.delete()

    # Preserve filters and sorting
    selected_category = request.GET.get('category', '')
    selected_storage = request.GET.get('storage', '')
    sort = request.GET.get('sort', '')

    redirect_url = reverse('fridge')
    params = []
    if selected_category:
        params.append(f"category={selected_category}")
    if selected_storage:
        params.append(f"storage={selected_storage}")
    if sort:
        params.append(f"sort={sort}")
    if params:
        redirect_url += '?' + '&'.join(params)

    return redirect(redirect_url)

def edit_item(request, pk):
    item = get_object_or_404(FoodItem, pk=pk)

    category = request.GET.get('category', '')
    storage = request.GET.get('storage', '')

    if request.method == 'POST':
        form = FoodItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            # Redirect back to fridge with filters
            return redirect(f'/?' + f'category={category}&storage={storage}')
    else:
        form = FoodItemForm(instance=item)

    return render(request, 'fridge/edit.html', {
        'form': form,
        'item': item,
        'category': category,
        'storage': storage
    })


import csv
from django.http import HttpResponse

def export_items_csv(request):
    items = FoodItem.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="fridge_export.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Category', 'Quantity', 'Best By', 'Opened', 'Storage'])

    for item in items:
        writer.writerow([
            item.name,
            item.get_category_display(),
            item.quantity,
            item.best_by if item.best_by else "Unknown",
            "Yes" if item.opened else "No",
            item.get_storage_location_display(),
        ])

    return response

from collections import defaultdict
from django.utils import timezone

def overview_view(request):
    today = timezone.now().date()
    items = FoodItem.objects.all()

    # Collect only spoiled or about-to-spoil items
    overview = defaultdict(list)
    for item in items:
        status = item.status
        if status in ('spoiled', 'about_to_spoil'):
            overview[item.get_storage_location_display()].append(item)

    # Sort each list by best_by date (None dates last)
    for storage in overview:
        overview[storage].sort(key=lambda x: (x.best_by is None, x.best_by))

    return render(request, 'fridge/overview.html', {
        'overview': dict(overview)
    })

