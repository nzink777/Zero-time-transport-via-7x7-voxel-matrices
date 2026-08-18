import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import dok_matrix

class VoxelGridEngine:
    def __init__(self, size=(50, 50, 50)):
        self.size = size
        self.lattice = dok_matrix((np.prod(size), 7), dtype=np.complex128)
        self.epsilon_planck = 1e-9

    def _coord_to_index(self, coord):
        x, y, z, t = coord
        return x * (self.size[1] * self.size[2]) + y * self.size[2] + z

    def inject_state(self, coord, state_vector):
        idx = self._coord_to_index(coord)
        self.lattice[idx, :] = state_vector

    def compute_energy(self, state_vector):
        return np.sum(np.abs(state_vector)**2)

    def execute_bilateral_swap(self, source_coord, target_coord):
        source_idx = self._coord_to_index(source_coord)
        target_idx = self._coord_to_index(target_coord)

        payload_state = self.lattice[source_idx, :].toarray()[0]
        payload_energy = self.compute_energy(payload_state)

        if payload_energy == 0:
            raise ValueError("Source voxel is empty.")

        # Relocate payload to target coordinate
        self.lattice[target_idx, :] = payload_state

        # Backfill source with equivalent photonic standing wave
        photonic_backfill = np.zeros(7, dtype=np.complex128)
        photonic_backfill[0] = np.sqrt(payload_energy / 2.0)
        photonic_backfill[1] = np.sqrt(payload_energy / 2.0)
        self.lattice[source_idx, :] = photonic_backfill

    def get_energy_slice(self, z_plane):
        grid_slice = np.zeros((self.size[0], self.size[1]))
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                idx = self._coord_to_index((x, y, z_plane, 0))
                state = self.lattice[idx, :].toarray()[0]
                grid_slice[x, y] = self.compute_energy(state)
        return grid_slice

if __name__ == "__main__":
    engine = VoxelGridEngine(size=(50, 50, 50))
    source_address = (15, 15, 10, 0)
    target_address = (35, 35, 10, 0)

    electron_state = np.array([1.0 + 0j, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.complex128)
    engine.inject_state(source_address, electron_state)

    before_slice = engine.get_energy_slice(z_plane=10)
    engine.execute_bilateral_swap(source_address, target_address)
    after_slice = engine.get_energy_slice(z_plane=10)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    im1 = axes[0].imshow(before_slice, cmap='inferno', origin='lower')
    axes[0].set_title("Before Swap: Electron at Source (15,15)")
    fig.colorbar(im1, ax=axes[0], label="Energy Density")

    im2 = axes[1].imshow(after_slice, cmap='inferno', origin='lower')
    axes[1].set_title("After Swap: Relocated & Photonic Backfill")
    fig.colorbar(im2, ax=axes[1], label="Energy Density")

    plt.tight_layout()
    plt.show()
    
