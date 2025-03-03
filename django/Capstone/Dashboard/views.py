from django.shortcuts import render

# Create your views here.
from django.shortcuts import render




from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Reviews
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Reviews

def home(request):
    return render(request, 'Dashboard/base.html')

def reviews_list(request):
    # Extract filter parameters from the request
    user_id = request.GET.get('user_id')
    customer_name = request.GET.get('customer_name')
    min_rating = request.GET.get('min_rating')
    max_rating = request.GET.get('max_rating')
    start_date = request.GET.get('start_date')  # Format: YYYY-MM-DD
    end_date = request.GET.get('end_date')  # Format: YYYY-MM-DD
    text_contains = request.GET.get('text_contains')
    gmap_id = request.GET.get('gmap_id')
    sentiment = request.GET.get('sentiment')
    order_by = request.GET.get('order_by', '-time')  # Default order by newest first
    page = request.GET.get('page', 1)
    per_page = 6  # Show 6 reviews per page (matching the UI)

    # Build query using Q objects
    filters = Q()
    
    if user_id:
        filters &= Q(user_id=user_id)
    if customer_name:
        filters &= Q(customer_name__icontains=customer_name)
    if min_rating:
        filters &= Q(rating__gte=min_rating)
    if max_rating:
        filters &= Q(rating__lte=max_rating)
    if start_date:
        filters &= Q(time__date__gte=start_date)
    if end_date:
        filters &= Q(time__date__lte=end_date)
    if text_contains:
        filters &= Q(text__icontains=text_contains)
    if gmap_id:
        filters &= Q(gmap_id=gmap_id)
    if sentiment:
        filters &= Q(text_sentiment=sentiment)

    # Query the database with applied filters
    reviews = Reviews.objects.filter(filters).order_by(order_by)

    # Paginate results
    paginator = Paginator(reviews, per_page)
    paginated_reviews = paginator.get_page(page)

    # Pass data to the template
    context = {
        "reviews": paginated_reviews,
        "total_reviews": paginator.count,
    }
    
    return render(request, 'Dashboard/reviews.html', context)


import json
from .models import Business


from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Business
import json
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Business
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
import json
from .models import Business
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
import json
from .models import Business

def business_list(request):
    # Extract filter parameters
    business_name = request.GET.get('business_name')
    category = request.GET.get('category')
    min_rating = request.GET.get('min_rating')
    max_rating = request.GET.get('max_rating')
    page = int(request.GET.get('page', 1))
    per_page = 6  # Show only 6 businesses per page

    # Filtering businesses
    filters = Q()
    if business_name:
        filters &= Q(business_name__icontains=business_name)
    if category:
        filters &= Q(category__icontains=category)
    if min_rating:
        filters &= Q(avg_rating__gte=min_rating)
    if max_rating:
        filters &= Q(avg_rating__lte=max_rating)

    # Query only businesses within Pennsylvania
    businesses = Business.objects.filter(filters).order_by('-avg_rating')

    # Paginate results (only show 6 per page)
    paginator = Paginator(businesses, per_page)
    paginated_businesses = paginator.get_page(page)

    # **Pass only paginated businesses to the map**
    business_locations = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(b.longitude), float(b.latitude)]
                },
                "properties": {
                    "name": b.business_name,
                    "category": b.category,
                    "rating": float(b.avg_rating) if b.avg_rating else None
                }
            }
            for b in paginated_businesses if b.latitude and b.longitude
        ]
    }

    context = {
        "businesses": paginated_businesses,
        "total_businesses": paginator.count,
        "business_geojson": json.dumps(business_locations),  # JSON data for ECharts
    }

    return render(request, 'Dashboard/business.html', context)
