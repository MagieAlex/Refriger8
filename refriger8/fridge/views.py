from django.shortcuts import render

# fridge/views.py
from django.shortcuts import render, redirect
from .models import FoodItem
from .forms import FoodItemForm

def fridge_view(request):
    items = FoodItem.objects.all().order_by('best_by')
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fridge')
    else:
        form = FoodItemForm()
    return render(request, 'fridge/fridge.html', {'items': items, 'form': form})
