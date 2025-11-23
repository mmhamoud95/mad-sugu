from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
from pydantic import BaseModel
import math

from ...api.deps import get_db
from ...models import Annonce, AnnonceStatus
from ...schemas.annonce import Annonce as AnnonceSchema

router = APIRouter()


class LocationUpdate(BaseModel):
    latitude: float
    longitude: float
    location_city: Optional[str] = None
    location_district: Optional[str] = None


class NearbySearch(BaseModel):
    latitude: float
    longitude: float
    radius_km: float = 10.0  # Default 10km radius


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two points using Haversine formula
    Returns distance in kilometers
    """
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c


@router.get("/nearby", response_model=List[AnnonceSchema])
def search_nearby_annonces(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(10.0, ge=0.1, le=100),
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Search for annonces near a specific location
    """
    # Base query for active annonces with coordinates
    query = db.query(Annonce).filter(
        and_(
            Annonce.status == AnnonceStatus.ACTIVE,
            Annonce.latitude.isnot(None),
            Annonce.longitude.isnot(None)
        )
    )
    
    # Apply filters
    if category_id:
        query = query.filter(Annonce.category_id == category_id)
    
    if min_price:
        query = query.filter(Annonce.price >= min_price)
    
    if max_price:
        query = query.filter(Annonce.price <= max_price)
    
    # Get all annonces (we'll filter by distance in Python)
    # In production, use PostGIS or spatial database for better performance
    all_annonces = query.all()
    
    # Filter by distance
    nearby_annonces = []
    for annonce in all_annonces:
        distance = calculate_distance(
            latitude, longitude,
            annonce.latitude, annonce.longitude
        )
        if distance <= radius_km:
            # Add distance as an attribute (not persisted)
            annonce.distance_km = round(distance, 2)
            nearby_annonces.append(annonce)
    
    # Sort by distance
    nearby_annonces.sort(key=lambda x: x.distance_km)
    
    # Apply pagination
    start = skip
    end = skip + limit
    
    return nearby_annonces[start:end]


@router.get("/cities")
def get_popular_cities(
    db: Session = Depends(get_db)
):
    """
    Get list of cities with annonce counts
    """
    cities = db.query(
        Annonce.location_city,
        func.count(Annonce.id).label('count')
    ).filter(
        and_(
            Annonce.status == AnnonceStatus.ACTIVE,
            Annonce.location_city.isnot(None)
        )
    ).group_by(
        Annonce.location_city
    ).order_by(
        func.count(Annonce.id).desc()
    ).limit(50).all()
    
    return [{"city": city, "count": count} for city, count in cities]


@router.get("/districts")
def get_districts_by_city(
    city: str = Query(..., description="City name"),
    db: Session = Depends(get_db)
):
    """
    Get districts for a specific city
    """
    districts = db.query(
        Annonce.location_district,
        func.count(Annonce.id).label('count')
    ).filter(
        and_(
            Annonce.status == AnnonceStatus.ACTIVE,
            Annonce.location_city == city,
            Annonce.location_district.isnot(None)
        )
    ).group_by(
        Annonce.location_district
    ).order_by(
        func.count(Annonce.id).desc()
    ).all()
    
    return [{"district": district, "count": count} for district, count in districts]


@router.get("/heatmap")
def get_annonces_heatmap(
    category_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Get annonces locations for heatmap visualization
    Returns list of coordinates with counts
    """
    query = db.query(
        Annonce.latitude,
        Annonce.longitude,
        func.count(Annonce.id).label('count')
    ).filter(
        and_(
            Annonce.status == AnnonceStatus.ACTIVE,
            Annonce.latitude.isnot(None),
            Annonce.longitude.isnot(None)
        )
    )
    
    if category_id:
        query = query.filter(Annonce.category_id == category_id)
    
    locations = query.group_by(
        Annonce.latitude,
        Annonce.longitude
    ).all()
    
    return [
        {
            "latitude": lat,
            "longitude": lon,
            "count": count
        }
        for lat, lon, count in locations
    ]
