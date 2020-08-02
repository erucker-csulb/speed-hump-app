import arcpy

arcpy.env.workspace = arcpy.GetParameterAsText(0)
fc = r"SpeedHump/SpeedHumpAnalysis"
edit = arcpy.da.Editor(arcpy.env.workspace)

def acc_hist_flag(ten_year, five_year, three_year):
    if ten_year > 6:
        return "Hi 10 yr crash"
    elif five_year > 2:
        return "Hi 5 yr crash"
    elif three_year > 1:
        return "Recent crashes"
    return ""

fields = ["TEYA", "FYA", "THYA", "AH"]

edit.startEditing(False, True)
edit.startOperation()

with arcpy.da.UpdateCursor(fc, fields) as cursor:
    for row in cursor:
        row[3] = acc_hist_flag(row[0], row[1], row[2])
        print(row[3])
        cursor.updateRow(row)

edit.stopOperation()
edit.stopEditing(True)
