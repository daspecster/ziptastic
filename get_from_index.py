def get_from_index(point):
    """
    Returns a point near the given point from the redis index.
    """
    lat, long = point
    pid = geohash.encode(lat, long)
    constituent = (pid[:i+1] for i in range(len(pid)))
    r = redis.Redis()
    # Go from most precise to least
    for area in constituent[::-1]:
        count = r.scard("MMA:" + area)
        if count == 0:
            continue
        elif count == 1:
            val = r.srandmember("MMA:" + area).decode()
            if val == pid:
                continue
            else:
                return val
        else:
            found = pid
            while found == pid:
                found = r.srandmember("MMA:" + area).decode()
            return found
    # No point found
    return