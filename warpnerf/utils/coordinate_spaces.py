import numpy as np

def bl2wn_matrix(bl_matrix: np.ndarray) -> np.ndarray:
    result = np.array(bl_matrix, copy=True)
    result[:, 1:3] *= -1
    result[:3, :] = np.roll(result[:3, :], -1, axis=0)
    result = result @ np.diag([1, -1, 1, 1]) # flip y
    return result

def wn2bl_matrix(nerf_matrix: np.ndarray) -> np.ndarray:
    result = np.array(nerf_matrix, copy=True)
    result = result @ np.diag([1, -1, 1, 1]) # flip y
    result[:3, :] = np.roll(result[:3, :], 1, axis=0)
    result[:, 1:3] *= -1
    return result
