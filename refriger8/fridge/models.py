from django.db import models
from datetime import date, timedelta

class FoodItem(models.Model):
    CATEGORY_CHOICES = [
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('dairy', 'Dairy'),
        ('meat', 'Meat'),
        ('poultry', 'Poultry'),
        ('fish', 'Fish & Seafood'),
        ('eggs', 'Eggs'),
        ('baked', 'Baked Goods'),
        ('leftovers', 'Leftovers'),
        ('spreads', 'Spreads & Dips'),
        ('condiments', 'Condiments & Sauces'),
        ('beverages', 'Beverages'),
        ('frozen', 'Frozen Foods'),
        ('snacks', 'Snacks & Sweets'),
        ('prepared', 'Prepared Meals'),
        ('other', 'Other'),
    ]

    STORAGE_CHOICES = [
        ('fridge', 'Fridge'),
        ('freezer', 'Freezer'),
        ('upper_pantry', 'Upper Pantry'),
        ('lower_pantry', 'Lower Pantry'),
        ('counter', 'Counter'),
        ('candy_cabinet', 'Candy Cabinet'),
        ('hanging_table', 'Hanging Table'),
        ('bar', 'Bar'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    quantity = models.IntegerField(default=1)
    best_by = models.DateField(null=True, blank=True)
    storage_location = models.CharField(max_length=50, choices=STORAGE_CHOICES, default='fridge')


    @property
    def status(self):
        today = date.today()
        if self.best_by < today:
            return "spoiled"
        elif self.best_by <= today + timedelta(days=2):
            return "about_to_spoil"
        return "fresh"

    @property
    def days_left(self):
        delta = (self.best_by - date.today()).days
        if delta > 0:
            return f"in {delta} day{'s' if delta > 1 else ''}"
        elif delta == 0:
            return "today"
        else:
            return f"{abs(delta)} day{'s' if abs(delta) > 1 else ''} ago"

