import arcpy

arcpy.env.workspace = arcpy.GetParameterAsText(0)
fc = r"SpeedHump/SpeedHumpAnalysis"
edit = arcpy.da.Editor(arcpy.env.workspace)

def pre_score(three_year, five_year, special_facilities, street_width, street_length, sidewalk, cd_priority):
    acc_factor = three_year + (five_year * 2)
    
    sf_int = []
    for sf in special_facilities:
        sf_int.append(1 if sf == "Yes" else 0)
    sf_factor = (sf_int[0] * 2) +  sf_int[1] + sf_int[2] + sf_int[3] + sf_int[4]

    width_factor = 1 if street_width > 38 or (street_width < 36 and special_facilities[2]) else 0
    length_factor = min(2, (street_length - 600)/1000 + 1)

    sw_factor = 0.5 if sidewalk == "No" else 0
    cd_factor = 0.5 if cd_priority == "Yes" else 0

    return acc_factor + sf_factor + width_factor + length_factor + sw_factor + cd_factor

fields = ["THYA", "FYA", "DA", "SR", "BDR", "Park", "OSF", "SWI", "SL", "SW", "CDP", "PS"]

edit.startEditing(False, True)
edit.startOperation()

with arcpy.da.UpdateCursor(fc, fields) as cursor:
    for row in cursor:
        row[11] = float(pre_score(row[0], row[1], row[2:7], row[7], row[8], row[9], row[10]))
        print(row[11])
        cursor.updateRow(row)

edit.stopOperation()
edit.stopEditing(True)
