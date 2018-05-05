from geocode import getGeocodeLocation
import json
import requests

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

from credentials import foursquare_client_id, foursquare_client_secret

import datetime

def findARestaurant(mealType,location):
    #1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
    
    #2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
    #HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi

    #3. Grab the first restaurant
    #4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
    #5. Grab the first image
    #6. If no image is available, insert default a image url
    #7. Return a dictionary containing the restaurant name, address, and image url

    lat, lng = getGeocodeLocation(location)
    url = 'https://api.foursquare.com/v2/venues/search'
    params = dict(
        client_id=foursquare_client_id,
        client_secret=foursquare_client_secret,
        v=datetime.datetime.now().strftime("%Y%m%d"),
        ll=str(lat)+","+str(lng),
        query=mealType,
        limit=1
        )
    resp = requests.get(url=url, params=params)
    venue = json.loads(resp.text)['response']['venues'][0]
    
    venue_id = venue['id']
    pictureUrl = ('https://api.foursquare.com/v2/venues/%s/photos'
                  % venue_id)
    pic_params = dict(
        venue_id=venue_id,
        client_id=foursquare_client_id,
        client_secret=foursquare_client_secret,
        v=datetime.datetime.now().strftime("%Y%m%d"),
        limit=1
        )
    pic_resp = requests.get(url=pictureUrl, params=pic_params)
    picture = json.loads(pic_resp.text)['response']['photos']['items']
    
    if ( picture ):
        pic_link = picture[0]['prefix'] + "300x300" + picture[0]['suffix']
    else:
        pic_link = 'http://via.placeholder.com/300x300?text=placeholder'

    address = ""
    for s in venue['location']['formattedAddress']:
        address += s + " "
    info = {
        'name': venue['name'],
        'address': address,
        'image_url': pic_link
        }
    print("Restaurant Name: %s\nRestaurant Address: %s\nImage: %s\n" %(info['name'], info['address'], info['image_url']) )
    return info


if __name__ == '__main__':
    findARestaurant("Pizza", "Tokyo, Japan")
    findARestaurant("Tacos", "Jakarta, Indonesia")
    findARestaurant("Tapas", "Maputo, Mozambique")
    findARestaurant("Falafel", "Cairo, Egypt")
    findARestaurant("Spaghetti", "New Delhi, India")
    findARestaurant("Cappuccino", "Geneva, Switzerland")
    findARestaurant("Sushi", "Los Angeles, California")
    findARestaurant("Steak", "La Paz, Bolivia")
    findARestaurant("Gyros", "Sydney Australia")
