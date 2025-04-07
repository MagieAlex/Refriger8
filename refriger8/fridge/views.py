# fridge/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import FoodItem
from .forms import FoodItemForm

def fridge_view(request):
    sort = request.GET.get('sort')
    selected_category = request.GET.get('category', '')
    selected_storage = request.GET.get('storage', '')

    items = FoodItem.objects.all()

    if selected_category:
        items = items.filter(category=selected_category)

    if selected_storage:
        items = items.filter(storage_location=selected_storage)

    if sort:
        items = items.order_by(sort)
    else:
        items = items.order_by('storage_location', 'best_by')

    form = FoodItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('fridge')

    categories = FoodItem.CATEGORY_CHOICES
    storage_locations = FoodItem.STORAGE_CHOICES

    return render(request, 'fridge/fridge.html', {
        'items': items,
        'form': form,
        'categories': categories,
        'selected_category': selected_category,
        'selected_storage': selected_storage,
        'sort': sort,
        'storage_locations': storage_locations,
    })


from django.shortcuts import get_object_or_404

def delete_item(request, pk):
    item = get_object_or_404(FoodItem, pk=pk)
    item.delete()
    return redirect('fridge')

def edit_item(request, pk):
    item = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('fridge')
    else:
        form = FoodItemForm(instance=item)
    return render(request, 'fridge/edit.html', {'form': form, 'item': item})

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

    return render(request, 'fridge/overview.html', {
        'overview': dict(overview)
    })

