from qgis import *
from qgis.core import *
from qgis.utils import *
from qgis.gui import *
import processing
import os
 
# Set the directory where the input files are stored
directory = "E:/desktop/BAGACHKA/OPORA/"
 
# Get the list of input files
fileList = os.listdir(directory)

file_output = open('E:/desktop/DataProcessing/basicstat.txt', 'w')

# csv attributes names
file_output.write('name;features_obl;features_1buff;features_2buff\n')
 
def clipper(fileList):
    # Copy the features from all the files in a new list
    for file in fileList:
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
            
            #count objects in region
            count = 0
            for f in layer.getFeatures():
                count = count + 1
            print file, 'containts ', count, 'features'
            file_output.write(file + ';' + str(count) + ';')
            
            #clip layer by priority zone 1
            processing.runalg("qgis:clip",directory + file,"E:/desktop/DataProcessing/shp/border/1_border_buff.shp","E:/desktop/DataProcessing/shp/clipped/1_" + file)
            
            clippedlayer = QgsVectorLayer("E:/desktop/DataProcessing/shp/clipped/1_" + file, file, 'ogr')
            
            #count clipped objects
            count = 0
            for f in clippedlayer.getFeatures():
                count = count + 1
            print '1_' + file, 'containts ', count, 'features'
            file_output.write(str(count) + ';')
            
            #clip layer by priority zone 2
            processing.runalg("qgis:clip",directory + file,"E:/desktop/DataProcessing/shp/border/2_border_buff.shp","E:/desktop/DataProcessing/shp/clipped/2_" + file)
            
            clipped_2layer = QgsVectorLayer("E:/desktop/DataProcessing/shp/clipped/2_" + file, file, 'ogr')
            
            #count clipped objects
            count = 0
            for f in clipped_2layer.getFeatures():
                count = count + 1
            print '2_' + file, 'containts ', count, 'features'
            file_output.write(str(count) + '\n')
            
clipper(fileList)
file_output.close()
#def Clipper()