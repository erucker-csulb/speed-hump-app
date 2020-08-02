import arcpy
from arcgis.gis import GIS
from arcgis.features import FeatureLayer

## LOCAL VARIABLES ##

url_gis = r"https://ladot.maps.arcgis.com" # URL to AGOL or Portal
url_fl = r"https://services3.arcgis.com/vq5vGR4r1YX7ueLg/arcgis/rest/services/SpeedHump_Survey123/FeatureServer/0" # URL for feature layer to download as feature class
user = "lan.nguyen_ladot" # AGOL or Portal username
pwd = "william.ha2020" # user password
arcpy.env.workspace = arcpy.GetParameterAsText(0) # path to file geodatabase
edit = arcpy.da.Editor(arcpy.env.workspace) # enables edits to the GDB
fc_copy = "SpeedHumpCopy" # name of copied feature class
fc = r"SpeedHump/SpeedHumpAnalysis" # name of main speed hump feature class

try:
    ## COPY LAYER FROM AGOL TO GDB ##

    gis = GIS(url_gis, user, pwd)
    fl = FeatureLayer(url_fl)
    fs = fl.query()
    fs.save(arcpy.env.workspace, fc_copy)

    ## APPEND FEATURES TO FEATURE CLASS AND DELETE COPY ##

    arcpy.DeleteRows_management(fc)

    edit.startEditing(False, True)
    edit.startOperation()

    arcpy.Append_management(fc_copy, fc, "TEST")

    edit.stopOperation()
    edit.stopEditing(True)

    arcpy.Delete_management(fc_copy)

## ERROR HANDLING ##

except arcpy.ExecuteError:
    print("ArcPy FAILED:")
    print(arcpy.GetMessages(2))
    
except Exception as err:
    print("Python FAILED:")
    print(err.args[0])
