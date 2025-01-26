# Copyright©[2025] Fraunhofer-Gesellschaft zur Foerderung der angewandten Forschung e.V. acting on behalf of its Fraunhofer-Institut für Kognitive Systeme IKS. All rights reserved.  
# This software is subject to the terms and conditions of the GNU GPLv2 (https://www.gnu.de/documents/gpl-2.0.de.html).

# Contact: andreas.kreutz@iks.fraunhofer.de


from math import ceil


def wrap_label(label, max_length, no_single_lines=True):
    lines = []
    line = []
    for word in label.split(" "):
        if len(" ".join(line + [word])) > max_length:
            lines.append(line)
            line = []
        line.append(word)
    lines.append(line)

    if no_single_lines and len(lines) == 1:
        n_words_first_line = ceil(len(lines[0])/2)
        lines = [lines[0][:n_words_first_line], lines[0][n_words_first_line:]]
    if len(lines) == 2:
        def length(lines):
            return max(
                sum(len(word) for word in lines[0]),
                sum(len(word) for word in lines[1])
            )

        best_lines = lines
        for i in range(len(lines[0])):
            new_lines= [lines[0][:i], lines[0][i:] + lines[1]]
            if length(new_lines) < length(best_lines):
                best_lines = new_lines
        lines = best_lines
    return "\n".join([" ".join(line) for line in lines])
