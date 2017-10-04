import overpy
import shapefile
import time
import geojson


inshp = "area/reg_buff.shp"
sf = shapefile.Reader(inshp)
bbox = sf.bbox
in_tags = [['amenity', ['amenity', 'name'], ['natural', 'building', 'landuse', 'boundary'], 2],
           ['building', ['building', 'name', 'amenity'], [], 0],
           ['natural', ['natural', 'name', 'amenity'], ['geological', 'landcover', 'waterway'], 0],
           ['boundary', ['boundary', 'name', 'admin_level', 'place', 'koatuu', 'population'], [], 0],
           ['landuse', ['landuse', 'name', 'amenity'], ['aeroway', 'leisure', 'tourism'], 0],
           ['highway', ['highway', 'name', 'amenity', 'int_ref', 'surface'],
            ['railway', 'trafic_sign', 'public_transport'], 0],
           ['man_made', ['man_made', 'name', 'amenity'],
            ['power', 'office', 'shop', 'leisure', 'tourism', 'historic'], 0],
           ['place', ['place', 'name', 'koatuu', 'population'], [], 0],
           ]


def convert_int_none(x):
    try:
        if x == None:
            return ''
        else:
            return int(x)
    except ValueError:
        return x


def get_osm(tag, yeskey=0, maintag=0):
    """
    requests data from OSM using Overpass API
    :param tag: OSM tag
    :return: dictionary {'node' : overpy.Result, 'way': overpy.Result, 'rel': [....]}
    """
    if yeskey == 0:
        query = lambda rel_type: api.query("""({}({},{},{},{}) [{}];);(._;>;);out;"""
                                           .format(rel_type, bbox[1], bbox[0], bbox[3], bbox[2], tag.replace("'", '"')))
    elif yeskey == 1:
        #asks that maintag for this tag == 'yes'
        query = lambda rel_type: api.query("""({}({},{},{},{}) [{}][{}='yes'];);(._;>;);out;"""
                                           .format(rel_type, bbox[1], bbox[0], bbox[3], bbox[2],\
                                                   tag.replace("'", '"'), maintag.replace("'", '"'),))
    elif yeskey == 2:
        #asks for objects that do not have tags from additional_tags (here tag is a list of them)
        def query(rel_type):
            qry = """({}({},{},{},{})[{}]"""\
                    .format(rel_type, bbox[1], bbox[0], bbox[3], bbox[2],maintag.replace("'", '"'))
            for t in tag:
                t = t.replace("'", '"')
                qry += '[{}!~".*"]'.format(t)
            qry += """;);(._;>;);out;"""
            return api.query(qry)

    def query_rels(ids):
        while True:
            try:
                return api.query("""relation({});(._;>;);out;""".format(ids))
            except:
                time.sleep(4)

    api = overpy.Overpass()
    while True:
        try:
            result = dict()
            result['node'] = query('node')
            result['way'] = query('way')
            result['rel'] = [query_rels(ID) for ID in query('rel').get_relation_ids()]
            return result
        except:
            time.sleep(4)  # time delay for the next query 3 seconds in case of many requests


def get_params(obj, schema_fields, main_tag, additional_tags):
    """
    :param obj: an overpy node/way/relation object
    :param schema: a list of keys for this tag
    :param additional_tags: other tags related to this tag
    :return: attribute values for each complete object (e.g. node, way or a component-way in a relation)
    """
    if main_tag == 'amenity':
        return list(map(convert_int_none, [obj.tags.get(tag) for tag in schema_fields]))
    else:
        params = [obj.tags.get(tag) for tag in schema_fields]
        for t in additional_tags:       # if 'amenity' value does not exist, check if the object is from additional tags
            params[2] = obj.tags.get(t)    # amenity = value of the tag
            if params[2]:
                params[0] = t              # type = name of the tag
                break
        return list(map(convert_int_none, params))  # try to convert to int and empty string/NULL


def all_unique(in_list):
    seen = list()
    return not any(l in seen or seen.append(l) for l in in_list)


def parse_osm(tag, schema, additional_tags, yes_key):
    """
    Downloads, parsers OSM data and saves each geometry type with parameters to separate .geojson files
    :param tag: a string of an OSM tag
    :param schema: a list of strings of field names, which are OSM keys for this tag
    :param additional_tags: other related OSM tags for this tag
    """
    # get all results for this key/tag and expand them with results from additional tags
    print('----' + tag + '----')
    print('Downloading OSM data...')
    res = get_osm(tag)
    if yes_key != 2:
        for atag in additional_tags:
            ares = get_osm(atag, yes_key, tag)  # {'node' : overpy.Result, 'way': overpy.Result, 'rel': [....]} for each additional tag
            res['node'].expand(ares['node'])
            res['way'].expand(ares['way'])
            res['rel'].extend(ares['rel'])
    else:
        ares = get_osm(additional_tags, yes_key, tag)  #pass a list of keys for a query in atag value
        res['node'].expand(ares['node'])
        res['way'].expand(ares['way'])
        res['rel'].extend(ares['rel'])
    print('Done')

    print('Obtaining geometry and key parameters...')
    objs = {'Point': {}, 'LineString': {'coords': [], 'params': []}, 'Polygon': {'coords': [], 'params': []},
            'MultiPolygon': {'coords': [], 'params': []}, 'MultiLineString': {'coords': [], 'params': []}}
    #Points
    objs['Point']['coords'] = [[float(node.lon), float(node.lat)] for node in res['node'].nodes]
    objs['Point']['params'] = [get_params(node, schema, tag, additional_tags) for node in res['node'].nodes]
    #LineStrings and Polygons
    for way in res['way'].ways:
        crd = [[float(node.lon), float(node.lat)] for node in way.nodes]
        if all_unique(crd):
            objs['LineString']['coords'].append(crd)  # if all points in the 'way' object are unique
            objs['LineString']['params'].append(get_params(way, schema, tag, additional_tags))
        else:  # if there is a shared point
            objs['Polygon']['coords'].append([crd])
            objs['Polygon']['params'].append(get_params(way, schema, tag, additional_tags))
    #MultiLineStrings and MultiPolygons
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
            objs['MultiPolygon']['params'].append(get_params(rres.relations[0], schema, tag, additional_tags))
        if mline:
            objs['MultiLineString']['coords'].append(mline)
            objs['MultiLineString']['params'].append(get_params(rres.relations[0], schema, tag, additional_tags))
    print('Done')

    print('Exporting json files...')
    schema = list(map(lambda x: x[:10], schema))  # shorten field names to 10 characters
    schema[0] = 'type'  # rename the first field to 'type'
    for key in objs.keys():
        if objs[key]['coords']:  # if this geom type has any objects in this tag, create a geojson file
            outjson = {"type": "FeatureCollection", "features": []}
            outname = 'osm/' + tag + '_' + key + '.geojson'
            for i in range(len(objs[key]['coords'])):
                feat = {'type': 'Feature',
                        'geometry': {
                            "type": key,
                            "coordinates": objs[key]['coords'][i]
                        },
                        'properties': dict(zip(schema, objs[key]['params'][i]))
                        }
                outjson['features'].append(feat)
            with open(outname, 'w') as outfile:
                geojson.dump(outjson, outfile)
    print('Done\n')

for tt in in_tags:
    parse_osm(*tt)
    break
