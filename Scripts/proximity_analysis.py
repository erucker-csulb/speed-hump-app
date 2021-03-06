"""
 Tool Name:   ProximityAnalysis
 Source Name: proximity_filter.py
 Author:      Ethan Rucker
 Required Arguments:
              The path to the Geodatabase Workspace
 Optional Arguments:
              Search Radius for Sidewalks (default="100 Feet")
              Search Radius for Bus Routes (default="300 Feet")
              Search Radius for Haul Routes (default="300 Feet")
              Search Radius for Police, Fire Stations, and Hospitals (default="1000 Feet")
              Search Radius for Schools (default="2000 Feet")
              Search Radius for Parks (default="1000 Feet")
              Search Radius for Bike Routes (default="300 Feet")
 Description: 
              Checks for features near speed hump requests based on given search distances.
              For schools, parks, and bike routes, also checks for direct access.
"""

import arcpy, sys

""" Common Variables """

arcpy.env.workspace = arcpy.GetParameterAsText(0)                       # path to geodatabase
edit = arcpy.da.Editor(arcpy.env.workspace)                             # enables edits to the GDB

speed_humps_fc = r"SpeedHump\SpeedHumpAnalysis"                         # path to speed hump feature class

""" Sidewalk Variables """

sidewalks_fc = "Sidewalks"                                              # path to sidewalk feature class 
sw_radius = arcpy.GetParameterAsText(1)                                 # search radius for sidewalks

""" Bus Route Variables """

metro_fc = "MetroBusRoutes"                                             # path to metro bus route feature class 
comm_dash_fc = "CommunityDASHRoutes"                                    # path to community dash route feature class 
comm_exp_fc = "CommuterExpressRoutes"                                   # path to commuter express route feature class 
dt_dash_fc = "DowntownDASHRoutes"                                       # path to downtown dash route feature class 
bdr_radius = arcpy.GetParameterAsText(2)                                # search radius for bus routes

""" Haul Route Variables """

empty_haul_fc = "EmptyTruckHaulRoutes"                                  # paths to empty haul route feature class
loaded_haul_fc = "LoadedTruckHaulRoutes"                                # paths to loaded haul route feature class
hr_radius = arcpy.GetParameterAsText(3)                                 # search radius for haul routes

""" Police/Fire/Hospital Variables """

police_fc = "Police"                                                    # paths to police station feature class
fire_fc = "FireStations"                                                # paths to fire station feature class
hospitals_fc = "Hospitals"                                              # paths to hospital feature class
pfh_radius = arcpy.GetParameterAsText(4)                                # search radius for police stations, fire stations, and hospitals

""" School Variables """

schools_fc = "SchoolCampuses"                                           # paths to school feature class
school_addr_field = "ADDRESS"                                           # address field of school feature class (for direct access check)
school_id_field = "OBJECTID"                                            # id field of school feature class (for direct access check)
school_radius = arcpy.GetParameterAsText(5)                             # search radius for schools

""" Park Variables """

parks_fc = "Parks"                                                      # paths to park feature class
park_addr_field = "Address"                                             # address field of park feature class (for direct access check)
park_id_field = "OBJECTID_1"                                            # id field of park feature class (for direct access check)
park_radius = arcpy.GetParameterAsText(6)                               # search radius for parks

""" Bike Route Variables """

bikeways_fc = "Bikeways"                                                # path to bike route feature class
bike_addr_field = "ST_NAME"                                             # address field of bike route feature class (for direct access check)
bike_id_field = "OBJECTID_12"                                           # id field of bike route feature class (for direct access check)
bike_radius = arcpy.GetParameterAsText(7)                               # search radius for bike routes

""" Direct Access Check Function """

def check_direct_access(fc, fid, fields, street_name):
    da = "No"
    expression = arcpy.AddFieldDelimiters(fc, fields[1]) + ' = ' + str(fid)

    with arcpy.da.SearchCursor(fc, fields, expression) as cursor:
        for row in cursor:
            if street_name.lower() in row[0].lower():
                da = "Yes"

    return da

""" Proximity Check Function """

def check_proximity(speed_humps_fc, other_fc, search_radius, field, da_check_fields=False):
    try:
        
        arcpy.Near_analysis(speed_humps_fc, other_fc, search_radius, method="GEODESIC")

        edit.startEditing(False, True)
        edit.startOperation()

        fields = [field, "DA", "SN", "NEAR_FID"]

        with arcpy.da.UpdateCursor(speed_humps_fc, fields) as cursor:
            for row in cursor:
                near_fid = row[-1]
                street_name = row[2]
                da = row[1]
                row[0] = "Yes" if near_fid != -1 else "No"
                if da_check_fields and da == "No":
                    row[1] = check_direct_access(other_fc, near_fid, da_check_fields, street_name)
                cursor.updateRow(row)
        
        edit.stopOperation()
        edit.stopEditing(True)

        arcpy.AddMessage(field + " proximity check SUCCEEDED!")

    except Exception as err:
        """ Error Handling """

        arcpy.AddError(err)
        sys.exit(1)


""" Set Direct Access field to 'No' (in case of multiple runs) """

arcpy.CalculateField_management(speed_humps_fc, "DA", "'No'", "PYTHON3")

""" All Proximity Function Calls """

check_proximity(speed_humps_fc, sidewalks_fc, sw_radius, "SW")
check_proximity(speed_humps_fc, [bikeways_fc, metro_fc, comm_dash_fc, comm_exp_fc, dt_dash_fc], bdr_radius, "BDR")
check_proximity(speed_humps_fc, [empty_haul_fc, loaded_haul_fc], hr_radius, "CHR")
check_proximity(speed_humps_fc, [police_fc, fire_fc, hospitals_fc], pfh_radius, "PFH")
check_proximity(speed_humps_fc, schools_fc, school_radius, "SR", [school_addr_field, school_id_field])
check_proximity(speed_humps_fc, parks_fc, park_radius, "Park", [park_addr_field, park_id_field])
check_proximity(speed_humps_fc, bikeways_fc, bike_radius, "BR", [bike_addr_field, bike_id_field])

""" Delete fields from Near analysis """

arcpy.DeleteField_management(speed_humps_fc, ["NEAR_FID", "NEAR_DIST", "NEAR_FC"])
