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

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    quantity = models.IntegerField(default=1)
    best_by = models.DateField()


    @property
    def status(self):
        today = date.today()
        if self.best_by < today:
            return "spoiled"
        elif self.best_by <= today + timedelta(days=2):
            return "about_to_spoil"
        return "fresh"
