import sys
import os
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *

app = QApplication([])
QgsApplication.setPrefixPath("/usr", True)
QgsApplication.initQgis()

sys.path.append('/usr/share/qgis/python/plugins')
from processing.core.Processing import Processing
from processing.tools import *
Processing.initialize()
#from processing.runalg import *

clip_mask = "/home/polina/Projects/AC_scripts/area/reg_buff.shp"
dir_path = "/home/polina/Projects/AC_scripts/osm/"
print dir_path

def clipper(jsonf):
    layer = QgsVectorLayer(os.path.join(dir_path, jsonf), jsonf.rstrip('.geojson'), 'ogr')

    # set layer crs
    crs = layer.crs()
    crs.createFromId(5564)
    layer.setCrs(crs)

    # set encoding
    layer.setProviderEncoding(u'System')
    layer.dataProvider().setEncoding(u'System')

    QgsMapLayerRegistry.instance().addMapLayer(layer)

    # clip layer
    output = os.path.join(dir_path, "clipped", jsonf)
    general.runalg('gdalogr:clipvectorsbypolygon', jsonf, clip_mask, output)  #"qgis:clip"
    #clippedlayer = QgsVectorLayer(directory + "clipped/" + file, file, 'ogr')



for fname in os.listdir(dir_path):
    print fname
    if fname.endswith('.geojson'):
            clipper(fname)

QgsApplication.exitQgis()
