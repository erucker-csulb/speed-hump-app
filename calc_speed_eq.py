import arcpy

arcpy.env.workspace = r"D:\CSULB\SpeedHumps\SpeedHump.gdb"
fc = r"SpeedHumpEmpty\SpeedHumpEmpty"
edit = arcpy.da.Editor(arcpy.env.workspace)

def calc_speed(ne_speed_1, sw_speed_1, ne_speed_2, sw_speed_2):
    count = 0
    sum_speed = 0
    if ne_speed_1:
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

fields = ["FN_E_S", "FS_W_S", "SN_E_S", "SS_W_S", "CL85"]

edit.startEditing(False, True)
edit.startOperation()

with arcpy.da.UpdateCursor(fc, fields) as cursor:
    for row in cursor:
        row[4] = float(calc_speed(row[0], row[1], row[2], row[3]))
        print(row[4])
        cursor.updateRow(row)

edit.stopOperation()
edit.stopEditing(True)
