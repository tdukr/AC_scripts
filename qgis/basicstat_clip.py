from qgis import *
from qgis.core import *
from qgis.utils import *
from qgis.gui import *
import processing
import os

 
def clipper(directory, mask):
    file_list = os.listdir(directory)
    stats = open(directory + 'basicstat.txt', 'w')
    stats.write('name;features_obl;features_1buff;features_2buff\n')

    for file in file_list:
        if file.endswith('.shp'):
            layer = QgsVectorLayer(directory + file, file, 'ogr')
            
            # set layer crs
            crs = layer.crs()
            crs.createFromId(5564)
            layer.setCrs(crs)
            
            # set encoding
            layer.setProviderEncoding(u'System')
            layer.dataProvider().setEncoding(u'System')
            
            QgsMapLayerRegistry.instance().addMapLayer(layer)

            # clip layer
            processing.runalg("qgis:clip", directory + file, mask, directory + "clipped/" + file)
            clippedlayer = QgsVectorLayer(directory + "clipped/" + file, file, 'ogr')

            # count objects in region
            stats.write(file + ';' + str(layer.getFeatures()) + ';')

            #count clipped objects
            stats.write(str(clippedlayer.getFeatures()) + ';')

            #count clipped objects
            stats.write(str(clipped_2layer.getFeatures()) + '\n')
    stats.close()


dir_to_clip = "osm/"
clip_mask = "area/reg_buff.shp"
clipper(dir_to_clip, clip_mask)
