#example how to use:
#xy = pd.DataFrame(list(zip(x,y)),columns=['LON','LAT'])
#ibuoy = find_closest_index([lon,lat], xy)

from scipy.spatial.distance import cdist
import numpy as np

def find_closest_index(target_point, points_array):
    # Convert the array and target point to numpy arrays
    target_point = np.array(target_point)
    points_array = np.array(points_array)

    # Calculate the distances between the target point and all points in the array
    distances = cdist([target_point], points_array)

    # Find the index of the closest point
    closest_index = np.argmin(distances)

    if np.size(closest_index) == 1:
        closest_index=int(closest_index)

    return closest_index
