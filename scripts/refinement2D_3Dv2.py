from dataclasses import field, dataclass
import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, Dict
from tqdm.auto import tqdm

def target_resolution(cell_centers:np.ndarray, curr_cell_size:float, max_cell_size:float, hps:Dict):
    hp_centers = hps["hp_centers"]
    sichardt_dists = hps["sichardt_dists"]
    lahm_w = hps["lahm_w"]
    lahm_l = hps["lahm_l"]
    min_cell_size_hp = hps["min_cell_size_hp"]
    min_cell_size_plume = hps["min_cell_size_plume"]

    n_refinement_steps = int(np.log2(max_cell_size / min_cell_size_hp))
    n_refinement_plumes = int(np.log2(max_cell_size / min_cell_size_plume))
    to_refine = False
    if to_refine:
        ress_all = np.ones_like(cell_centers[...,0]) * max_cell_size
        for plume_w, plume_l, hp_center, min_radius in zip(lahm_w, lahm_l, hp_centers, sichardt_dists):
            ress_local = np.ones_like(cell_centers[..., 0]) * max_cell_size
            dist = np.sqrt((cell_centers[..., 0]-hp_center[0]) ** 2 + (cell_centers[..., 1]-hp_center[1]) ** 2) # + (cell_centers[..., 2]-hp_center[2]) ** 2)
            for i in range(n_refinement_steps+1):
                ress_local[dist <= 2*min_radius - i/n_refinement_steps*min_radius] = max_cell_size*2**(-i-1) # cells within 2x sichardt distance are exponentially refined
            ress_local[dist <= curr_cell_size] = min_cell_size_hp

            for j in range(n_refinement_plumes):
                ress_plume = np.ones_like(cell_centers[..., 0]) * max_cell_size
                # set ress_plume to plume_res in the plume. plume is defined as a box with width lahm_w and length lahm_l
                plume = np.logical_and(
                    np.abs(cell_centers[..., 1] - hp_center[1]) <= (2*plume_w - j/n_refinement_plumes*plume_w)/2,
                    # np.logical_and(
                    #     np.abs(cell_centers[..., 2] - hp_center[2]) <= (2*plume_w - j/n_refinement_plumes*plume_w)/2
                    # ),
                    np.logical_and(
                        (cell_centers[...,0] - hp_center[0]) > 0,
                        (cell_centers[...,0] - hp_center[0]) <= 2*plume_l - j/n_refinement_plumes*plume_l
                    )
                )
                ress_plume[plume] = max_cell_size*2**(-j-1)
                ress_local = np.minimum(ress_local, ress_plume)

            ress_all = np.minimum(ress_all, ress_local)
    else:
        constant_cell_size = 0.2
        ress_all = np.ones_like(cell_centers[...,0]) * constant_cell_size
    result = np.stack([ress_all, ress_all, ress_all], axis=-1)
    return result

def plot_grid(cell_centers, face_centers, face_cell_ids, face_areas, cell_volumes):
    face_cell_ids -= 1
    plt.scatter(
        cell_centers[:, 0], cell_centers[:, 1], c="r", label="cell centers", marker="."
    )
    n1 = cell_centers[face_cell_ids[:, 0]]
    n2 = cell_centers[face_cell_ids[:, 1]]
    direction = n2 - n1
    lens = np.sqrt(face_areas) / 1.05
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


def get_grid(
    res_x: int,
    res_y: int,
    res_z: int,
    minx: float,
    maxx: float,
    miny: float,
    maxy: float,
    minz: float,
    maxz: float,
    ids: np.ndarray[int],
    index_offset: int,
    prev_level_highest_id: int,
    target_resolution: Callable[[np.ndarray[float]], np.ndarray[float]],
    max_cell_size:float,
    hps: Dict,
    visualize=False,
):
    """
    res_x: number of cells in x direction
    res_y: number of cells in y direction
    minx, maxx, miny, maxy: domain of this grid
    ids: 2d array of existing cell ids, -1 means no cell. Shape is (res_x+2, res_y+2) to include the cell ids from neighboring grids
    index_offset: the first id to use for this grid
    target_resolution(cell_centers): function that the target resolution at the given positions. cell_centers.shape is (res_x,res_y, 2), output has the same shape, with resolution in x and y separate. calculate for each position, how large the cell should be in x and y direction
    """
    cell_w = (maxx - minx) / res_x
    cell_h = (maxy - miny) / res_y
    cell_d = (maxz - minz) / res_z
    cell_centers = np.stack(
        np.meshgrid(
            np.linspace(minx + cell_w / 2, maxx - cell_w / 2, res_x, endpoint=True),
            np.linspace(miny + cell_h / 2, maxy - cell_h / 2, res_y, endpoint=True),
            np.linspace(minz + cell_d / 2, maxz - cell_d / 2, res_z, endpoint=True),
        )
    ).transpose(2,1,3,0)
    if visualize:
        existing_ids = ids.copy()

    # these cells should not be added to the grid at the current resolution
    assert cell_w == cell_h, "square cells are expected in target_resolution rn"
    target_res = target_resolution(cell_centers, np.maximum(cell_w, cell_h), max_cell_size, hps)
    leave_out = (target_res[..., 0] < cell_w) | (target_res[..., 1] < cell_h) | (target_res[..., 2] < cell_d)

    # only add the cells that are not to be left out and where there is no existing cell
    place_centers = (~leave_out) & (ids[1:-1, 1:-1] == -1)
    ids[1:-1, 1:-1][place_centers] = np.arange(place_centers.sum()) + index_offset

    vertical_face_centers = np.stack(
        np.meshgrid(
            np.linspace(minx,              maxx,              res_x + 1, endpoint=True),
            np.linspace(miny + cell_h / 2, maxy - cell_h / 2, res_y, endpoint=True),
            np.linspace(minz + cell_d / 2, maxz - cell_d / 2, res_z, endpoint=True),
        )
    ).transpose(2,1,3,0)
    horizontal_face_centers = np.stack(
        np.meshgrid(
            np.linspace(minx + cell_w / 2, maxx - cell_w / 2, res_x, endpoint=True),
            np.linspace(miny,              maxy,              res_y + 1, endpoint=True),
            np.linspace(minz + cell_d / 2, maxz - cell_d / 2, res_z, endpoint=True),
        )
    ).transpose(2,1,3,0)
    if ids.shape[2] != 1:
        depth_face_centers = np.stack(  
            np.meshgrid(
                np.linspace(minx + cell_w / 2, maxx - cell_w / 2, res_x, endpoint=True),
                np.linspace(miny + cell_h / 2, maxy - cell_h / 2, res_y, endpoint=True),
                np.linspace(minz + cell_d,     maxz - cell_d,     res_z - 1, endpoint=True), # different because never chunking in z-dir, so there are no neighbours in z-dir
            )
        ).transpose(2,1,3,0)

    # mask out the centers that should not be added
    final_cell_centers = cell_centers[place_centers]

    # no faces when any neighbor has id -1 (you can't "connect" to a non-existing cell)
    valid = ids != -1
    vertical_add = np.ones((res_x + 1, res_y, res_z), dtype=bool)
    horizontal_add = np.ones((res_x, res_y + 1, res_z), dtype=bool)
    if ids.shape[2] != 1:
        depth_add = np.ones((res_x, res_y, res_z - 1), dtype=bool)
    
    left_valid = valid[:-1, 1:-1]
    right_valid = valid[1:, 1:-1]
    vertical_add &= left_valid
    vertical_add &= right_valid

    up_valid = valid[1:-1, 1:]
    down_valid = valid[1:-1, :-1]
    horizontal_add &= down_valid
    horizontal_add &= up_valid

    if ids.shape[2] != 1:
        front_valid = valid[1:-1, 1:-1, :-1]
        back_valid = valid[1:-1, 1:-1, 1:]
        depth_add &= front_valid
        depth_add &= back_valid

    # no faces if both neighbors are from the larger grid
    larger_grid = ids <= prev_level_highest_id
    vertical_add &= ~(larger_grid[:-1, 1:-1] & larger_grid[1:, 1:-1])
    horizontal_add &= ~(larger_grid[1:-1, :-1] & larger_grid[1:-1, 1:])
    if ids.shape[2] != 1:
        depth_add &= ~(larger_grid[1:-1, 1:-1, :-1] & larger_grid[1:-1, 1:-1, 1:])

    # no faces where both neighbors are the same (this is a face inside the same cell)
    vertical_diff_valid = np.diff(ids, axis=0)[:, 1:-1] != 0
    horizontal_diff_valid = np.diff(ids, axis=1)[1:-1, :] != 0
    vertical_add &= vertical_diff_valid
    horizontal_add &= horizontal_diff_valid
    if ids.shape[2] != 1:
        depth_diff_valid = np.diff(ids, axis=2)[1:-1, 1:-1] != 0
        depth_add &= depth_diff_valid

    # apply the masks
    final_vertical_face_centers = vertical_face_centers[vertical_add]
    final_horizontal_face_centers = horizontal_face_centers[horizontal_add]
    if ids.shape[2] != 1:
        final_depth_face_centers = depth_face_centers[depth_add]

    vertical_face_left_neighbor = ids[:-1, 1:-1][vertical_add]
    vertical_face_right_neighbor = ids[1:, 1:-1][vertical_add]
    horizontal_face_down_neighbor = ids[1:-1, :-1][horizontal_add]
    horizontal_face_up_neighbor = ids[1:-1, 1:][horizontal_add]
    if ids.shape[2] != 1:
        depth_face_front_neighbor = ids[1:-1, 1:-1, :-1][depth_add]
        depth_face_back_neighbor = ids[1:-1, 1:-1, 1:][depth_add]

    vertical_face_ids = np.stack(
        [vertical_face_left_neighbor, vertical_face_right_neighbor], axis=-1
    )
    horizontal_face_ids = np.stack(
        [horizontal_face_down_neighbor, horizontal_face_up_neighbor], axis=-1
    )
    if ids.shape[2] != 1:
        depth_face_ids = np.stack(
            [depth_face_front_neighbor, depth_face_back_neighbor], axis=-1
        )

    if ids.shape[2] == 1: 
        final_face_centers = np.concatenate(
            [final_horizontal_face_centers, final_vertical_face_centers]
        )
        final_face_ids = np.concatenate([horizontal_face_ids, vertical_face_ids])
        final_face_areas = np.concatenate(
            [
                np.full(final_horizontal_face_centers.shape[0], cell_w * cell_d),
                np.full(final_vertical_face_centers.shape[0], cell_h * cell_d),
            ]
        )
    else:
        final_face_centers = np.concatenate(
            [final_horizontal_face_centers, final_vertical_face_centers, final_depth_face_centers]
        )
        final_face_ids = np.concatenate([horizontal_face_ids, vertical_face_ids, depth_face_ids])
        final_face_areas = np.concatenate(
            [
                np.full(final_horizontal_face_centers.shape[0], cell_w * cell_d),
                np.full(final_vertical_face_centers.shape[0], cell_h * cell_d),
                np.full(final_depth_face_centers.shape[0], cell_w * cell_h),
            ]
        )

    cell_volume = cell_w * cell_h * cell_d
    final_cell_volumes = np.full(final_cell_centers.shape[0], cell_volume)

    def plot():
        pl_grid = (1, 5)

        def lims():
            plt.xlim(minx - cell_w, maxx + cell_w)
            plt.ylim(miny - cell_h, maxy + cell_h)
            plt.colorbar()

        plt.figure(figsize=(20, 5))
        plt.tight_layout()

        plt.subplot(*pl_grid, 1)
        plt.title("ids input")
        plt.imshow(
            existing_ids.T,
            origin="lower",
            extent=(minx - cell_w, maxx + cell_w, miny - cell_h, maxy + cell_h),
        )
        lims()

        plt.subplot(*pl_grid, 2)
        plt.title("leave out mask")
        plt.imshow(
            leave_out.T,
            origin="lower",
            extent=(minx, maxx, miny, maxy),
        )
        lims()

        plt.subplot(*pl_grid, 3)
        plt.title("place centers mask")
        plt.imshow(place_centers.T, origin="lower", extent=(minx, maxx, miny, maxy))
        lims()

        plt.subplot(*pl_grid, 4)
        plt.title("ids")
        plt.imshow(
            ids.T,
            origin="lower",
            extent=(minx - cell_w, maxx + cell_w, miny - cell_h, maxy + cell_h),
        )
        lims()
        plt.scatter(
            cell_centers.reshape(-1, 2)[:, 0],
            cell_centers.reshape(-1, 2)[:, 1],
            c="r",
            label="cell centers",
            marker="x",
        )
        plt.scatter(
            vertical_face_centers.reshape(-1, 2)[:, 0],
            vertical_face_centers.reshape(-1, 2)[:, 1],
            c="b",
            label="vertical face centers",
            marker="|",
        )
        plt.scatter(
            horizontal_face_centers.reshape(-1, 2)[:, 0],
            horizontal_face_centers.reshape(-1, 2)[:, 1],
            c="g",
            label="horizontal face centers",
            marker="_",
        )

        plt.subplot(*pl_grid, 5)
        plt.title("result")
        plt.imshow(
            ids.T,
            origin="lower",
            extent=(minx - cell_w, maxx + cell_w, miny - cell_h, maxy + cell_h),
        )
        lims()
        plt.scatter(
            final_cell_centers[:, 0],
            final_cell_centers[:, 1],
            c="r",
            label="cell centers",
            marker="x",
        )
        plt.scatter(
            final_vertical_face_centers[:, 0],
            final_vertical_face_centers[:, 1],
            c="b",
            label="vertical face centers",
            marker="|",
        )
        plt.scatter(
            final_horizontal_face_centers[:, 0],
            final_horizontal_face_centers[:, 1],
            c="g",
            label="horizontal face centers",
            marker="_",
        )

        plt.show()

    if visualize:
        plot()

    return (
        final_cell_centers,
        final_face_centers,
        final_face_ids,
        final_face_areas,
        final_cell_volumes,
    )


def double_size(ids, refine_z:bool=False):
    w, h, d = ids.shape
    if refine_z:
        new_ids = -np.ones((w * 2, h * 2, d * 2), dtype=ids.dtype)
        new_ids[::2, ::2, ::2] = ids
        new_ids[1::2, ::2, ::2] = ids
        new_ids[::2, 1::2, ::2] = ids
        new_ids[1::2, 1::2, ::2] = ids
        new_ids[::2, ::2, 1::2] = ids
        new_ids[1::2, ::2, 1::2] = ids
        new_ids[::2, 1::2, 1::2] = ids
        new_ids[1::2, 1::2, 1::2] = ids
    else:
        new_ids = -np.ones((w * 2, h * 2, d), dtype=ids.dtype)
        new_ids[::2, ::2] = ids
        new_ids[1::2, ::2] = ids
        new_ids[::2, 1::2] = ids
        new_ids[1::2, 1::2] = ids
    return new_ids


@dataclass
class Grid:
    """
    res_x: number of cells in x direction, HAS TO BE DIVISIBLE BY chunk_w
    res_y: number of cells in y direction HAS TO BE DIVISIBLE BY chunk_h
    minx, maxx, miny, maxy: domain of this grid
    chunk_w:  number of cells in x direction per chunk, just used during computation
    chunk_h: number of cells in y direction per chunk
    """

    res_x: int
    res_y: int
    res_z: int
    minx: float
    maxx: float
    miny: float
    maxy: float
    minz: float
    maxz: float
    chunk_w: int
    chunk_h: int
    chunk_d: int
    chunks: dict[tuple[int, int, int], "Chunk"] = field(default_factory=dict)
    max_cell_size: float = None

    def __post_init__(self):
        if self.res_x % self.chunk_w != 0:
            raise ValueError("res_x has to be divisible by chunk_w")
        if self.res_y % self.chunk_h != 0:
            raise ValueError("res_y has to be divisible by chunk_h")
        assert self.res_z == 1, "3D not implemented yet"
        assert self.res_z // self.chunk_d == 1, "3D chunking not implemented yet"
        if self.max_cell_size is None:
            self.max_cell_size = np.max([(self.maxx-self.minx)// self.res_x, (self.maxy-self.miny)// self.res_y]) #, (self.maxz-self.minz)//self.res_z]), # to refine, actively excluding z-dim
        
    @property
    def width(self):
        return self.maxx - self.minx

    @property
    def height(self):
        return self.maxy - self.miny

    @property
    def depth(self):
        return self.maxz - self.minz

    def chunk_index(self, x, y, level):
        """
        level 0 is just the base grid, level 1 is the first refinement (factor 2) etc.
        x and y are in the global coordinate system
        """
        # level 0 is no refinement
        n_chunks_x = self.res_x // self.chunk_w * 2**level
        n_chunks_y = self.res_y // self.chunk_h * 2**level
        ix = int((x - self.minx) * n_chunks_x / self.width)
        iy = int((y - self.miny) * n_chunks_y / self.height)
        return ix, iy

    @property
    def xlim(self):
        return self.minx, self.maxx

    @property
    def ylim(self):
        return self.miny, self.maxy
    
    @property
    def zlim(self):
        return self.minz, self.maxz

    def base_chunks(self):
        """
        Yield all chunks that fit in the unrefined base grid
        """
        for x in range(0, self.res_x, self.chunk_w):
            for y in range(0, self.res_y, self.chunk_h):
                yield Chunk(
                    self.chunk_w,
                    self.chunk_h,
                    self.chunk_d,
                    self.minx + x * self.width / self.res_x,
                    self.minx + (x + self.chunk_w) * self.width / self.res_x,
                    self.miny + y * self.height / self.res_y,
                    self.miny + (y + self.chunk_h) * self.height / self.res_y,
                    self.minz,
                    self.maxz,
                    0,
                    self,
                    -np.ones((self.chunk_w, self.chunk_h, self.chunk_d), dtype=int),
                )

    def get_chunk(self, target, center):
        """
        target: tuple of level, idx, idy
        center: tuple of x, y
        try to get the chunk at the given target, if it does not exist, create it from the parent chunks
        """
        level, idx, idy = target
        if target in self.chunks:
            return self.chunks[target]
        if level == 0:
            print(target)

        # not in this level, split parent chunk
        parent = self.get_chunk(
            (level - 1, *self.chunk_index(*center, level - 1)), center
        )
        for x in range(2):
            for y in range(2):
                region_of_interest = parent.indices[
                    x * parent.res_x // 2 : (x + 1) * parent.res_x // 2,
                    y * parent.res_y // 2 : (y + 1) * parent.res_y // 2,
                ]
                # the constructor adds the chunk to the dict of chunks
                id_x, id_y = self.chunk_index(
                    parent.minx + x * parent.width / 2 + parent.width / 4,
                    parent.miny + y * parent.height / 2 + parent.height / 4,
                    level,
                )

                # This chunk exists already, overwriting it would reset the indices
                if (level, id_x, id_y) in self.chunks:
                    continue

                cell_size_x = parent.width/parent.res_x
                cell_size_y = parent.height/parent.res_y
                refine_z = np.max([cell_size_x, cell_size_y]) <= (parent.maxz-parent.minz)/parent.res_z
                Chunk(
                    parent.res_x,
                    parent.res_y,
                    parent.res_z*2 if refine_z else parent.res_z,
                    parent.minx + x * parent.width / 2,
                    parent.minx + (x + 1) * parent.width / 2,
                    parent.miny + y * parent.height / 2,
                    parent.miny + (y + 1) * parent.height / 2,
                    parent.minz,
                    parent.maxz,
                    level,
                    self,
                    double_size(region_of_interest, refine_z=refine_z),
                )
        return self.chunks[target]


@dataclass
class Chunk:
    res_x: int
    res_y: int
    res_z: int
    minx: float
    maxx: float
    miny: float
    maxy: float
    minz: float
    maxz: float
    level: int
    grid: Grid
    indices: np.ndarray[int]

    def __post_init__(self):
        self.idx, self.idy = self.ids()
        # register this chunk in the grid
        chunk_id = (self.level, self.idx, self.idy)
        if chunk_id in self.grid.chunks:
            raise ValueError(f"Chunk {chunk_id} already exists")
        self.grid.chunks[chunk_id] = self

    def ids(self):
        """id of this chunk in the grid in x and y direction"""
        return self.grid.chunk_index(
            (self.minx + self.maxx) / 2, (self.miny + self.maxy) / 2, self.level
        )

    def valid_subdivisions(self):
        """
        Each chunk can be divided into 4 subchunks, this function yields the ones where there is at least one cell that is not yet represented
        """
        for x in range(2):
            for y in range(2):
                region_of_interest = self.indices[
                    x * self.res_x // 2 : (x + 1) * self.res_x // 2,
                    y * self.res_y // 2 : (y + 1) * self.res_y // 2,
                ]
                if (region_of_interest == -1).any():
                    cell_size_x = (self.maxx - self.minx) / self.res_x
                    cell_size_y = (self.maxy - self.miny) / self.res_y
                    refine_z = np.max([cell_size_x, cell_size_y]) <= (self.maxz-self.minz)/self.res_z
                    new_res_z = self.res_z * 2 if refine_z else self.res_z
                    yield Chunk(
                        res_x=self.res_x,
                        res_y=self.res_y,
                        res_z=new_res_z,
                        minx=self.minx + x * (self.maxx - self.minx) / 2,
                        maxx=self.minx + (x + 1) * (self.maxx - self.minx) / 2,
                        miny=self.miny + y * (self.maxy - self.miny) / 2,
                        maxy=self.miny + (y + 1) * (self.maxy - self.miny) / 2,
                        minz=self.minz,
                        maxz=self.maxz,
                        level=self.level + 1,
                        grid=self.grid,
                        indices=double_size(region_of_interest,refine_z=refine_z),
                    )

    def indices_with_neighbors(self):
        """
        This function collects the indices from the neighboring chunks and returns a 2d array with the indices of this chunk and its neighbors, shape is (res_x+2, res_y+2, res_z)
        The newly created array is stored in self.indices and a view returned, so that it can be modified in place by get_grid
        """
        all_indices = -np.ones((self.res_x + 2, self.res_y + 2, self.res_z), dtype=int)
        all_indices[1:-1, 1:-1] = self.indices
        if self.idx > 0:
            # search left neighbor
            target = (self.level, self.idx - 1, self.idy)
            left_position = (
                self.minx - (self.maxx - self.minx) / 2,
                (self.miny + self.maxy) / 2,
            )

            all_indices[0, 1:-1] = self.grid.get_chunk(
                target, left_position
            ).right_border_slice()

        if self.idx < self.grid.res_x // self.grid.chunk_w * 2**self.level - 1:
            # search right neighbor
            target = (self.level, self.idx + 1, self.idy)
            right_position = (
                self.maxx + (self.maxx - self.minx) / 2,
                (self.miny + self.maxy) / 2,
            )
            all_indices[-1, 1:-1] = self.grid.get_chunk(
                target, right_position
            ).left_border_slice()

        if self.idy > 0:
            # search bottom neighbor
            target = (self.level, self.idx, self.idy - 1)
            bottom_position = (
                (self.minx + self.maxx) / 2,
                self.miny - (self.maxy - self.miny) / 2,
            )
            all_indices[1:-1, 0] = self.grid.get_chunk(
                target, bottom_position
            ).top_border_slice()

        if self.idy < self.grid.res_y // self.grid.chunk_h * 2**self.level - 1:
            # search top neighbor
            target = (self.level, self.idx, self.idy + 1)
            top_position = (
                (self.minx + self.maxx) / 2,
                self.maxy + (self.maxy - self.miny) / 2,
            )
            all_indices[1:-1, -1] = self.grid.get_chunk(
                target, top_position
            ).bottom_border_slice()

        # important: make this a view
        self.indices = all_indices[1:-1, 1:-1]
        return all_indices

    @property
    def width(self):
        return self.maxx - self.minx

    @property
    def height(self):
        return self.maxy - self.miny
    
    def right_border_slice(self):
        return self.indices[-1, :]

    def left_border_slice(self):
        return self.indices[0, :]

    def top_border_slice(self):
        return self.indices[:, -1]

    def bottom_border_slice(self):
        return self.indices[:, 0]

    @property
    def extent_xy(self):
        # only used for plotting
        return self.minx, self.maxx, self.miny, self.maxy

    @property
    def center(self):
        # not used
        return (self.minx + self.maxx) / 2, (self.miny + self.maxy) / 2

    def plot(self, ax=None, **kwargs):
        if ax is None:
            ax = plt.gca()
        xmin, xmax, ymin, ymax = self.extent_xy
        ax.add_patch(
            plt.Rectangle(
                (xmin, ymin),
                xmax - xmin,
                ymax - ymin,
                fill=None,
                **kwargs,
            )
        )

    def plot_indices(self, ax=None, **kwargs):
        if ax is None:
            ax = plt.gca()
        ax.imshow(
            self.indices.T,
            origin="lower",
            extent=self.extent_xy,
            **kwargs,
        )


def refine_grid(
    grid:Grid, max_depth:int, target_resolution:Callable, hps: np.ndarray, visualize_grid:bool=False, visualize_steps:bool=False
):
    grid.chunks = {}
    # breadth first, first process all chunks in the unrefined grid
    todos = list(grid.base_chunks())
    results = []
    index_offset = 0
    prev_level_highest_id = -1
    if grid.res_x % grid.chunk_w != 0:
        raise ValueError("res_x has to be divisible by chunk_w")
    if grid.res_y % grid.chunk_h != 0:
        raise ValueError("res_y has to be divisible by chunk_h")

    for level in tqdm(range(max_depth + 1),position=0):
        for chunk in tqdm(todos,position=1,leave=False):
            results.append(
                get_grid(
                    res_x=chunk.res_x,
                    res_y=chunk.res_y,
                    res_z=chunk.res_z,
                    minx=chunk.minx,
                    maxx=chunk.maxx,
                    miny=chunk.miny,
                    maxy=chunk.maxy,
                    minz=chunk.minz,
                    maxz=chunk.maxz,
                    ids=chunk.indices_with_neighbors(),
                    index_offset=index_offset,
                    prev_level_highest_id=prev_level_highest_id,
                    target_resolution=target_resolution,
                    max_cell_size=grid.max_cell_size,
                    hps=hps,
                    visualize=visualize_steps,
                )
            )
            index_offset = max(index_offset, np.max(chunk.indices) + 1)
        prev_level_highest_id = index_offset - 1
        if visualize_grid:
            for chunk in todos:
                chunk.plot(linewidth=(max_depth - level + 1), color="lightblue")
        new_todos = []
        if level == max_depth:
            break
        for chunk in todos:
            new_todos.extend(chunk.valid_subdivisions())
        todos = new_todos
    
    results = [np.concatenate(r) for r in zip(*results)]

    hps_cell_ids = calc_hp_cell_ids(results[0], hps, grid.max_cell_size)
    hps_cell_ids += 1
    results[2] += 1 # cell ids start at 1 in pflotran
    return results, hps_cell_ids

def calc_hp_cell_ids(cell_centers, hps_dict, max_cell_size):
    n_refinement_steps = int(np.log2(max_cell_size/hps_dict["min_cell_size_hp"]))
    smallest_cell_size = max_cell_size*2**(-n_refinement_steps-1)
    hp_ids = []
    # for each hp find cell center it belongs to by assuming all cells are resolved at n_refinement_step_
    for hp_center in hps_dict["hp_centers"]:
        try:
            hp_center = np.array(hp_center)//smallest_cell_size * smallest_cell_size + smallest_cell_size/2
            # dist = np.linalg.norm(cell_centers - hp_center, axis=-1)
            assert hp_center in cell_centers, f"hp_center {hp_center} not in cell_centers "
            hp_line = np.where(np.all(cell_centers == hp_center, axis=-1))[0]
            hp_ids.append(hp_line[0])
        except:
            # get cell_center closest to hp_center
            dist = np.linalg.norm(cell_centers - hp_center, axis=-1)
            hp_line = np.argmin(dist)
            hp_ids.append(hp_line)
    return np.array(hp_ids)


def plot_3d_cells(cell_centers, face_centers, face_cell_ids, face_areas, cell_volumes=None):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot cell centers
    cell_centers = np.array(cell_centers)
    ax.scatter(cell_centers[:, 0], cell_centers[:, 1], cell_centers[:, 2], c='r', marker='o', label='Cell Centers')
    
    face_centers = np.array(face_centers)
    ax.scatter(face_centers[:, 0], face_centers[:, 1], face_centers[:, 2], c='b', marker='o', label='Face Centers')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.legend()
    plt.show()

if __name__ == "__main__":

    # size_x = 1000
    # size_y = 1000
    # grid = Grid(
    #     res_x=10,
    #     res_y=10,
    #     res_z=1,
    #     minx=0,
    #     maxx=size_x,
    #     miny=0,
    #     maxy=size_y,
    #     minz=0,
    #     maxz=50, #000//20,
    #     chunk_w=2,
    #     chunk_h=10,
    #     chunk_d=1, #number of elements per chunk per direction
    #     max_cell_size=100,
    # )
    # max_depth = 5
    # hp_centers = np.array([[200.0, 500.0, 0.5], [600.0,600.0,20.0], [800.0, 200.0,10.0]])
    # sichardt_dists = np.array([50, 100, 10]).astype(np.float32)
    # lahm_l = np.array([500, 200, 100])
    # lahm_w = np.array([160, 200, 50])
    # hps = {
    #     "hp_centers": hp_centers,
    #     "sichardt_dists": sichardt_dists,
    #     "lahm_l": lahm_l,
    #     "lahm_w": lahm_w,
    #     "min_cell_size_hp": 7,
    #     "min_cell_size_plume": 20,
    # }

    # results, hps_ids = refine_grid(grid, max_depth, target_resolution, hps, visualize_grid=True)

    # plt.xlim(grid.xlim)
    # plt.ylim(grid.ylim)
    # plot_grid(*results)
    # print(set(np.sqrt(results[3])))
    # print(set(np.cbrt(results[4])))

    # plot_3d_cells(*results)
    import pathlib
    import h5py

    data = h5py.File(pathlib.Path("/home/pelzerja/pelzerja/test_nn/dataset_generation_laptop/Phd_simulation_groundtruth/outputs/test_refine/RUN_0/pflotran.h5"), "r")
    print(data["   0 Time  0.00000E+00 y"]["Liquid Pressure [Pa]"].shape)
    print(data["   0 Time  0.00000E+00 y"]["Liquid Pressure [Pa]"][:10])
    mesh = h5py.File(pathlib.Path("/home/pelzerja/pelzerja/test_nn/dataset_generation_laptop/Phd_simulation_groundtruth/outputs/test_refine/RUN_0/mesh.h5"), "r")
    print(mesh["Domain"]["Cells"]["Centers"].shape)
    print(mesh["Domain"]["Cells"]["Centers"][:10])
    pressure_275 = np.array(data["   0 Time  0.00000E+00 y"]["Liquid Pressure [Pa]"])
    mesh_cells = np.array(mesh["Domain"]["Cells"]["Centers"])
    mesh_vols = np.array(mesh["Domain"]["Cells"]["Volumes"])
    fig = plt.figure(figsize=(10, 8))
    # top view
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(mesh_cells[:,0], mesh_cells[:,1], mesh_cells[:, 2],  c=np.cbrt(mesh_vols), s=np.sqrt(mesh_vols), cmap="flag")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()