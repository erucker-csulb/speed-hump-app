"""
 Tool Name:   CreateSpeedHumpBuffers
 Source Name: speed_hump_buffer.py
 Author:      Ethan Rucker
 Required Arguments:
              The path to the Geodatabase Workspace
 Optional Arguments:
              A set of distances (default=[600,900,1200])
              The distance unit of measurement (default="Feet")
 Description: 
              Creates a set of buffers for the Speed Hump Analysis feature class.
              The buffers are defined using a set of variable distances. The resulting
              feature class is added to the map beneath the input layer.
"""

import arcpy, os, sys

""" Local Variables """

arcpy.env.workspace = arcpy.GetParameterAsText(0)                         # path to file geodatabase
speed_hump_fc = r"SpeedHump\SpeedHumpAnalysis"                            # name of speed hump feature class
buffer_fc = r"SpeedHumpBuffers"                                           # name of buffer feature class
distances = arcpy.GetParameter(1)                                         # buffer distances
unit = arcpy.GetParameterAsText(2)                                        # distance unit of measurement

try:
    """ Delete Previous Buffer Feature Class and Execute Multi Ring Buffer Tool """

    arcpy.Delete_management(buffer_fc)
    arcpy.MultipleRingBuffer_analysis(speed_hump_fc, buffer_fc, distances, unit, "", "NONE")
    aprx = arcpy.mp.ArcGISProject("CURRENT")
    m = aprx.listMaps("Speed Hump")[0]
    ref_lyr = m.listLayers("SpeedHumpAnalysis")[0]
    buf_lyr = m.addDataFromPath(os.path.join(arcpy.env.workspace, buffer_fc))
    m.moveLayer(ref_lyr, buf_lyr, "AFTER")
    arcpy.AddMessage("SUCCESS")
    
except Exception as err:
    """ Error Handling """

    arcpy.AddError(err)
    sys.exit(1)