import arcpy

arcpy.env.workspace = arcpy.GetParameterAsText(0)
fc = r"SpeedHump/SpeedHumpAnalysis"
edit = arcpy.da.Editor(arcpy.env.workspace)

def calc_adt(ne_adt_1, sw_adt_1, ne_adt_2, sw_adt_2):
    if ne_adt_1:
        sum_1 = ne_adt_1 + sw_adt_1
        if ne_adt_2:
            sum_2 = ne_adt_2 + sw_adt_2
            return max(sum_1, sum_2)
        return sum_1
    return 0

fields = ["FN_E_T", "FS_W_T", "SN_E_T", "SS_W_T", "CLADT"]

edit.startEditing(False, True)
edit.startOperation()

with arcpy.da.UpdateCursor(fc, fields) as cursor:
    for row in cursor:
        row[4] = calc_adt(row[0], row[1], row[2], row[3])
        print(row[4])
        cursor.updateRow(row)

edit.stopOperation()
edit.stopEditing(True)
