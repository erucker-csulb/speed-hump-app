"""
 Tool Name:   CalcSpeed
 Source Name: calc_speed_eq.py
 Author:      Ethan Rucker
 Required Arguments:
              The path to the Geodatabase Workspace
 Description: 
              Calculates 85th percentile speed for each speed hump request location.
              Calculation is the average of recorded speeds in both directions from
              up to two separate field surveys.
"""

import arcpy, sys

arcpy.env.workspace = arcpy.GetParameterAsText(0)
edit = arcpy.da.Editor(arcpy.env.workspace)
fc = r"SpeedHump\SpeedHumpAnalysis"
fields = ["FN_E_S", "FS_W_S", "SN_E_S", "SS_W_S", "CL85"]

def calc_speed(ne_speed_1, sw_speed_1, ne_speed_2, sw_speed_2):
    count = 0
    sum_speed = 0
    if ne_speed_1 is not None:
        count += 1
        sum_speed += ne_speed_1
        if sw_speed_1:
            count += 1
            sum_speed += sw_speed_1
        if ne_speed_2:
            count += 1
            sum_speed += ne_speed_2
            if sw_speed_2:
                count += 1
                sum_speed += sw_speed_2
            return sum_speed / count
        return sum_speed / count
    return 0

try:

    edit.startEditing(False, True)
    edit.startOperation()

    with arcpy.da.UpdateCursor(fc, fields) as cursor:
        for row in cursor:
            row[4] = float(calc_speed(row[0], row[1], row[2], row[3]))
            arcpy.AddMessage(row[4])
            cursor.updateRow(row)

    edit.stopOperation()
    edit.stopEditing(True)

except Exception as err:
    """ Error Handling """

    arcpy.AddError(err)
    sys.exit(1)
