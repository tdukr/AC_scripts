import overpy
import shapefile
import urllib.request
import time
import geojson


inshp = "area/reg_buff.shp"
sf = shapefile.Reader(inshp)
bbox = sf.bbox
in_tags = [['natural', ['natural','name','amenity'], ['geological', 'landcover', 'waterway']],
           ['building', ['building', 'name', 'amenity'], ['shop', 'tourism']],
           ['boundary', ['boundary','name','admin_level','place','koatuu','population'], []],
            ['landuse', ['landuse','name','amenity'], ['aeroway', 'leisure', 'tourism']],
            ['highway', ['highway','name','amenity','int_ref','surface'], ['railway', 'trafic_sign','public_transport']],
            ['man_made', ['man_made','name','amenity',], ['power', 'office', 'shop', 'leisure', 'tourism', 'historic']],
            ['place', ['place','name','koatuu','population'], []],
            ['natural', ['natural','name','amenity'], ['geological', 'landcover']]]


def convert_int_none(x):
    try:
        if x == None:
            return ''
        else:
            return int(x)
    except ValueError:
        return x


def get_osm(tag):
    """
    requests data from OSM using Overpass API
    :param tag: OSM tag
    :return: dictionary {'node' : overpy.Result, 'way': overpy.Result, 'rel': [....]}
    """
    query = lambda rel_type: api.query("""({}({},{},{},{}) [{}];);(._;>;);out;"""
                                       .format(rel_type, bbox[1], bbox[0], bbox[3], bbox[2], tag.replace("'", '"')))

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


def get_params(obj, schema_fields, additional_tags):
    """
    :param obj: an overpy node/way/relation object
    :param schema: a list of keys for this tag
    :param additional_tags: other tags related to this tag
    :return: attribute values for each complete object (e.g. node, way or a component-way in a relation)
    """
    val = [obj.tags.get(tag) for tag in schema_fields]
    if not val[2]:  # if 'amenity' value does not exist, check if the object is from additional tags
        for t in additional_tags:
            val[2] = obj.tags.get(t)  # amenity = value of the tag
            if val[2]:
                val[0] = t # type = name of the tag
                break
        if not val[2]:  # if (after the check) the object is still not from the additional tags
            val[2] = ''
            val[0] = ''
    params = list(map(convert_int_none, val))  # try to convert to int and empty string/NULL
    return params


def all_unique(in_list):
    seen = list()
    return not any(l in seen or seen.append(l) for l in in_list)


def parse_osm(tag, schema, additional_tags):
    """
    Downloads, parsers OSM data and saves each geometry type with parameters to separate .geojson files
    :param tag: a string of an OSM tag
    :param schema: a list of strings of field names, which are OSM keys for this tag
    :param additional_tags: other related OSM tags for this tag
    """
    # get all results for this key/tag and expand them with results from additional tags
    res = get_osm(tag)
    for atag in additional_tags:
        ares = get_osm(atag)  # {'node' : overpy.Result, 'way': overpy.Result, 'rel': [....]} for each additional tag
        res['node'].expand(ares['node'])
        res['way'].expand(ares['way'])
        res['rel'].extend(ares['rel'])

    objs = {'Point': {}, 'LineString': {'coords': [], 'params': []}, 'Polygon': {'coords': [], 'params': []},
            'MultiPolygon': {}}
    objs['Point']['coords'] = [[float(node.lon), float(node.lat)] for node in res['node'].nodes]
    objs['Point']['params'] = [get_params(node, schema, additional_tags) for node in res['node'].nodes]
    objs['MultiPolygon']['coords'] = [
        [[[[float(node.lon), float(node.lat)] for node in way.nodes]] for way in rres.ways] for rres in
        res['rel']]  # has len(rel['coords']) objects; each has len(rel['coords'][i]) ways
    objs['MultiPolygon']['params'] = [get_params(rres.relations[0], schema, additional_tags) for rres in
                                      res['rel']]  # here rres represents only one relation/MultiPolygon object
    for way in res['way'].ways:
        coord = [[float(node.lon), float(node.lat)] for node in way.nodes]
        if all_unique(coord):
            objs['LineString']['coords'].append(coord)  # if all points in the 'way' object are unique
            objs['LineString']['params'].append(get_params(way, schema, additional_tags))
        else:  # if there is a shared point
            objs['Polygon']['coords'].append([coord])
            objs['Polygon']['params'].append(get_params(way, schema, additional_tags))

    # export json
    schema = list(map(lambda x: x[:10], schema))  # shorten field names to 10 characters
    schema[0] = 'type'  # rename the first field to 'type'
    for key in objs.keys():
        if objs[key]['coords']:  # if this geom type has any objects in this tag, create a geojson file
            outjson = {"type": "FeatureCollection", "features": []}
            outname = tag + '_' + key + '.geojson'
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


for in_tag in in_tags:
    parse_osm(in_tag[0], in_tag[1], in_tag[2])