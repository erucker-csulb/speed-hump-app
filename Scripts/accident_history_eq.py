"""
 Tool Name:   AccidentHistoryFlag
 Source Name: accident_history_eq.py
 Author:      Ethan Rucker
 Required Arguments:
              The path to the Geodatabase Workspace
 Description: 
              Sets accident history flag based on following criteria:
                  Ten-Year Crashes > 6 --> "Hi 10 yr crash"
                  Five-Year Crashes > 2 --> "Hi 5 yr crash"
                  Three-Year Crashes > 1 --> "Recent crashes"
"""

import arcpy, sys

arcpy.env.workspace = arcpy.GetParameterAsText(0)
edit = arcpy.da.Editor(arcpy.env.workspace)
fc = r"SpeedHump\SpeedHumpAnalysis"
fields = ["TEYA", "FYA", "THYA", "AH"]

def acc_hist_flag(ten_year, five_year, three_year):
    if ten_year and ten_year > 6:
        return "Hi 10 yr crash"
    elif five_year and five_year > 2:
        return "Hi 5 yr crash"
    elif three_year and three_year > 1:
        return "Recent crashes"
    return ""

try:

    edit.startEditing(False, True)
    edit.startOperation()

    with arcpy.da.UpdateCursor(fc, fields) as cursor:
        for row in cursor:
            row[3] = acc_hist_flag(row[0], row[1], row[2])
            arcpy.AddMessage(row[3])
            cursor.updateRow(row)

    edit.stopOperation()
    edit.stopEditing(True)

except Exception as err:
    """ Error Handling """

    arcpy.AddError(err)
    sys.exit(1)
