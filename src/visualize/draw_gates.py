# Copyright©[2025] Fraunhofer-Gesellschaft zur Foerderung der angewandten Forschung e.V. acting on behalf of its Fraunhofer-Institut für Kognitive Systeme IKS. All rights reserved.  
# This software is subject to the terms and conditions of the GNU GPLv2 (https://www.gnu.de/documents/gpl-2.0.de.html).

# Contact: andreas.kreutz@iks.fraunhofer.de


import matplotlib.pyplot as plt
import matplotlib.patches as patches


def draw_or_gate(x, y, size):
    # Draw the left half of the OR gate
    arc1 = patches.Arc((x - size*0.1, y - size/2), size*1.2, size*2.5, theta1=0, theta2=84.175, edgecolor="black")
    plt.gca().add_patch(arc1)

    # Draw the left half of the OR gate
    arc2 = patches.Arc((x + size*0.1, y - size/2), size*1.2, size*2.5, theta1=95.825, theta2=180, edgecolor="black")
    plt.gca().add_patch(arc2)

    # Draw the base line of the OR gate
    arc2 = patches.Arc((x, y - size*1.06), size*1.5, size*1.5, theta1=48, theta2=132, edgecolor="black")
    plt.gca().add_patch(arc2)

    # Draw connecting line
    plt.gca().plot([x, x], [y - size*0.75, y - size*0.4], color="black")


def draw_and_gate(x, y, size):
    # Draw the semicircle part of the AND gate
    arc = patches.Arc((x, y - size/2), size, size*2.5, theta1=0, theta2=180, edgecolor="black")
    plt.gca().add_patch(arc)

    # Draw the base line of the AND gate
    plt.gca().plot([x - size / 2, x + size / 2], [y - size/2, y - size/2], color="black")

    # Draw connecting line
    plt.gca().plot([x, x], [y - size*0.75, y - size*0.5], color="black")
