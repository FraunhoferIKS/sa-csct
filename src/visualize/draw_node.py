# Copyright©[2025] Fraunhofer-Gesellschaft zur Foerderung der angewandten Forschung e.V. acting on behalf of its Fraunhofer-Institut für Kognitive Systeme IKS. All rights reserved.  
# This software is subject to the terms and conditions of the GNU GPLv2 (https://www.gnu.de/documents/gpl-2.0.de.html).

# Contact: andreas.kreutz@iks.fraunhofer.de


import matplotlib.pyplot as plt

from src.visualize.draw_gates import draw_and_gate, draw_or_gate


BBOX_STYLES = {
    "refined": {"boxstyle": "square", "facecolor": "white"},
    "context": {"boxstyle": "ellipse", "pad": 0.2, "facecolor": "white"},
    "parameter": {"boxstyle": "ellipse", "pad": 0.2, "linestyle": "dashed", "facecolor": "white"},
    "undeveloped": {"boxstyle": "square", "linestyle": "dashed", "facecolor": "white"},
    "technical": {"facecolor": "white", "edgecolor": "none"}
}


def draw_node(x, y, text, style, scale):
    if style == "and":
        draw_and_gate(x, y, size=20*scale)
    elif style == "or":
        draw_or_gate(x, y, size=20*scale)
    else:
        plt.text(
            x, y, text,
            size=13*scale,
            family="Times New Roman",
            horizontalalignment="center",
            verticalalignment="center",
            bbox=BBOX_STYLES[style]
        )
