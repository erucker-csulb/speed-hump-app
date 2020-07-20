# excel_fields: BJ BM BW BY CR

def acc_hist_flag(ten_year, five_year, three_year):
    if ten_year > 6:
        return "Hi 10 yr crash"
    elif five_year > 2:
        return "Hi 5 yr crash"
    elif three_year > 1:
        return "Recent crashes"
    return ""

def pre_score(three_year, five_year, special_facilities, street_width, street_length, sidewalk, cd_priority):
    acc_factor = three_year + (five_year * 2)
    sf_factor = (special_facilities[0] * 2) +  special_facilities[1] + special_facilities[2] + special_facilities[3] + special_facilities[4]
    width_factor = 1 if street_width > 38 or (street_width < 36 and special_facilities[2]) else 0
    length_factor = min(2, (street_length - 600)/1000 + 1)
    sw_factor = 0.5 if not sidewalk else 0
    cd_factor = 0.5 if cd_priority else 0
    return acc_factor + sf_factor + width_factor + length_factor + sw_factor + cd_factor

def calc_speed(ne_speed_1, sw_speed_1, ne_speed_2, sw_speed_2):
    if ne_speed_1:
        if ne_speed_2:
            return (ne_speed_1 + sw_speed_1 + ne_speed_2 + sw_speed_2) / 4
        return (ne_speed_1 + sw_speed_1) / 2
    return 0 

def calc_adt(ne_adt_1, sw_adt_1, ne_adt_2, sw_adt_2):
    if ne_adt_1:
        sum_1 = ne_adt_1 + sw_adt_1
        if ne_adt_2:
            sum_2 = ne_adt_2 + sw_adt_2
            return max(sum_1, sum_2)
        return sum_1
    return 0

def calc_sf_points(special_facilities, width_factor):
    sr_points = 26 if special_facilities[0] else 0
    br_points = 12 if special_facilities[1] + width_factor > 1 else 0
    park_points = 28 if special_facilities[2] else 0
    osf_points = 18 if special_facilities[3] else 0
    return sr_points + br_points + park_points + osf_points

def rank_score(speed_limit, speed_calc, adt_calc, ksi, three_year, five_year, swcd_factor, da, sf_points):
    sl_check = 1 if speed_limit <= 30 else 0
    speed_check = 1 if speed_calc - speed_limit > 5 else 0
    adt_check = 1 if adt_calc - 1000 > 0 else 0
    speed_points = min(40, (speed_calc - speed_limit - 5) * 3) if speed_check else 0
    print("CK: ", speed_points)
    adt_points = min(20, (adt_calc - 1000) / 400) if adt_check and adt_check > 0 else 0
    print("CL: ", adt_points)
    ksi_factor = 20 if ksi > 0 else min(20, five_year * 10)
    three_year_check = min(20, three_year * 7)
    acc_points = min(20, ksi_factor + three_year_check)
    print("CM: ", acc_points)
    swcd_points = swcd_factor * 10
    da_points = 30 if da else sf_points
    print("CO: ", da_points)
    tot_other = acc_points + swcd_points + da_points
    return sl_check * speed_check * adt_check * (speed_points + adt_points + tot_other)