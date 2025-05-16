from listing.models import Postcodes

def get_postcodes_by_location():
    postcodes_by_location = {}
    for row in Postcodes.objects.values('postcode', 'location'):
        location = row['location']
        if location not in postcodes_by_location:
            postcodes_by_location[location] = []
        postcodes_by_location[location].append(row['postcode'])
    return postcodes_by_location