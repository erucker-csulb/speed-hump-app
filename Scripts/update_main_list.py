"""
 Tool Name:   UpdateMainList
 Source Name: update_main_list.py
 Author:      Ethan Rucker
 Required Arguments:
              The path to the Geodatabase Workspace
 Description: 
              Appends the data from the Analysis feature class to the main speed 
              hump feature class that holds all previous speed hump requests.
"""

import arcpy, sys

""" Local Variables """

arcpy.env.workspace = arcpy.GetParameterAsText(0)                        # path to file geodatabase
fc_from = r"SpeedHump\SpeedHumpAnalysis"                                 # name of copied feature class
fc_to = r"SpeedHump\SpeedHump"                                           # name of main speed hump feature class

try:
    """ Replace Features in Feature Class and Delete Copy """

    arcpy.Append_management(fc_from, fc_to, "NO_TEST")
    arcpy.AddMessage("SUCCESS")
    
except Exception as err:
    """ Error Handling """

    arcpy.AddError(err)
    sys.exit(1)
