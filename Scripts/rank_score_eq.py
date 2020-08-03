"""
 Tool Name:   RankScore
 Source Name: rank_score_eq.py
 Author:      Ethan Rucker
 Required Arguments:
              The path to the Geodatabase Workspace
 Description: 
              Calculates final rank score for each speed hump request. Score is 
              based on calculated 85th percentile speed, calculated average daily 
              traffic, accident history, nearby facilities, street width, sidewalks, 
              and priority from council district. Rank score is 0 if any of the
              following criteria fails:
                  Speed Limit <= 30 mph
                  Calc 85th Speed - Speed Limit > 5
                  Calc ADT - 1000 > 0
"""

import arcpy

arcpy.env.workspace = arcpy.GetParameterAsText(0)
fc = r"SpeedHump\SpeedHumpAnalysis"
edit = arcpy.da.Editor(arcpy.env.workspace)

def null_value_error(field):
    arcpy.AddError(field + " returned a NULL value.")
    sys.exit(1)

def calc_sf_points(special_facilities, width_factor):
    sr_points = 26 if special_facilities[0] else 0
    br_points = 12 if special_facilities[1] + width_factor > 1 else 0
    park_points = 28 if special_facilities[2] else 0
    osf_points = 18 if special_facilities[3] else 0
    return sr_points + br_points + park_points + osf_points

def rank_score(speed_limit, speed_calc, adt_calc, ksi, three_year, five_year, sidewalk, cd_priority, da, special_facilities, street_width):
    if not speed_limit or speed_calc is None or adt_calc is None:
        null_value_error("Speed or Traffic")
    sl_check = 1 if speed_limit <= 30 else 0
    speed_check = 1 if speed_calc - speed_limit > 5 else 0
    adt_check = 1 if adt_calc - 1000 > 0 else 0
    speed_points = min(40, (speed_calc - speed_limit - 5) * 3) if speed_check else 0
    adt_points = min(20, (adt_calc - 1000) / 400) if adt_check and adt_check > 0 else 0

    if ksi is None or three_year is None or five_year is None:
        null_value_error("Accident History")
    ksi_factor = 20 if ksi > 0 else min(20, five_year * 10)
    three_year_check = min(20, three_year * 7)
    acc_points = min(20, ksi_factor + three_year_check)

    if not sidewalk or not cd_priority:
        null_value_error("Sidewalk or Council District Priority")
    sw_factor = 0.5 if sidewalk == "No" else 0
    cd_factor = 0.5 if cd_priority == "Yes" else 0
    swcd_points = (sw_factor + cd_factor) * 10

    if not street_width or not da:
        null_value_error("Street Width or Direct Access")
    width_factor = 1 if street_width < 36 else 0
    sf_int = []
    for sf in special_facilities:
        if not sf:
            null_value_error("Special Facilities")
        sf_int.append(1 if sf == "Yes" else 0)
    sf_points = calc_sf_points(sf_int, width_factor)
    da_points = 30 if da == "Yes" else sf_points

    tot_other = acc_points + swcd_points + da_points
    return sl_check * speed_check * adt_check * (speed_points + adt_points + tot_other)

fields = ["SP", "CL85", "CLADT", "KSI", "THYA", "FYA", "SW", "CDP", "DA", "SR", "BDR", "Park", "OSF", "SWI", "RS", "ST"]
expression = arcpy.AddFieldDelimiters(fc, fields[-1]) + " = 'Pending'"

try:

    edit.startEditing(False, True)
    edit.startOperation()

    with arcpy.da.UpdateCursor(fc, fields, expression) as cursor:
        for row in cursor:
            row[14] = float(rank_score(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9:13], row[13]))
            arcpy.AddMessage(row[14])
            cursor.updateRow(row)

    edit.stopOperation()
    edit.stopEditing(True)

except Exception as err:
    """ Error Handling """

    arcpy.AddError(err)
    sys.exit(1)
