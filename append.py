import arcpy, os

arcpy.env.workspace = r"D:\CSULB\SpeedHumps\SpeedHump.gdb" # path to file geodatabase
edit = arcpy.da.Editor(arcpy.env.workspace) # enables edits to the GDB

fc_copy = r"SpeedHumpCopy" # name of copied feature class
fc = r"SpeedHumpEmpty/SpeedHumpEmpty" # name of main speed hump feature class

edit.startEditing(False, True)
edit.startOperation()

arcpy.Append_management(fc_copy, fc, "TEST")

edit.stopOperation()
edit.stopEditing(True)