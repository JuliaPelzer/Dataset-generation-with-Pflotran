import numpy as np
import matplotlib.pyplot as plt
from typing import List

from scripts.utils import timing
from scripts.mesh_refinement import get_refinement_intervals

def calc_refined_grid_2D(leave_outs: List[np.ndarray]):
    ids = None
    cell_centerss = []
    face_centerss = []
    face_idss = []
    face_areass = []
    cell_volumess = []
    for leave_out in leave_outs + [None]:
        w, h = leave_out.shape if leave_out is not None else np.array(ids.shape) * 2
        aspect = w / h
        cell_centers, face_centers, face_ids, face_areas, cell_volumes, ids = get_grid_2D(
            w=w,
            h=h,
            minx=0,
            maxx=aspect,
            miny=0,
            maxy=1,
            larger_indices=ids,
            leave_out=leave_out,
        )
        cell_centerss.append(cell_centers)
        face_centerss.append(face_centers)
        face_idss.append(face_ids)
        face_areass.append(face_areas)
        cell_volumess.append(cell_volumes)
    cell_centers = np.concatenate(cell_centerss)
    face_centers = np.concatenate(face_centerss)
    face_ids = np.concatenate(face_idss)
    face_areas = np.concatenate(face_areass)
    cell_volumes = np.concatenate(cell_volumess)
    return cell_centers, face_centers, face_ids, face_areas, cell_volumes

def get_grid_2D(w, h, minx, maxx, miny, maxy, larger_indices=None, leave_out=None):

    # to_draw is a mask that tells us which cells to define
    to_draw = np.ones((w, h), dtype=bool)

    # don't draw cells that will be filled with finer resolution
    if leave_out is not None:
        to_draw[leave_out] = False

    # don't draw cells that are already in the coarser grid
    if larger_indices is not None:
        dont_redraw = larger_indices != -1
        to_draw[::2, ::2][dont_redraw] = False
        to_draw[1::2, ::2][dont_redraw] = False
        to_draw[::2, 1::2][dont_redraw] = False
        to_draw[1::2, 1::2][dont_redraw] = False

    highest_index = np.max(larger_indices) if larger_indices is not None else -1
    ids = -np.ones((w, h))
    # fill the ids of all cells
    ids[to_draw] = np.arange(to_draw.sum()) + highest_index + 1

    # fill in ids from cells of larger grid
    if larger_indices is not None:
        ids[::2, ::2][dont_redraw] = larger_indices[dont_redraw]
        ids[1::2, ::2][dont_redraw] = larger_indices[dont_redraw]
        ids[::2, 1::2][dont_redraw] = larger_indices[dont_redraw]
        ids[1::2, 1::2][dont_redraw] = larger_indices[dont_redraw]

    # remove all faces that are inside the same cell
    horizontal_mask = ids[:, :-1] - ids[:, 1:] != 0
    vertical_mask = ids[:-1, :] - ids[1:, :] != 0

    sx = (maxx - minx) / w
    sy = (maxy - miny) / h
    cell_centers = np.stack(
        np.meshgrid(
            np.linspace(minx + sx / 2, maxx - sx / 2, w),
            np.linspace(miny + sy / 2, maxy - sy / 2, h),
        )
    ).T

    horizontal_faces_centers = np.stack(
        np.meshgrid(
            np.linspace(minx + sx / 2, maxx - sx / 2, w),
            np.linspace(miny + sx, maxy - sx, h - 1),
        )
    ).T

    vertical_faces_centers = np.stack(
        np.meshgrid(
            np.linspace(minx + sy, maxx - sy, w - 1),
            np.linspace(miny + sy / 2, maxy - sy / 2, h),
        )
    ).T
    vertical_face_ids = np.zeros(vertical_faces_centers.shape, dtype=int)
    vertical_face_ids[..., 0] = ids[:-1, :]
    vertical_face_ids[..., 1] = ids[1:, :]
    vertical_mask &= vertical_face_ids[..., 0] != -1
    vertical_mask &= vertical_face_ids[..., 1] != -1
    vertical_mask &= ~(
        (vertical_face_ids[..., 0] <= highest_index)
        & (vertical_face_ids[..., 1] <= highest_index)
    )
    vertical_face_ids = vertical_face_ids[vertical_mask]
    vertical_faces_centers = vertical_faces_centers[vertical_mask]
    horizontal_face_ids = np.zeros(horizontal_faces_centers.shape, dtype=int)
    horizontal_face_ids[..., 0] = ids[:, :-1]
    horizontal_face_ids[..., 1] = ids[:, 1:]
    horizontal_mask &= (
        (horizontal_face_ids[..., 0] != -1)
        & (horizontal_face_ids[..., 1] != -1)
        & ~(
            (horizontal_face_ids[..., 0] <= highest_index)
            & (horizontal_face_ids[..., 1] <= highest_index)
        )
    )
    horizontal_face_ids = horizontal_face_ids[horizontal_mask]
    horizontal_faces_centers = horizontal_faces_centers[horizontal_mask]
    cell_centers = cell_centers[to_draw]
    cell_centers = cell_centers.reshape(-1, 2)
    cell_volumes = np.full((w, h), 125)
    cell_volumes = cell_volumes[to_draw]
    cell_volumes = cell_volumes.flatten()
    face_centers = np.concatenate(
        [horizontal_faces_centers.reshape(-1, 2), vertical_faces_centers.reshape(-1, 2)]
    )
    face_ids = np.concatenate(
        [horizontal_face_ids.reshape(-1, 2), vertical_face_ids.reshape(-1, 2)]
    )
    face_areas = np.full(face_centers.shape[0], (maxx - minx) / w * 5)
    return cell_centers, face_centers, face_ids, face_areas, cell_volumes, ids

@timing
def plot_grid_2D(cell_centers, face_centers, face_cell_ids, face_areas, factor):
    plt.scatter(
        cell_centers[:, 0], cell_centers[:, 1], c="r", label="cell centers", marker="."
    )
    n1 = cell_centers[face_cell_ids[:, 0]]
    n2 = cell_centers[face_cell_ids[:, 1]]
    direction = n2 - n1
    lens = np.sqrt(face_areas) / (factor*1.5)
    updown = np.abs(direction[:, 1]) > np.abs(direction[:, 0])
    leftright = ~updown

    plt.scatter(
        face_centers[:, 0],
        face_centers[:, 1],
        c="b",
        label="face centers",
        marker=".",
    )
    ys = face_centers[:, 1][updown]
    xmins = face_centers[:, 0][updown] - lens[updown] / 2
    xmaxs = face_centers[:, 0][updown] + lens[updown] / 2
    plt.hlines(ys, xmins, xmaxs, colors="black")
    xs = face_centers[:, 0][leftright]
    ymins = face_centers[:, 1][leftright] - lens[leftright] / 2
    ymaxs = face_centers[:, 1][leftright] + lens[leftright] / 2
    plt.vlines(xs, ymins, ymaxs, colors="black")
    plt.axis("equal")
    plt.legend()
    plt.show()

def test_run_2D():
    num_dp = 4
    num_hp = 3
    orig_resolution = 10
    settings = {
        "grid": {
            "resolution": 5,
            "size [m]": [100, 60, 5],
            "distance_to_border": 1,
        },
        "subsurface": {
            "hydraulic_conductivity": 1e-5,
            "thickness": 5,
            "darcy_velocity": 1,
        },
    }

    length, width, height = 100, 50, 1#= settings["grid"]["size [m]"]
    res = settings["grid"]["resolution"]
    width, length = width//res, length//res
    cells_to_refine_later = []
    num_hp = 2
    hp_locs = np.array([[width/2,length/8],[1,10]]) #/res #, [10, 50]])/res #m # TODO achtung mit orientierung von hp, vllt taischen notwendig / später im aufruf vllt? # TODO in cells

    sichardt_dists = [1.5,] * num_hp
    lahm_w = [4,] * num_hp
    lahm_l = [8,] * num_hp
    radii_hps = []
    plume_w_hps = []
    plume_l_hps = []
    for hp in range(num_hp):
        # TO DO more efficient, but for now: radii = list of hp with dict of level:radius
        radii_hps.append(get_refinement_intervals(res, 0.1, sichardt_dists[hp]))
        plume_w_hps.append(get_refinement_intervals(res, 1, lahm_w[hp]))
        plume_l_hps.append(get_refinement_intervals(res, 1, lahm_l[hp]))

    levels = len(radii_hps[0])
    for i in range(levels):
        coords = (
            np.stack(np.meshgrid(
                    np.linspace(0, width, width * 2**i, endpoint=False),
                    np.linspace(0, length, length * 2**i, endpoint=False),)).T)

        mask = np.zeros(coords.shape[:2], dtype=bool) # mask of n_cells_w,_l in current resolution
        for hp_id, hp_coords in enumerate(hp_locs):
            radius = radii_hps[hp_id][i]
            mask += (coords[..., 0]-hp_coords[0]) ** 2 + (coords[..., 1]-hp_coords[1]) ** 2 < (radius + 0.75/(2**i)) ** 2 # +0.75 so that no cells with more than 1 difference in resolution steps are adjacent
            if i in plume_l_hps[hp_id].keys():
                diff_l = coords[...,1] - hp_coords[1] #+ 0.5/(2**i)
                diff_w =  plume_w_hps[hp_id][i] / 2 #+ 0.5 / (2 ** i)
                mask += np.logical_and(np.abs(coords[..., 0] - hp_coords[0]) < diff_w, np.logical_and(0 < diff_l, diff_l < plume_l_hps[hp_id][i]))
        cells_to_refine_later.append(mask)

    cell_centers, face_centers, face_ids, face_areas, cell_volumes = calc_refined_grid_2D(
        cells_to_refine_later
    )
    plot_grid_2D(cell_centers, face_centers, face_ids, face_areas, cell_volumes)

if __name__ == "__main__":
    test_run_2D()