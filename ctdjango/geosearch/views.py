import math
from django.shortcuts import render_to_response
from django.conf import settings
from linkedct.models import *
import databrowse
from databrowse.datastructures import *
from geopy import geocoders, distance

def map_view(request):

    databrowse.site.root_url = settings.CONFIG['ROOT']
    countries = Country.objects.all().order_by('country_name')

    country = 'Canada'
    city = 'Toronto'
    dist = '5'
    condition = ''

    input_error = False
    geo_error = False
    over_max = False
    no_result = False
    error = False

    inputs = request.GET
    if ('country' in inputs) and ('city' in inputs) and ('distance' in inputs) and ('condition' in inputs):

        country = inputs.get('country')
        city = inputs.get('city')
        dist = inputs.get('distance')
        condition = inputs.get('condition')


        if not country or not city or not dist or not condition:
            input_error = True


        elif float(dist) > 50 or float(dist) < 0:
            over_max = True

        else:
            g = geocoders.GoogleV3()
            try:
                _, (lat, lng) = g.geocode(city+','+country, exactly_one=False)[0]
            except:
                geo_error = True
                error = True


            radius = float(dist)
            if not error:
                lat_diff = radius/69
                lng_diff = radius/abs(math.cos(math.radians(lat))*69)
                lat1 = str(lat - lat_diff)
                lat2 = str(lat + lat_diff)
                lng1 = str(lng - lng_diff)
                lng2 = str(lng + lng_diff)
                coords = Coordinates.objects.select_related('address', 'latitude', 'longitude', 'address__country__country_name').\
                                             filter(address__country__country_name = country,
                                                    latitude__range=(lat1, lat2),
                                                    longitude__range=(lng1,lng2)).values_list('address', 'latitude', 'longitude')

                within = []
                for c in coords:
                    if distance.distance((lat,lng), (float(c[1]),float(c[2]))).miles < radius:
                        within.append(c)

                if not within:
                    no_result = True
                    error = True

            if not error:
                conds = Condition.objects.select_related('label', 'slug').filter(label__icontains=condition).values_list('slug', flat=True)
                trials = Trial.objects.only('conditions__slug').filter(conditions__slug__in=conds).distinct()

                if not trials:
                    no_result = True
                    error = True


            trials_dict = {}
            if not error:
                for c in within:
                    ts = trials.filter(locations__facility__address__in = [c[0]])[:4].count()
                    if ts:
                        trials_dict[c] = ts
                if not trials_dict:
                    no_result = True
                    error = True


            if not error:
                return render_to_response('geosearch/map_results.html',
                       {'coordinates': (lat, lng),  'trials': trials_dict.items(), 'countries': countries,
                        'country':country, 'city':city, 'distance':dist, 'condition':condition, 'root_url': databrowse.site.root_url})

    return render_to_response('geosearch/map.html',
           {'input_error': input_error, 'geo_error': geo_error, 'over_max': over_max, 'no_result': no_result,
            'countries': countries, 'country':country, 'city':city, 'distance':dist,
            'condition':condition, 'root_url': databrowse.site.root_url})


def map_search_result_view(request):

    error = False
    databrowse.site.root_url = settings.CONFIG['ROOT']

    inputs = request.GET
    if ('location' in inputs) and ('condition' in inputs):
        location_addr = inputs.get('location')
        condition = inputs.get('condition')

        if not location_addr or not condition:
            error = True

        else:
            trial_m = EasyModel(databrowse.site, Trial)
            cond_list = Condition.objects.filter(label__icontains=condition).values_list('slug', flat=True)
            trials = Trial.objects.only('locations__facility__address','conditions__slug').filter(locations__facility__address__in=[location_addr],\
            																					  conditions__slug__in=cond_list).distinct()

            facilities = []
            for t in trials:
                for l in t.locations.only('facility', 'facility__address').filter(facility__address=location_addr).distinct():
                    if l.facility.facility_name not in facilities:
                        facilities.append(l.facility.facility_name)

            facility_dict = {}
            for f in facilities:
                trial_dict = {}
                for t in trials.only('locations__facility', 'conditions').filter(locations__facility__facility_name=f):
                    trial_dict[EasyInstance(trial_m, t)] = t.conditions.all()
                facility_dict[f] = trial_dict

            return render_to_response('geosearch/map_search_result.html',
                                                {'trials':facility_dict,
                                                 'address': Address.objects.get(slug = location_addr),
                                                 'condition': condition,
                                                 'root_url': databrowse.site.root_url})

    return render_to_response('geosearch/map_search_result.html',
                                        {'error':error, 'root_url': databrowse.site.root_url})
