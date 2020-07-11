lan_cell = 6267123295
fields = ['BJ', 'BM', 'BW', 'BY', 'CR']

def acc_hist_flag(ten_year, five_year, three_year):
    if ten_year > 6:
        return "Hi 10 yr crash"
    elif five_year > 2:
        return "Hi 5 yr crash"
    elif three_year > 1:
        return "Recent crashes"
    return ""

def pre_score(three_year, five_year, special_facilities, street_width, bike_route, street_length, sidewalk, cd_priority):
    acc_factor = three_year + (five_year * 2)
    sf_factor = (special_facilities[0] * 2) +  special_facilities[1] + special_facilities[2] + special_facilities[3] + special_facilities[4]
    width_factor = 1 if street_width > 38 or (street_width < 36 and bike_route) else 0
    length_factor = min(2, (street_length - 600)/1000 + 1)
    sw_factor = 0.5 if not sidewalk else 0
    cd_factor = 0.5 if cd_priority else 0
    return acc_factor + sf_factor + width_factor + length_factor + sw_factor + cd_factor

def calc_speed(ne_speed_1, sw_speed_1, ne_speed_2, sw_speed_2):
    sum_speed = sum(ne_speed_1, sw_speed_1, ne_speed_2, sw_speed_2)
    if ne_speed_1:
        if ne_speed_2:
            return sum_speed / 4
        return sum_speed / 2
    return -1
    

def calc_adt(ne_adt_1, sw_adt_1, ne_adt_2, sw_adt_2):
    sum_1 = ne_adt_1 + sw_adt_1
    sum_2 = ne_adt_2 + sw_adt_2
    if sum_1 or sum_2:
        return max(sum_1, sum_2)
    return -1

def rank_score(speed_limit, speed_calc, adt_calc):
    sl_check = 1 if speed_limit >= 30 else 0
    speed_check = 1 if speed_calc - speed_limit > 5 else 0
    adt_check = 1 if adt_calc - 1000 > 0 else 0
    speed_points = min(40, (speed_calc - speed_limit - 5) * 3) if speed_check else 0
    adt_points = min(20, (adt_calc - 1000) / 400) if adt_check and adt_check > 0 else 0
    tot_other = 0 #placeholder
    return sl_check * speed_check * adt_check * (speed_points + adt_points + tot_other)