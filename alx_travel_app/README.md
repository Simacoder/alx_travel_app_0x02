# ALX Travel App 0x01 - API Development

This project extends the ALX Travel App with RESTful API endpoints for managing listings, bookings, and reviews using Django REST Framework ViewSets.

## Project Structure

```
alx_travel_app_0x01/
├── alx_travel_app/
│   ├── listings/
│   │   ├── views.py          # ViewSets for Listing, Booking, Review
│   │   ├── urls.py           # API URL configuration with router
│   │   ├── models.py         # Data models
│   │   └── serializers.py    # DRF serializers
│   ├── settings.py
│   └── urls.py
└── README.md
```

## API Endpoints

The API follows RESTful conventions and is accessible under `/api/`. All endpoints support standard HTTP methods (GET, POST, PUT/PATCH, DELETE).

### Base URL
```
http://localhost:8000/api/
```

### Listings API

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/listings/` | List all listings | Optional |
| POST | `/api/listings/` | Create a new listing | Required |
| GET | `/api/listings/{listing_id}/` | Retrieve a specific listing | Optional |
| PUT | `/api/listings/{listing_id}/` | Update a listing (full) | Required (host only) |
| PATCH | `/api/listings/{listing_id}/` | Update a listing (partial) | Required (host only) |
| DELETE | `/api/listings/{listing_id}/` | Delete a listing | Required (host only) |

**Query Parameters:**
- `host`: Filter listings by host username (e.g., `/api/listings/?host=john`)

### Bookings API

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/bookings/` | List user's bookings | Required |
| POST | `/api/bookings/` | Create a new booking | Required |
| GET | `/api/bookings/{booking_id}/` | Retrieve a specific booking | Required (owner only) |
| PUT | `/api/bookings/{booking_id}/` | Update a booking (full) | Required (owner only) |
| PATCH | `/api/bookings/{booking_id}/` | Update a booking (partial) | Required (owner only) |
| DELETE | `/api/bookings/{booking_id}/` | Delete a booking | Required (owner only) |

### Reviews API

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/reviews/` | List all reviews | Optional |
| POST | `/api/reviews/` | Create a new review | Required |
| GET | `/api/reviews/{review_id}/` | Retrieve a specific review | Optional |
| PUT | `/api/reviews/{review_id}/` | Update a review (full) | Required (author only) |
| PATCH | `/api/reviews/{review_id}/` | Update a review (partial) | Required (author only) |
| DELETE | `/api/reviews/{review_id}/` | Delete a review | Required (author only) |
| GET | `/api/reviews/my_reviews/` | Get current user's reviews | Required |

**Query Parameters:**
- `listing_id`: Filter reviews by listing (e.g., `/api/reviews/?listing_id=123`)

## Setup Instructions

1. **Duplicate the project:**
   ```bash
   cp -r alx_travel_app_0x00 alx_travel_app_0x01
   cd alx_travel_app_0x01
   ```

2. **Install dependencies:**
   ```bash
   pip install djangorestframework
   pip install django-cors-headers  # If needed for CORS
   ```

3. **Update settings.py:**
   ```python
   INSTALLED_APPS = [
       # ... other apps
       'rest_framework',
       'listings',
   ]
   
   REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': [
           'rest_framework.authentication.SessionAuthentication',
           'rest_framework.authentication.TokenAuthentication',
       ],
       'DEFAULT_PERMISSION_CLASSES': [
           'rest_framework.permissions.IsAuthenticatedOrReadOnly',
       ],
       'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
       'PAGE_SIZE': 20
   }
   ```

4. **Update main urls.py:**
   ```python
   from django.contrib import admin
   from django.urls import path, include
   
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('', include('listings.urls')),
   ]
   ```

5. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the server:**
   ```bash
   python manage.py runserver
   ```

## Testing with Postman

### Authentication
For endpoints requiring authentication, you can use:
1. **Session Authentication**: Login via Django admin or login endpoint
2. **Token Authentication**: Include `Authorization: Token <token>` header

### Sample API Calls

#### 1. Create a Listing (POST)
```
POST http://localhost:8000/api/listings/
Content-Type: application/json
Authorization: Token <your-token>

{
    "title": "Hector Perterson House",
    "description": "A stunning historical property",
    "price_per_night": 150.00,
    "location": "Soweto",
    "amenities": ["WiFi", "Pool", "Beach Access"]
}
```

#### 2. Get All Listings (GET)
```
GET http://localhost:8000/api/listings/
```

#### 3. Get Specific Listing (GET)
```
GET http://localhost:8000/api/listings/1/
```

#### 4. Create a Booking (POST)
```
POST http://localhost:8000/api/bookings/
Content-Type: application/json
Authorization: Token <your-token>

{
    "listing": "1",
    "start_date": "2024-12-01",
    "end_date": "2024-12-05",
    "total_price": 600.00
}
```

#### 5. Get User's Bookings (GET)
```
GET http://localhost:8000/api/bookings/
Authorization: Token <your-token>
```

#### 6. Create a Review (POST)
```
POST http://localhost:8000/api/reviews/
Content-Type: application/json
Authorization: Token <your-token>

{
    "listing": "1",
    "rating": 5,
    "comment": "Amazing place! Highly recommended."
}
```

#### 7. Get Reviews for a Listing (GET)
```
GET http://localhost:8000/api/reviews/?listing_id=1
```

## Key Features

### ViewSets Benefits
- **Automatic URL routing**: Router automatically generates all CRUD endpoints
- **Consistent API structure**: All endpoints follow RESTful conventions
- **Built-in permissions**: Proper access control for different operations
- **Custom actions**: Additional endpoints like `my_reviews`

### Security Features
- **Authentication required**: For creating, updating, and deleting resources
- **Owner-only access**: Users can only modify their own bookings and reviews
- **Host-only access**: Only listing hosts can modify their listings
- **Validation**: Prevents booking own listings and duplicate reviews

### Error Handling
- Proper HTTP status codes (200, 201, 400, 401, 403, 404)
- Descriptive error messages
- Validation for required fields and relationships

## API Browser
Visit `http://localhost:8000/api/` in your browser to see the DRF browsable API interface, which provides:
- Interactive API documentation
- Forms for testing endpoints
- Authentication interface
- Response formatting options

## Swagger Documentation
To add Swagger documentation, install and configure `drf-yasg`:

```bash
pip install drf-yasg
```

Add to `settings.py`:
```python
INSTALLED_APPS = [
    # ... other apps
    'drf_yasg',
]
```

Add to main `urls.py`:
```python
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="ALX Travel App API",
        default_version='v1',
        description="API for managing travel listings, bookings, and reviews",
    ),
    public=True,
)

urlpatterns = [
    # ... other patterns
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
]
```

# AUTHOR
- Simanga Mchunu