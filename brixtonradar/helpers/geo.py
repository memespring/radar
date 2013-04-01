import urllib
import re
import sys
import json
import time

def streets():
    return [
"Dalyell Road",
"Pulross Road",
"Bellefields Road",
"Gateley Road",
"Nursery Road",
"Brighton Terrace",
"Ferndale Road",
"Trinity Gardens",
"Bernay's Grove",
"Beehive Place",
"Astoria Walk",
"Stockwell Avenue",
"Porden Road",
"Buckner Road",
"Arlington Parade",
"Baytree Road",
"Atlantic Road",
"Railton Road",
"Electric Avenue",
"Electric Lane",
"Pope's Road",
"Popes Road",
"Canterbury Crescent",
"Brixton Station Road",
"Gresham Road",
"Barrington Road",
"Wiltshire Road",
"Valentia Place",
"Saltoun Road",
"Kellett Road",
"Rushcroft Road",
"Vining Street",
"Rattray Road",
"Marcus Garvey Way",
"Bob Marley Way",
"Mayall Road",
"Somerleyton Road",
"Geneva Drive",
"Broughton Drive",
"Eaton Drive",
"Corry Drive",
"Clifford Drive",
"Moorland Road",
"Coldhabour Lane",
"Dalberg Road",
"Barnwell Road",
"Effra Parade",
"Southwyck House",
"Hillmead Drive",
"Tilia Walk",
"Market Row",
]

def is_local(latlng):

    result = False

    top_left={'lat':51.46532, 'lng': -0.1219}
    top_right={'lat':51.46548, 'lng': -0.1044}
    bottom_right={'lat':51.45540, 'lng': -0.1039}
    bottom_left={'lat':51.45526, 'lng': -0.1221}

    if latlng['lng'] >= top_left['lng'] and latlng['lng'] <= top_right['lng']:
        if latlng['lat'] > bottom_left['lat'] and latlng['lat'] <= top_left['lat']:
            result = True

    return result

def postcode_latlng(postcode):
    result = False
    time.sleep(0.5) # wait before calling
    try:
        url = "http://mapit.mysociety.org/postcode/%s.json" % urllib.quote(postcode)
        data = json.load(urllib.urlopen(url))
        result = {'lat': data['wgs84_lat'], 'lng': data['wgs84_lon']}
    except:
        print 'failed to get location from postcode'

    return result

def extract_gb_postcode(string):
    postcode = False
    matches = re.findall(r'[A-Z][A-Z]?[0-9][A-Z0-9]? ?[0-9][ABDEFGHJLNPQRSTUWXYZ]{2}\b', string, re.IGNORECASE)

    if len(matches) > 0:
        postcode = matches[0]

    return postcode


