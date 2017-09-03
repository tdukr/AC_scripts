# POLYGONS
# building=*
# If the object has also tag 'shop=*' or 'tourism=*', key (e.g. 'shop') has to be written in 'type' and value (e.g. 'convenience') has to be written in 'amenity'
'building' = [['type','C',50,0],['name','C',254,0],['amenity','C',50,0]] 

# boundary=*
'boundary' = [['type','C',50,0],['name','C',254,0],['admin_level','N',0],['place','C',50,0],['koatuu','C',20,0],['population','N',0]]

# natural=*
# If the object has also tag 'geological=*' or 'landcover=*', key (e.g. 'landcover') has to be written in 'type' and value (e.g. 'grass') has to be written in 'amenity'
'natural' = [['type','C',50,0],['name','C',254,0],['amenity','C',50,0]]

# landuse=*
# Includes also objects with tags 'aeroway=*', 'leisure=*' or 'tourism=*' (if it is not a building), where key (e.g. 'aeroway') stores in 'type' and its value stores in 'amenity'
'landuse' = [['type','C',50,0],['name','C',254,0],['amenity','C',50,0]]

# amenity=* 
# має зберігати лише ті об'єкти, яких немає в 'building=*', 'boundary=*', 'natural=*' та 'landuse=*'
'amenity' = [['type','C',50,0,],['name','C',254,0]]



# LINES
# highway=*
# Includes also objects with tags 'railway=*', where key (e.g. 'railway') stores in 'type' and its value stores in 'amenity'
'highway' = [['type','C',50,0],['name','C',254,0],['int_ref','C',254,0],['surface','C',50,0],['amenity','C',50,0]]

# boundary=*
'boundary' = [['type','C',50,0],['name','C',254,0],['admin_level','N',0]]

# natural=*
# Includes also objects with tags 'waterway=*', where key (e.g. 'waterway') stores in 'type' and its value stores in 'amenity'
'natural' = [['type','C',50,0,],['name','C',254,0],['amenity','C',50,0]]

# man_made=*
# Includes also objects with tags power=*', where key (e.g. 'power') stores in 'type' and its value stores in 'amenity'
'man_made' = [['type','C',50,0],['name','C',254,0],['amenity','C',50,0]]


# POINTS
# highway=*
# Includes also objects with tags 'trafic_sign=*', railway=*' or 'public_transport=*', where key (e.g. 'public_transport') stores in 'type' and its value stores in 'amenity'
'highway' = [['type','C',50,0],['name','C',254,0],['amenity','C',50,0]]

# place=*
'place' = [['type','C',50,0],['name','C',254,0],['koatuu','C',20,0],['population','N',0]]

# natural=*
# If the object has also tag 'geological=*' or 'landcover=*', key ('landcover', for instance) has to be written in 'type' and value ('grass', for instance) has to be written in 'amenity'
'natural' = [['type','C',50,0],['name','C',254,0],['amenity','C',50,0]]

# man_made=*
# Includes also objects with tags 'historic=*', office=*', 'shop=*', power=*', 'leisure=*' or 'tourism=*', where key (e.g. 'tourism') stores in 'type' and its value stores in 'amenity'
'man_made' = [['type','C',50,0],['name','C',254,0],['amenity','C',50,0]]

# amenity=*
# має зберігати лише ті об'єкти, яких немає в 'highway=*', 'place=*', 'natural=*' та 'man_made=*' 
'amenity' = [['type','C',50,0,],['name','C',254,0]]