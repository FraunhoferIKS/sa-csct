# Copyright©[2025] Fraunhofer-Gesellschaft zur Foerderung der angewandten Forschung e.V. acting on behalf of its Fraunhofer-Institut für Kognitive Systeme IKS. All rights reserved.  
# This software is subject to the terms and conditions of the GNU GPLv2 (https://www.gnu.de/documents/gpl-2.0.de.html).

# Contact: andreas.kreutz@iks.fraunhofer.de


import numpy as np

def get_above_and_below(Z, threshold):
    above = Z.copy()
    below = Z.copy()
    above[np.less(Z, threshold)] = np.nan
    below[np.greater_equal(Z, threshold)] = np.nan

    return above, below
