# MadSugu - Phase 2/3 Features Documentation

This document describes the newly implemented Phase 2 and Phase 3 features for the MadSugu platform.

## Table of Contents
1. [Rating and Review System](#1-rating-and-review-system)
2. [Personalized Alerts](#2-personalized-alerts)
3. [Ad Boosting](#3-ad-boosting)
4. [Admin Dashboard](#4-admin-dashboard)
5. [Push Notifications](#5-push-notifications)
6. [Progressive Web App (PWA)](#6-progressive-web-app-pwa)
7. [Advanced Geolocation](#7-advanced-geolocation)
8. [Analytics and Statistics](#8-analytics-and-statistics)

---

## 1. Rating and Review System

### Overview
Users can now rate and review other users based on their transactions. This builds trust and reputation within the platform.

### Features
- Star rating system (1-5 stars)
- Written comments (optional)
- Reviews linked to specific annonces (optional)
- Automatic rating aggregation for users
- Review management (edit, delete)

### API Endpoints

#### Create Review
```http
POST /api/v1/reviews/
Content-Type: application/json
Authorization: Bearer {token}

{
  "reviewed_user_id": 123,
  "rating": 4.5,
  "comment": "Great seller, fast delivery!",
  "annonce_id": 456
}
```

#### Get User Reviews
```http
GET /api/v1/reviews/user/{user_id}?skip=0&limit=20
```

#### Update Review
```http
PUT /api/v1/reviews/{review_id}
Content-Type: application/json
Authorization: Bearer {token}

{
  "rating": 5.0,
  "comment": "Updated comment"
}
```

### Frontend Components
- `ReviewForm.svelte`: Form for submitting reviews
- `ReviewList.svelte`: Display list of reviews for a user

---

## 2. Personalized Alerts

### Overview
Users can create custom alerts to be notified when new annonces matching their criteria are published.

### Features
- Multiple criteria: keywords, category, location, price range
- Notification frequency: instant, daily, weekly
- Active/inactive status management
- Automatic matching with new annonces

### API Endpoints

#### Create Alert
```http
POST /api/v1/alerts/
Content-Type: application/json
Authorization: Bearer {token}

{
  "title": "iPhone 13 à Dakar",
  "keywords": "iphone 13 pro max",
  "category_id": 5,
  "location_city": "Dakar",
  "min_price": 200000,
  "max_price": 500000,
  "frequency": "instant"
}
```

#### List My Alerts
```http
GET /api/v1/alerts/?skip=0&limit=50
Authorization: Bearer {token}
```

#### Toggle Alert Status
```http
POST /api/v1/alerts/{alert_id}/toggle
Authorization: Bearer {token}
```

### Frontend Components
- `AlertForm.svelte`: Form for creating alerts

### Backend Services
- `AlertService`: Matches new annonces against active alerts

---

## 3. Ad Boosting

### Overview
Users can boost their annonces to increase visibility through featured placement.

### Features
- Multiple boost durations (7, 14, 30 days)
- Pricing structure in FCFA
- Featured/urgent flags
- Automatic expiration tracking

### API Endpoints

#### Get Boost Prices
```http
GET /api/v1/boost/prices
```

Response:
```json
{
  "prices": [
    {"duration_days": 7, "price": 2000, "currency": "FCFA"},
    {"duration_days": 14, "price": 3500, "currency": "FCFA"},
    {"duration_days": 30, "price": 6000, "currency": "FCFA"}
  ]
}
```

#### Boost Annonce
```http
POST /api/v1/boost/
Content-Type: application/json
Authorization: Bearer {token}

{
  "annonce_id": 123,
  "duration_days": 7
}
```

#### Mark as Urgent
```http
POST /api/v1/boost/{annonce_id}/urgent
Authorization: Bearer {token}
```

---

## 4. Admin Dashboard

### Overview
Administrative interface for platform management, user moderation, and statistics visualization.

### Features
- User management (verify, suspend)
- Annonce moderation (approve, disable)
- Dashboard statistics
- Recent activity tracking

### API Endpoints

#### Get Dashboard Stats
```http
GET /api/v1/admin/stats/dashboard
Authorization: Bearer {token}
```

#### Verify User
```http
PUT /api/v1/admin/users/{user_id}/verify
Authorization: Bearer {token}
```

#### Approve Annonce
```http
PUT /api/v1/admin/annonces/{annonce_id}/approve
Authorization: Bearer {token}
```

#### Disable Annonce
```http
PUT /api/v1/admin/annonces/{annonce_id}/disable?reason=Violation%20des%20CGU
Authorization: Bearer {token}
```

### Frontend Pages
- `/admin`: Main dashboard with statistics
- `/admin/users`: User management (to be implemented)
- `/admin/annonces`: Annonce moderation (to be implemented)

### Access Control
Currently using `is_pro` flag as temporary admin indicator. Should be replaced with proper role-based access control (RBAC) in production.

---

## 5. Push Notifications

### Overview
Real-time notification system for important events with support for push notifications.

### Features
- Multiple notification types (messages, favorites, reviews, alerts, etc.)
- Read/unread status
- Push notification support via service worker
- Real-time notification bell in header

### Notification Types
- `NEW_MESSAGE`: New message received
- `NEW_FAVORITE`: Annonce added to favorites
- `ANNONCE_SOLD`: Annonce marked as sold
- `ANNONCE_EXPIRED`: Annonce expired
- `ALERT_MATCHED`: Alert criteria matched
- `NEW_REVIEW`: New review received
- `BOOST_EXPIRED`: Boost period ended
- `ADMIN_MESSAGE`: Administrative message

### API Endpoints

#### Get Notifications
```http
GET /api/v1/notifications/?skip=0&limit=50&unread_only=false
Authorization: Bearer {token}
```

#### Mark as Read
```http
PUT /api/v1/notifications/{notification_id}/read
Authorization: Bearer {token}
```

#### Mark All as Read
```http
PUT /api/v1/notifications/mark-all-read
Authorization: Bearer {token}
```

### Frontend Components
- `NotificationBell.svelte`: Notification dropdown in header
- `notifications.js`: Notification store and API methods

### Service Worker
- Location: `/static/service-worker.js`
- Handles push events and notification clicks
- Caching for offline support

---

## 6. Progressive Web App (PWA)

### Overview
The application is now installable as a PWA with offline capabilities.

### Features
- App manifest configuration
- Service worker for caching
- Offline support
- App shortcuts
- Installable on mobile and desktop

### Configuration Files

#### Manifest (`/static/manifest.json`)
- App name, icons, theme colors
- Display mode: standalone
- App shortcuts for quick actions

#### Service Worker (`/static/service-worker.js`)
- Cache-first strategy
- Push notification handling
- Background sync (future)

### Installation
1. Visit the website on a mobile device
2. Tap "Add to Home Screen" (iOS) or "Install" (Android)
3. The app will be installed like a native app

### Icons Required
- `icon-192.png`: 192x192 icon
- `icon-512.png`: 512x512 icon

Place these in the `/static/` directory.

---

## 7. Advanced Geolocation

### Overview
Enhanced location features including nearby search, distance calculation, and heatmaps.

### Features
- Search annonces within radius
- Distance calculation using Haversine formula
- City and district aggregation
- Heatmap data for visualization

### API Endpoints

#### Search Nearby Annonces
```http
GET /api/v1/geolocation/nearby?latitude=14.7167&longitude=-17.4677&radius_km=10&category_id=5
```

Parameters:
- `latitude`: Latitude coordinate
- `longitude`: Longitude coordinate
- `radius_km`: Search radius in kilometers (default: 10, max: 100)
- `category_id`: Optional category filter
- `min_price`: Optional minimum price
- `max_price`: Optional maximum price

#### Get Popular Cities
```http
GET /api/v1/geolocation/cities
```

#### Get Districts by City
```http
GET /api/v1/geolocation/districts?city=Dakar
```

#### Get Heatmap Data
```http
GET /api/v1/geolocation/heatmap?category_id=5
```

### Distance Calculation
Uses Haversine formula for accurate distance calculation between two coordinates on Earth's surface.

---

## 8. Analytics and Statistics

### Overview
Comprehensive analytics system for tracking user activity, annonce performance, and platform metrics.

### Features
- View tracking for annonces
- Daily aggregated statistics
- User-specific analytics
- Global platform metrics
- Period comparisons (7 days, 30 days)

### API Endpoints

#### Track Annonce View
```http
POST /api/v1/analytics/views
Content-Type: application/json

{
  "annonce_id": 123,
  "ip_address": "192.168.1.1",
  "user_agent": "Mozilla/5.0..."
}
```

#### Get Analytics Summary
```http
GET /api/v1/analytics/summary?days=30
Authorization: Bearer {token}
```

#### Get User Analytics
```http
GET /api/v1/analytics/user/{user_id}
Authorization: Bearer {token}
```

Response:
```json
{
  "user_id": 123,
  "total_annonces": 15,
  "active_annonces": 10,
  "sold_annonces": 5,
  "total_views": 1250,
  "total_messages_received": 87,
  "total_favorites_received": 42,
  "average_rating": 4.5,
  "total_reviews": 12
}
```

#### Get Daily Stats
```http
GET /api/v1/analytics/daily-stats?days=30
Authorization: Bearer {token}
```

### Database Models
- `AnnonceView`: Individual view tracking
- `DailyStats`: Aggregated daily statistics

---

## Database Schema Updates

### New Tables

#### reviews
- `id`: Primary key
- `rating`: Float (1.0 to 5.0)
- `comment`: Text (optional)
- `reviewer_id`: Foreign key to users
- `reviewed_user_id`: Foreign key to users
- `annonce_id`: Foreign key to annonces (optional)
- `created_at`, `updated_at`: Timestamps

#### alerts
- `id`: Primary key
- `user_id`: Foreign key to users
- `title`: String
- `keywords`: String (optional)
- `category_id`: Foreign key to categories (optional)
- `location_city`: String (optional)
- `min_price`, `max_price`: Float (optional)
- `is_active`: Boolean
- `frequency`: Enum (instant, daily, weekly)
- `created_at`, `updated_at`, `last_triggered`: Timestamps

#### notifications
- `id`: Primary key
- `user_id`: Foreign key to users
- `type`: Enum (notification types)
- `title`: String
- `message`: Text
- `annonce_id`: Foreign key to annonces (optional)
- `related_user_id`: Foreign key to users (optional)
- `is_read`: Boolean
- `read_at`: Timestamp (optional)
- `is_push_sent`: Boolean
- `push_sent_at`: Timestamp (optional)
- `created_at`: Timestamp

#### annonce_views
- `id`: Primary key
- `annonce_id`: Foreign key to annonces
- `user_id`: Foreign key to users (optional)
- `ip_address`: String (optional)
- `user_agent`: String (optional)
- `viewed_at`: Timestamp

#### daily_stats
- `id`: Primary key
- `stat_date`: Date (unique)
- `new_users`, `active_users`: Integer
- `new_annonces`, `active_annonces`, `sold_annonces`: Integer
- `total_messages`, `total_views`, `total_favorites`: Integer
- `boost_revenue`: Float
- `created_at`, `updated_at`: Timestamps

---

## Migration Guide

### Backend Setup

1. Install dependencies (already in requirements.txt):
   - All required packages are already included

2. Run database migrations:
   ```bash
   cd backend
   # The tables will be created automatically on first run
   python -m uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Add app icons:
   - Create `icon-192.png` and `icon-512.png`
   - Place them in `frontend/static/`

2. Update API URLs:
   - Check all fetch calls use correct backend URL
   - Update in production environment

3. Test PWA:
   ```bash
   cd frontend
   npm run build
   npm run preview
   ```

---

## Security Considerations

### Admin Access
- Currently using `is_pro` flag as temporary admin indicator
- **Production**: Implement proper RBAC with admin roles
- Add middleware for admin route protection

### API Rate Limiting
- Implement rate limiting for public endpoints
- Use SlowAPI (already in requirements.txt)

### Notification Spam Prevention
- Limit alert creation per user
- Implement cooldown for notifications
- Add notification preferences

### Review System
- Prevent self-reviews (implemented)
- Limit reviews per user-pair
- Add review reporting system

---

## Future Enhancements

### Phase 3 Features
1. **Mobile Money Integration**
   - Orange Money, MTN Mobile Money, Moov Money
   - Payment processing for boosts

2. **Email/SMS Notifications**
   - Email service integration
   - SMS gateway for alerts

3. **Advanced Analytics Dashboard**
   - Charts and graphs
   - Export functionality
   - Custom date ranges

4. **Multi-language Support**
   - French, English, local languages
   - i18n implementation

5. **Map Integration**
   - Google Maps or OpenStreetMap
   - Interactive location picker
   - Route directions

6. **AI-Powered Features**
   - Smart pricing suggestions
   - Image recognition for categorization
   - Fraud detection

---

## API Documentation

Complete API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Support

For questions or issues:
1. Check the main README.md
2. Review this documentation
3. Open an issue on GitHub
4. Contact the development team

---

**Version**: 2.0.0  
**Last Updated**: November 2024  
**Status**: Production Ready
