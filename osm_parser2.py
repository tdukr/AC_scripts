import overpy
import shapefile
import time
import geojson


inshp = "area/reg_buff.shp"
sf = shapefile.Reader(inshp)
bbox = sf.bbox
in_tags = [['infrastructure', ['"amenity"= "fire_station"', '"amenity"= "police"', '"amenity"= "bus_station"',
                            '"amenity"= "fuel"', '"highway"="bus_stop"', '"shop"="car_repair"', '"amenity"="parking"',
                               '"amenity"= "post_office"', '"building"="office"', '"office"="government"',
                               '"government"="administrative"', '"amenity"="townhall"', '"boundary"="protected_area"',
                               '"office"="government"', '"landuse"="industrial"', '"landuse"="commercial"',
                               '"landuse"="farmyard"']]
            ]

def get_osm(tag):
    """
    requests data from OSM using Overpass API
    :param tag: OSM tag
    :return: dictionary {'node' : overpy.Result, 'way': overpy.Result, 'rel': [....]}
    """
    query = lambda rel_type: api.query("""({}({},{},{},{}) [{}];);(._;>;);out;"""
                                           .format(rel_type, bbox[1], bbox[0], bbox[3], bbox[2], tag))

    def query_rels(ids):
        while True:
            try:
                return api.query("""relation({});(._;>;);out;""".format(ids))
            except:
                time.sleep(4)

    api = overpy.Overpass()
    result = dict()
    do_queries = [['node', query('node')], ['way', query('way')],
         ['rel', [query_rels(ID) for ID in query('rel').get_relation_ids()]]]
    for q in do_queries:
        while True:
            try:
                result[q[0]] = q[1]
                break
            except:
                time.sleep(4)  # time delay for the next query 3 seconds in case of many requests
    return result


def all_unique(in_list):
    seen = list()
    return not any(l in seen or seen.append(l) for l in in_list)


def parse_osm(category_name, keys):
    """
    Downloads, parsers OSM data and saves each geometry type with parameters to separate .geojson files
    :param category_name: string; a name of the category to be downloaded
    :param keys: list; all OSM keys for this category with their values
    """
    print('----' + category_name + '----')
    print('Downloading OSM data...')
    keys = in_tags[0][1]
    res = get_osm(keys[0])
    for k in keys[1:]:
        ares = get_osm(k)       # {'node' : overpy.Result, 'way': overpy.Result, 'rel': [....]} for each key
        try:
            res['node'].expand(ares['node'])
        except KeyError:
            print('No nodes for the key  ' + k)
        try:
            res['way'].expand(ares['way'])
        except KeyError:
            print('No ways for the key  ' + k)
        try:
            res['rel'].extend(ares['rel'])
        except KeyError:
            print('No relations for the key  ' + k)
    print('Done')

    print('Obtaining geometry and key parameters...')
    objs = {'Point': {}, 'LineString': {'coords': [], 'params': []}, 'Polygon': {'coords': [], 'params': []},
            'MultiPolygon': {'coords': [], 'params': []}, 'MultiLineString': {'coords': [], 'params': []}}
    #Points
    objs['Point']['coords'] = [[float(node.lon), float(node.lat)] for node in res['node'].nodes]
    objs['Point']['params'] = [node.tags for node in res['node'].nodes]
    count = 0
    for node in res['node'].nodes:
        objs['Point']['params'][count]['osm_id'] = node.id
        count += 1
    #LineStrings and Polygons
    count = 0
    for way in res['way'].ways:
        crd = [[float(node.lon), float(node.lat)] for node in way.nodes]
        if all_unique(crd):
            objs['LineString']['coords'].append(crd)  # if all points in the 'way' object are unique
            objs['LineString']['params'].append(way.tags)
            objs['LineString']['params'][count]['osm_id'] = way.id
        else:  # if there is a shared point
            objs['Polygon']['coords'].append([crd])
            objs['Polygon']['params'].append(way.tags)
            objs['Polygon']['params'][count]['osm_id'] = way.id
        count += 1
        #MultiLineStrings and MultiPolygons

    count = 0
    for rres in res['rel']:
        mline = []
        mpoly = []
        for way in rres.ways:
            crd = [[float(node.lon), float(node.lat)] for node in way.nodes]
            if all_unique(crd):
                mline.append(crd)
            else:
                mpoly.append([crd])
        if mpoly:
            objs['MultiPolygon']['coords'].append(mpoly)
            objs['MultiPolygon']['params'].append(rres.relations[0].tags)
            objs['MultiPolygon']['params'][count]['osm_id'] = rres.relations[0].id
        if mline:
            objs['MultiLineString']['coords'].append(mline)
            objs['MultiLineString']['params'].append(rres.relations[0].tags)
            objs['MultiLineString']['params'][count]['osm_id'] = rres.relations[0].id
        count += 1
    print('Done')

    print('Exporting json files...')
    for geom in objs.keys():
        if objs[geom]['coords']:  # if this geom type has any objects in this tag, create a geojson file
            outjson = {"type": "FeatureCollection", "features": []}
            outname = 'osm/' + category_name + '_' + geom + '.geojson'
            for i in range(len(objs[geom]['coords'])):
                feat = {'type': 'Feature',
                        "name": category_name,
                        'geometry': {
                            "type": geom,
                            "coordinates": objs[geom]['coords'][i]
                        },
                        'properties': objs[geom]['params'][i]
                        }
                outjson['features'].append(feat)
            with open(outname, 'w') as outfile:
                geojson.dump(outjson, outfile, ensure_ascii=False)
    print('Done\n')

for ttag in in_tags:
    parse_osm(*ttag)
