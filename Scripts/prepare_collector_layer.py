"""
 Tool Name:   PrepareCollectorLayer
 Source Name: prepare_collector_layer.py
 Author:      Ethan Rucker
 Required Arguments:
              The path to the Geodatabase Workspace
 Description: 
              Copies the data from the Analysis feature class to the Collector feature 
              class in preparation to overwrite the Collector layer on ArcGIS Online.
              Deletes previous data from SpeedHump_Collector feature class and appends 
              the analysis data to the empty feature class.
"""

import arcpy, sys

""" Local Variables """

arcpy.env.workspace = arcpy.GetParameterAsText(0)                                                                       # path to file geodatabase
fc_from = r"SpeedHump\SpeedHumpAnalysis"                                                                                              # name of copied feature class
fc_to = r"SpeedHump\SpeedHump_Collector"                                                                                     # name of main speed hump feature class

try:
    """ Replace Features in Feature Class and Delete Copy """

    arcpy.DeleteRows_management(fc_to)
    arcpy.Append_management(fc_from, fc_to, "NO_TEST")
    arcpy.AddMessage("SUCCESS")
    
except Exception as err:
    """ Error Handling """

    arcpy.AddError(err)
    sys.exit(1)
