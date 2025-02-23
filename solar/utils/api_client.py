from rex import Resource
import numpy as np
from scipy.spatial import cKDTree

nsrdb_file = '/nrel/nsrdb/current/nsrdb_2022.h5'


def get_ghi(lat, long):
    with Resource(nsrdb_file) as res:
        target_coord = np.array([lat, long])
        latitudes = np.array(res.coordinates[:, 0])
        longitudes = np.array(res.coordinates[:, 1])
        coords = np.column_stack((latitudes, longitudes))
        tree = cKDTree(coords)
        _, index = tree.query(target_coord)

        ghi_value = np.mean(res['ghi', :, index])

    return ghi_value