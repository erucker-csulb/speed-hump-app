"""
 Tool Name:   CopyCollectorLayer
 Source Name: copy_collector_layer.py
 Author:      Ethan Rucker
 Required Arguments:
              The path to the Geodatabase Workspace
 Description: 
              Copies the Collector feature layer from ArcGIS Online to the Geodatabase.
              Deletes previous data from SpeedHumpAnalysis feature class and appends the
              collector data to the empty feature class. The copy of the survey layer is 
              then deleted.
"""

import arcpy, sys
from arcgis.gis import GIS
from arcgis.features import FeatureLayer

""" Local Variables """

url_gis = r"https://ladot.maps.arcgis.com"                                                                              # URL to AGOL or Portal
url_fl = r"https://services3.arcgis.com/vq5vGR4r1YX7ueLg/arcgis/rest/services/Speed_Hump_Layer/FeatureServer/0"         # URL for feature layer to download as feature class
user = arcpy.GetParameterAsText(1)                                                                                      # AGOL or Portal username
pwd = arcpy.GetParameterAsText(2)                                                                                       # user password
arcpy.env.workspace = arcpy.GetParameterAsText(0)                                                                       # path to file geodatabase
fc_copy = r"SpeedHumpCopy"                                                                                              # name of copied feature class
fc = r"SpeedHump\SpeedHumpAnalysis"                                                                                     # name of main speed hump feature class

try:
    """ Copy Layer from AGOL to GDB """

    gis = GIS(url_gis, user, pwd)
    fl = FeatureLayer(url_fl)
    fs = fl.query()
    fs.save(arcpy.env.workspace, fc_copy)

    """ Replace Features in Feature Class and Delete Copy """

    arcpy.DeleteRows_management(fc)
    arcpy.Append_management(fc_copy, fc, "NO_TEST")
    arcpy.Delete_management(fc_copy)
    arcpy.AddMessage("SUCCESS")
    
except Exception as err:
    """ Error Handling """

    arcpy.AddError(err)
    sys.exit(1)
