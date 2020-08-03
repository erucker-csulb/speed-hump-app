"""
 Tool Name:   PreliminaryFilter
 Source Name: preliminary_filter.py
 Author:      Ethan Rucker
 Required Arguments:
              The path to the Geodatabase Workspace
 Description: 
              Denies speed hump requests that do not meet preliminary criteria.
              Criteria: Outside of City
                        Street is not Local or Collector
                        Grading is higher than 7%
"""

import arcpy, sys

arcpy.env.workspace = arcpy.GetParameterAsText(0)
fc = r"SpeedHump\SpeedHumpAnalysis"
edit = arcpy.da.Editor(arcpy.env.workspace)

def update_status(council_district, street_class, grade_percent, status):
    if not council_district:
        return "Outside of City"
    elif street_class and street_class != "Local Street" and street_class != "Collector Street":
        return "Street Class"
    elif grade_percent and grade_percent > 7:
        return "Grade Percent"
    return status

fields = ["CDN", "SCL", "GP", "ST"]

try:

    edit.startEditing(False, True)
    edit.startOperation()

    with arcpy.da.UpdateCursor(fc, fields) as cursor:
        for row in cursor:
            row[3] = update_status(row[0], row[1], row[2], row[3])
            arcpy.AddMessage(row[3])
            cursor.updateRow(row)

    edit.stopOperation()
    edit.stopEditing(True)

except Exception as err:
    """ Error Handling """

    arcpy.AddError(err)
    sys.exit(1)
