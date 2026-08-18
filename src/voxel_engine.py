import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import dok_matrix

class VoxelGridEngine:
    def __init__(self, size=(50, 50, 50)):
        self.size = size
        self.lattice = dok_matrix((np.prod(size), 7), dtype=np.complex128)
        self.epsilon_planck = 1e-9

    def _coord_to_index(self, coord):
        # Enforce T^7 toroidal boundary wrapping
        wrapped_coords = tuple(c % self.size[i] for i, c in enumerate(coord[:3])) + (coord[3],)
        x, y, z, t = wrapped_coords
        return x * (self.size[1] * self.size[2]) + y * self.size[2] + z

    def inject_state(self, coord, state_vector):
        idx = self._coord_to_index(coord)
        self.lattice[idx, :] = state_vector

    def compute_energy(self, state_vector):
        return np.sum(np.abs(state_vector)**2)

    def compute_charge(self, state_vector):
        # Assume standard fermionic U(1) charge mapping to the 0th component
        return np.imag(state_vector[0])

    def verify_unitarity(self, matrix_7x7):
        """Verifies U^\dagger U = I for the 7x7 transformation operator."""
        identity_check = np.dot(matrix_7x7.conjugate().T, matrix_7x7)
        identity_matrix = np.eye(7, dtype=np.complex128)
        return np.allclose(identity_check, identity_matrix, atol=1e-7)

    def execute_bilateral_swap(self, source_coord, target_coord, transformation_matrix):
        # 1. Verify Unitarity of the 7x7 matrix before executing
        if not self.verify_unitarity(transformation_matrix):
            raise ValueError("Transformation matrix violates unitarity (U^\dagger U != I). Swap aborted.")

        source_idx = self._coord_to_index(source_coord)
        target_idx = self._coord_to_index(target_coord)

        payload_state = self.lattice[source_idx, :].toarray()[0]
        initial_energy = self.compute_energy(payload_state)
        initial_charge = self.compute_charge(payload_state)

        if initial_energy == 0:
            raise ValueError("Source voxel is empty. No payload to transport.")

        # Apply 7x7 transformation matrix to the payload state vector
        transformed_payload = np.dot(transformation_matrix, payload_state)

        # 2. Relocate payload to target coordinate
        self.lattice[target_idx, :] = transformed_payload

        # 3. Construct equivalent photonic backfill for source coordinate
        photonic_backfill = np.zeros(7, dtype=np.complex128)
        photonic_backfill[0] = np.sqrt(initial_energy / 2.0)
        photonic_backfill[1] = np.sqrt(initial_energy / 2.0)
        self.lattice[source_idx, :] = photonic_backfill

        # 4. Automated Conservation Assertions ($\Delta E = 0, \Delta Q = 0$)
        final_system_energy = self.compute_energy(transformed_payload) + self.compute_energy(photonic_backfill)
        final_system_charge = self.compute_charge(transformed_payload) + self.compute_charge(photonic_backfill)

        delta_e = np.abs(final_system_energy - initial_energy)
        delta_q = np.abs(final_system_charge - initial_charge)

        assert delta_e < 1e-7, f"Energy conservation violation! Delta E = {delta_e}"
        assert delta_q < 1e-7, f"Charge conservation violation! Delta Q = {delta_q}"
        print(f"Swap verified: Delta E = {delta_e:.2e}, Delta Q = {delta_q:.2e} (Passed invariants)")

if __name__ == "__main__":
    engine = VoxelGridEngine(size=(50, 50, 50))
    source_address = (15, 15, 10, 0)
    target_address = (35, 35, 10, 0)

    # Construct a valid unitary 7x7 rotation matrix (mocking the Lie group generator exponentiation)
    np.random.seed(42)
    random_matrix = np.random.randn(7, 7) + 1j * np.random.randn(7, 7)
    q, r = np.linalg.qr(random_matrix)  # QR decomposition yields a unitary matrix
    unitary_7x7 = q

    electron_state = np.array([1.0 + 0j, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.complex128)
    engine.inject_state(source_address, electron_state)

    # Execute with invariant assertions
    engine.execute_bilateral_swap(source_address, target_address, unitary_7x7)
    
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
    
