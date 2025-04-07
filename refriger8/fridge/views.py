# fridge/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import FoodItem
from .forms import FoodItemForm


def fridge_view(request):
    sort = request.GET.get('sort')
    selected_category = request.GET.get('category', '')

    items = FoodItem.objects.all()

    if selected_category:
        items = items.filter(category=selected_category)

    # Apply sorting safely
    if sort:
        items = items.order_by(sort)
    else:
        items = items.order_by('storage_location', 'best_by')

    form = FoodItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('fridge')

    categories = FoodItem.CATEGORY_CHOICES
    return render(request, 'fridge/fridge.html', {
        'items': items,
        'form': form,
        'categories': categories,
        'selected_category': selected_category,
        'sort': sort
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
