import requests
import os
from amadeus import Client, ResponseError


def get_flights(originAirportCode: str, destinationAirportCode: str, departureDate: str, number_of_passengers: int):
    """
    Performs a search to list flights available from origin city to destination city on a given departureDate for give number of passengers

    Args:
        origin (str): the start city airport code
        destination (str): the destination city airport code
        departureDate (str): the departure date in format 'yyyy-mm-dd'
        number_of_passengers (int): the number of passengers

    Returns:
        dict: The JSON response from the Amadeus API, or None if the request fails.
    """

    # Initialize client
    amadeus = Client(
        client_id=os.getenv('AMADEUS_CLIENT_ID'),
        client_secret=os.getenv('AMADEUS_CLIENT_SECRET')
    )

    try:
        # Search for flights
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=originAirportCode,      # Bangalore
            destinationLocationCode=destinationAirportCode,  # Delhi
            departureDate=departureDate,
            adults=number_of_passengers
        )

        responses = []

        # Display results
        for flight in response.data:
            response = {}
            response['price']  = flight['price']['total']
            response['currency'] = flight['price']['currency']
            response['segments'] = []
            for itinerary in flight['itineraries']:
                for segment in itinerary['segments']:
                    dep = segment['departure']
                    arr = segment['arrival']
                    response['segments'].append({'departFrom': dep, 'arriveAt': arr})
            responses.append(response)
        
        return responses
                    
    except ResponseError as error:
        print(f"Error: {error}")
        return None


def get_hotels(cityCode: str, checkInDate: str, checkOutDate: str, number_of_adults: int = 1, number_of_rooms: int = 1):
    """
    Lists hotels by city, extracts hotelIds, then fetches offers for all the hotels.
    
    Args:
        cityCode (str): IATA city code
        checkInDate (str): check in date in the format 'yyyy-mm-dd'
        checkOutDate (str): check in date in the format  'yyyy-mm-dd'
        number_of_adults (int): number of Adults
        number_of_rooms (int): number of Rooms required
        
    Returns:
        hotels_offers (list): List of hotels with offers, empty list if no hotel found
    """
    amadeus = Client(
        client_id=os.getenv('AMADEUS_CLIENT_ID'),
        client_secret=os.getenv('AMADEUS_CLIENT_SECRET')
    )

    try:
        # Step 1: Get hotel list for the city
        hotels_list_response = amadeus.reference_data.locations.hotels.by_city.get(
            cityCode=cityCode
        )
        hotels_with_offers = []
        # PERFORMANCE-NOTE: This loop makes one API call per hotel. The Amadeus API
        # supports passing a comma-separated list of `hotelIds` to get offers for multiple
        # hotels in a single request, which is much more efficient.
        for hotel in hotels_list_response.data[:20]:
            print(hotel)
            hotelId = hotel['hotelId']
            # Step 2: Get offers for this hotelId only
            try:
                offers_response = amadeus.shopping.hotel_offers_search.get(
                    hotelIds=hotelId,
                    checkInDate=checkInDate,
                    checkOutDate=checkOutDate,
                    adults=number_of_adults,
                    roomQuantity=number_of_rooms
                )
                for offer in offers_response.data:
                    print(offer)
                    hotel_offers = []
                    for h_offer in offer['offers']:
                        hotel_offers.append({
                            'checkIn': h_offer['checkInDate'],
                            'checkOut': h_offer['checkOutDate'],
                            'price': h_offer['price']['total'],
                            'currency': h_offer['price']['currency']
                        })
                    hotels_with_offers.append({
                        'hotelId': hotelId,
                        'name': hotel['name'],
                        # 'latitude': hotel['geoCode']['latitude'],
                        # 'longitude': hotel['geoCode']['longitude'],
                        # 'country': hotel['address']['countryCode'],
                        # 'distance': hotel['distance']['value'],
                        # 'distanceUnit': hotel['distance']['unit'],
                        'offers': hotel_offers
                    })
            except ResponseError as error:
                print(f"Could not get offers for hotelId {hotelId}: {error}")
                continue
        return hotels_with_offers
    except ResponseError as error:
        print(f"Error: {error}")
        return []


def get_tourist_attractions(place:str):
    """
    Performs a text search for tourist attractions in a given location using the Google Places API (v1).

    Args:
        place (str): The location to search for tourist attractions in (e.g., "Paris").

    Returns:
        dict: The JSON response from the Google Places API, or None if the request fails.
    """
    url = "https://places.googleapis.com/v1/places:searchText"
    query = f"tourist attractions in {place}"
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.name,places.primaryType,places.types,places.location,places.editorialSummary,places.generativeSummary,places.neighborhoodSummary,places.reviewSummary,places.rating,places.websiteUri,places.displayName,places.id,nextPageToken"
    }

    data = {
        "textQuery": query
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request to Google Places API: {e}")
        return None