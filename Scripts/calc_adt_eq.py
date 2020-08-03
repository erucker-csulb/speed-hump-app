"""
 Tool Name:   CalcADT
 Source Name: calc_adt_eq.py
 Author:      Ethan Rucker
 Required Arguments:
              The path to the Geodatabase Workspace
 Description: 
              Calculates average daily traffic for each speed hump request location.
              Calculation is the maximum sum of recorded traffic counts in both directions between
              up to two separate field surveys.
"""

import arcpy

arcpy.env.workspace = arcpy.GetParameterAsText(0)
edit = arcpy.da.Editor(arcpy.env.workspace)
fc = r"SpeedHump\SpeedHumpAnalysis"
fields = ["FN_E_T", "FS_W_T", "SN_E_T", "SS_W_T", "CLADT"]

def calc_adt(ne_adt_1, sw_adt_1, ne_adt_2, sw_adt_2):
    if ne_adt_1 is not None:
        sum_1 = (ne_adt_1 + sw_adt_1) if sw_adt_1 else ne_adt_1
        if ne_adt_2 is not None:
            sum_2 = (ne_adt_2 + sw_adt_2) if sw_adt_2 else ne_adt_2
            return max(sum_1, sum_2)
        return sum_1
    return 0

try:

    edit.startEditing(False, True)
    edit.startOperation()

    with arcpy.da.UpdateCursor(fc, fields) as cursor:
        for row in cursor:
            row[4] = calc_adt(row[0], row[1], row[2], row[3])
            arcpy.AddMessage(row[4])
            cursor.updateRow(row)

    edit.stopOperation()
    edit.stopEditing(True)

except Exception as err:
    """ Error Handling """

    arcpy.AddError(err)
    sys.exit(1)
