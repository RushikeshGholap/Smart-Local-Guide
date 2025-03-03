# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Business(models.Model):
    gmap_id = models.TextField(primary_key=True)
    business_name = models.TextField()
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    num_of_reviews = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    hours = models.TextField(blank=True, null=True)
    misc = models.JSONField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    relative_results = models.TextField(blank=True, null=True)  # This field type is a guess.
    url = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'business'


class Reviews(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user_id = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=255)
    time = models.DateTimeField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    text = models.TextField()
    resp = models.TextField(blank=True, null=True)
    gmap_id = models.CharField(max_length=50)
    clean_text = models.TextField(blank=True, null=True)
    text_sentiment = models.BigIntegerField(blank=True, null=True)
    sentiment_confidence = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reviews'


class Users(models.Model):
    user_id = models.TextField(primary_key=True)
    customer_name = models.TextField(blank=True, null=True)
    first_review_date = models.DateTimeField(blank=True, null=True)
    last_review_date = models.DateTimeField(blank=True, null=True)
    user_lifetime_days = models.IntegerField(blank=True, null=True)
    total_reviews = models.IntegerField(blank=True, null=True)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    min_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    max_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    sentiment_avg_score = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    sentiment_volatility = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    highly_positive_reviews = models.IntegerField(blank=True, null=True)
    highly_negative_reviews = models.IntegerField(blank=True, null=True)
    balanced_reviews = models.IntegerField(blank=True, null=True)
    has_response = models.IntegerField(blank=True, null=True)
    avg_response_time = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    active_years = models.IntegerField(blank=True, null=True)
    active_months = models.IntegerField(blank=True, null=True)
    peak_activity_year = models.IntegerField(blank=True, null=True)
    peak_activity_month = models.IntegerField(blank=True, null=True)
    review_frequency = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    recent_activity_score = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
