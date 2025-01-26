# Copyright©[2025] Fraunhofer-Gesellschaft zur Foerderung der angewandten Forschung e.V. acting on behalf of its Fraunhofer-Institut für Kognitive Systeme IKS. All rights reserved.  
# This software is subject to the terms and conditions of the GNU GPLv2 (https://www.gnu.de/documents/gpl-2.0.de.html).

# Contact: andreas.kreutz@iks.fraunhofer.de


import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

from settings import THRESHOLD

from use_case.fuzzy_constraints.no_humans import get_no_humans_fis
from use_case.fuzzy_constraints.amr_velocity import get_amr_velocity_fis, maximum_velocity

from evaluate.get_above_and_below import get_above_and_below
from evaluate.correctness_over_input_space import evaluate_correctness


N_SAMPLES = 200
location_universe, activity_universe, distance_universe, no_humans_fis = get_no_humans_fis(N_SAMPLES)
load_weight_universe, surface_gradient_universe, amr_velocity_fis = get_amr_velocity_fis(N_SAMPLES)


# Evaluate for single input
inputs = {
    "Location": 1,
    "Activity": 0.4,
    "Distance": 71,
    "LoadWeight": 600,
    "SurfaceGradient": 0.02
}
print("No humans present:", no_humans_fis.compute(inputs, plot=True))
print("AMR speed:", amr_velocity_fis.compute(inputs, plot=True))


# Evaluate over input space
X_humans_present, Y_humans_present = np.meshgrid(activity_universe, distance_universe)
Z_warehouse = np.zeros_like(X_humans_present)
Z_other = np.zeros_like(X_humans_present)
with tqdm(total=N_SAMPLES**2, desc="Humans present") as pbar:
    for i in range(N_SAMPLES):
        for j in range(N_SAMPLES):
            Z_warehouse[i, j] = no_humans_fis.compute({"Location": 0, "Activity": X_humans_present[i, j], "Distance": Y_humans_present[i, j]})
            Z_other[i, j] = no_humans_fis.compute({"Location": 1, "Activity": X_humans_present[i, j], "Distance": Y_humans_present[i, j]})
            pbar.update(1)

# Warehouse
x = X_humans_present[np.greater_equal(Z_warehouse, THRESHOLD)]
y = Y_humans_present[np.greater_equal(Z_warehouse, THRESHOLD)]
print(f"In warehouse: Activity in [{np.min(x)}, {np.max(x)}], distance in [{np.min(y)}, {np.max(y)}]")
# Other
x = X_humans_present[np.greater_equal(Z_other, THRESHOLD)]
y = Y_humans_present[np.greater_equal(Z_other, THRESHOLD)]
print(f"In factory:   Activity in [{np.min(x)}, {np.max(x)}], distance in [{np.min(y)}, {np.max(y)}]")
print()

# Other variables
evaluate_correctness(N_SAMPLES)

Z_warehouse_above, Z_warehouse_below = get_above_and_below(Z_warehouse, THRESHOLD)
Z_other_above, Z_other_below = get_above_and_below(Z_other, THRESHOLD)

X_amr_velocity, Y_amr_velocity = np.meshgrid(load_weight_universe, surface_gradient_universe)
Z_amr_velocity = np.zeros_like(X_amr_velocity)
for i in tqdm(range(N_SAMPLES), "AMR velocity"):
    for j in range(N_SAMPLES):
        Z_amr_velocity[i, j] = amr_velocity_fis.compute({"LoadWeight": X_amr_velocity[i, j], "SurfaceGradient": Y_amr_velocity[i, j]})

Z_velocity_true = maximum_velocity(X_amr_velocity, Y_amr_velocity)
Z_velocity_above, Z_velocity_below = get_above_and_below(Z_amr_velocity, Z_velocity_true)

print(f"{np.sum(np.isnan(Z_velocity_above))} are below the true value")
print(f"{np.sum(np.isnan(Z_velocity_below))} are above the true value")


# Plotting
# Mamdani
plt.rc("text", usetex=True)
figsize = (4.4, 3.5)
warehouse_figure = plt.figure(figsize=figsize)
warehouse = warehouse_figure.add_subplot(111, projection="3d")
warehouse.set_zlim([0, 1])
warehouse.plot_surface(X_humans_present, Y_humans_present, Z_warehouse_above, color="green", vmin=0, vmax=1)
warehouse.plot_surface(X_humans_present, Y_humans_present, Z_warehouse_below, cmap="coolwarm_r", vmin=0, vmax=1)
warehouse.set_xlabel("Measured activity")
warehouse.set_ylabel("Measured worker distance")
warehouse.set_zlabel("Defuzzified fulfillment")

other_figure = plt.figure(figsize=figsize)
other = other_figure.add_subplot(111, projection="3d")
other.set_zlim([0, 1])
other.plot_surface(X_humans_present, Y_humans_present, Z_other_above, color="green", vmin=0, vmax=1)
other.plot_surface(X_humans_present, Y_humans_present, Z_other_below, cmap="coolwarm_r", vmin=0, vmax=1)
other.set_xlabel("Measured activity")
other.set_ylabel("Measured worker distance")
other.set_zlabel("Defuzzified fulfillment")

# Sugeno
velocity_figure = plt.figure(figsize=(figsize[0] * 3, figsize[1]))
velocity = velocity_figure.add_subplot(131, projection="3d")
velocity.plot_surface(X_amr_velocity, Y_amr_velocity, Z_velocity_above, color="red")
velocity.plot_surface(X_amr_velocity, Y_amr_velocity, Z_velocity_below, cmap="coolwarm_r")
velocity.set_xlabel("Measured load weight")
velocity.set_ylabel("Measured surface gradient")
velocity.set_zlabel("Maximum velocity")
velocity.set_title("Inferred velocity")

velocity = velocity_figure.add_subplot(132, projection="3d")
velocity.plot_surface(X_amr_velocity, Y_amr_velocity, Z_velocity_true, cmap="coolwarm_r")
velocity.set_xlabel("Measured load weight")
velocity.set_ylabel("Measured surface gradient")
velocity.set_zlabel("Maximum velocity")
velocity.set_title("True velocity")

velocity = velocity_figure.add_subplot(133, projection="3d")
velocity.plot_surface(X_amr_velocity, Y_amr_velocity, (Z_amr_velocity - Z_velocity_true), cmap="coolwarm_r")
velocity.set_xlabel("Measured load weight")
velocity.set_ylabel("Measured surface gradient")
velocity.set_zlabel("Maximum velocity")
velocity.set_title("Velocity difference")

warehouse_figure.savefig("output/correctness/no_humans_warehouse.png")
other_figure.savefig("output/correctness/no_humans_other.png")
velocity_figure.savefig("output/correctness/amr_velocity.png")
