from rex import Resource

nsrdb_file = '/nrel/nsrdb/conus/nsrdb_conus_2022.h5'


def get_ghi(latitude, longitude):
    with Resource(nsrdb_file) as res:
        latitudes = res.coordinates[:, 0]
        longitudes = res.coordinates[:, 1]

        lat_index = (abs(latitudes - latitude)).argmin()
        lon_index = (abs(longitudes - longitude)).argmin()

        ghi = res['ghi', lat_index, lon_index]

    return ghi


# print(get_ghi(40.7128, -74.0060))  # New York City
print(get_ghi(34.0522, -118.2437))  # Los Angeles
# print(get_ghi(41.8781, -87.6298))  # Chicago
# print(get_ghi(37.7749, -122.4194))  # San Francisco
