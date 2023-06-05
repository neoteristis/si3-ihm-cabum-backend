import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on the Earth's surface using the Haversine formula.
    
    Args:
    - lat1, lon1: Latitude and longitude of the first point in decimal degrees.
    - lat2, lon2: Latitude and longitude of the second point in decimal degrees.
    
    Returns:
    - The distance between the two points in kilometers.
    """
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        print("One of the latitude/longitude values is None.")
        return None
    
    R = 6371  # Radius of the Earth in kilometers
    
    # Convert latitude and longitude to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Calculate the differences between the latitudes and longitudes
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Calculate the square of half the chord length between the points
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    
    # Calculate the angular distance in radians
    c = 2 * math.asin(math.sqrt(a))
    
    # Calculate the distance in kilometers
    d = R * c
    
    return d