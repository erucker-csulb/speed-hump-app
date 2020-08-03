"""
 Tool Name:   PreScore
 Source Name: pre_score_eq.py
 Author:      Ethan Rucker
 Required Arguments:
              The path to the Geodatabase Workspace
 Description: 
              Calculates pre-score ranking for each speed hump request. Score is 
              based on accident history, nearby facilities, street measurements,
              sidewalks, and priority from council district.
"""

import arcpy

arcpy.env.workspace = arcpy.GetParameterAsText(0)
edit = arcpy.da.Editor(arcpy.env.workspace)
fc = r"SpeedHump\SpeedHumpAnalysis"
fields = ["THYA", "FYA", "DA", "SR", "BDR", "Park", "OSF", "SWI", "SL", "SW", "CDP", "PS"]

def null_value_error(field):
    arcpy.AddError(field + " returned a NULL value.")
    sys.exit(1)

def pre_score(three_year, five_year, special_facilities, street_width, street_length, sidewalk, cd_priority):
    if three_year is None or five_year is None:
        null_value_error("Accident History")
    acc_factor = three_year + (five_year * 2)
    
    sf_int = []
    for sf in special_facilities:
        if not sf:
            null_value_error("Special Facilities")
        sf_int.append(1 if sf == "Yes" else 0)
    sf_factor = (sf_int[0] * 2) +  sf_int[1] + sf_int[2] + sf_int[3] + sf_int[4]

    if not street_width or not street_length:
        null_value_error("Street Width or Length")
    width_factor = 1 if street_width > 38 or (street_width < 36 and special_facilities[2]) else 0
    length_factor = min(2, (street_length - 600)/1000 + 1)

    if not sidewalk or not cd_priority:
        null_value_error("Sidewalk or Council District Priority")
    sw_factor = 0.5 if sidewalk == "No" else 0
    cd_factor = 0.5 if cd_priority == "Yes" else 0

    return acc_factor + sf_factor + width_factor + length_factor + sw_factor + cd_factor

try:

    edit.startEditing(False, True)
    edit.startOperation()

    with arcpy.da.UpdateCursor(fc, fields) as cursor:
        for row in cursor:
            row[11] = float(pre_score(row[0], row[1], row[2:7], row[7], row[8], row[9], row[10]))
            arcpy.AddMessage(row[11])
            cursor.updateRow(row)

    edit.stopOperation()
    edit.stopEditing(True)

except Exception as err:
    """ Error Handling """

    arcpy.AddError(err)
    sys.exit(1)
