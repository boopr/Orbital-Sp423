"""
Made by Louis ETIENNE
2020-03-03

The code to print table come from https://github.com/CodeForeverAndEver/TableIt
"""

import numpy as np
import matplotlib.pyplot as plt


def find_largest_element(rows, cols, length_array, matrix, format):
    # Loop through each row
    for i in range(rows):
        # Loop through each column
        for j in range(cols):
            if type(matrix[i][j]) is str:
                length_array.append(len(matrix[i][j]))
            else:
                length_array.append(len(f'{matrix[i][j]:{format}}'))
    # Sort the length matrix so that we can find the element with the longest length
    length_array.sort()
    return length_array[-1]


def create_matrix(rows, cols, matrix_to_work_on, matrix, format):
    # Loop through each row
    for i in range(rows):
        # Append a row to matrixToWorkOn for each row in the matrix passed in
        matrix_to_work_on.append([])
        # Loop through each column
        for j in range(cols):
            # Add a each column of the current row (in string form) to matrixToWorkOn
            if type(matrix[i][j]) is str:
                matrix_to_work_on[i].append(matrix[i][j])
            else:
                matrix_to_work_on[i].append(f'{matrix[i][j]:{format}}')


def make_rows(rows, cols, largest_element_length, row_length, matrix_to_work_on, final_table):
    # Loop through each row
    for i in range(rows):
        # Initialize the row that will we work on currently as a blank string
        current_row = ""
        # Loop trhough each column
        for j in range(cols):
            current_el = f' {matrix_to_work_on[i][j]}'

            # If the raw element is less than the largest length of a raw element (raw element is just the unformatted element passed in)
            if largest_element_length != len(matrix_to_work_on[i][j]):
                current_el = current_el + " " * (largest_element_length - len(current_el) + 2) + "|"
            # If the raw element length us equal to the largest length of a raw element then we don't need to add extra spaces
            else:
                current_el = current_el + " " + "|"
            # Now add the current element to the row that we are working on
            current_row += current_el
        # When the entire row that we were working on is done add it as a row to the final table that we will print
        final_table.append("|" + current_row)
    return len(current_row)


def create_wrapping_rows(row_length, final_table):
    # Here we deal with the rows that will go on the top and bottom of the table (look like -> +--------------+), we start by initializing an empty string
    wrapping_rows = ""
    # Then for the length of each row minus one (have to account for the plus that comes at the end, not minus two because rowLength doesn't include the | at the beginning) we add a -
    for i in range(row_length - 1):
        wrapping_rows += "-"
    # Add a plus at the beginning
    wrapping_rows = "+" + wrapping_rows
    # Add a plus at the end
    wrapping_rows += "+"

    # Add the two wrapping rows
    final_table.insert(0, wrapping_rows)
    final_table.append(wrapping_rows)


def create_row_under_fields(largest_element_length, cols, final_table):
    # Initialize the row that will be created
    row_under_fields = ""
    # Loop through each column
    for _ in range(cols):
        # For each column add a plus
        current_el_under_field = "+"
        # Then add an amount of -'s equal to the length of largest raw element and add 2 for the 2 spaces that will be either side the element
        current_el_under_field = current_el_under_field + "-" * (largest_element_length + 2)
        # Then add the current element (there will be one for each column) to the final row that will be under the fields
        row_under_fields += current_el_under_field
    # Add a final plus at the end of the row
    row_under_fields += "+"
    # Insert this row under the first row
    final_table.insert(2, row_under_fields)


def print_rows_in_table(final_table):
    # For each row - print it
    for row in final_table:
        print(row)


def print_table(matrix, use_field_names=False, format=None):
    # Rows equal amount of lists inside greater list
    rows = len(matrix)
    # Cols equal amount of elements inside each list
    cols = len(matrix[0])
    # This is the array to sort the length of each element
    length_array = []
    # This is the variable to store the vakye of the largest length of any element
    largest_element_length = None
    # This is the variable that will store the length of each row
    row_length = None
    # This is the matrix that we will work with throughout this program (main difference between matrix passed in and this matrix is that the matrix that is passed in doesn't always have elements which are all strings)
    matrix_to_work_on = []
    # This the list in which each row will be one of the final table to be printed
    final_table = []

    largest_element_length = find_largest_element(rows, cols, length_array, matrix, format)
    create_matrix(rows, cols, matrix_to_work_on, matrix, format)
    row_length = make_rows(rows, cols, largest_element_length, row_length, matrix_to_work_on, final_table)
    create_wrapping_rows(row_length, final_table)
    if use_field_names:
        create_row_under_fields(largest_element_length, cols, final_table)
    print_rows_in_table(final_table)


def seconds2dhms(time):
    seconds2minute = 60
    seconds2hour = 60 * seconds2minute
    seconds2day = 24 * seconds2hour
    days = time // seconds2day
    time %= seconds2day
    hours = time // seconds2hour
    time %= seconds2hour
    minutes = time // seconds2minute
    time %= seconds2minute
    seconds = time

    return days, hours, minutes, seconds


def compute_t_param(v_deg, excentricity):
    return np.sqrt((1 - np.power(excentricity, 2))) / (1 + excentricity * np.cos(np.deg2rad(v_deg))) * np.sin(np.deg2rad(v_deg))


def determine_correction_for_t(v_c, v):
    if -v_c <= v <= v_c:
        correction = 0
        factor = 1
    elif v < -v_c:
        k = 0
        while v <= -(2 * np.pi) * ((k + 1) // 2) + (-1) ** (k + 1) * v_c:
            k += 1
            correction = -k * np.pi
            factor = (-1) ** k
    else:
        k = 0
        while v >= (2 * np.pi) * ((k + 1) // 2) + (-1) ** k * v_c:
            k += 1
            correction = k * np.pi
            factor = (-1) ** k

    return correction, factor


def compute_t(v_c_deg, v_deg, excentricity, n):
    param = compute_t_param(v_deg, excentricity)
    correction, factor = determine_correction_for_t(np.deg2rad(v_c_deg), np.deg2rad(v_deg))
    return (1 / n) * (correction + factor * np.arcsin(param) - excentricity * param)


def determine_correction_for_lo(w, v, inclinaison):
    if -w - np.pi / 2 <= v <= -w + np.pi / 2:
        correction = 0
        factor = 1
    elif v < -w - np.pi / 2:
        k = 0
        while v <= -w - np.pi * (k + 0.5):
            k += 1
            correction = -k * np.pi
            factor = (-1) ** k
    else:
        k = 0
        while v >= -w + np.pi * (k + 0.5):
            k += 1
            correction = k * np.pi
            factor = (-1) ** k

    if inclinaison > np.pi / 2:
        correction *= -1

    return correction, factor


def compute_lo(w_deg, v_deg, la, inclinaison):
    correction, factor = determine_correction_for_lo(np.deg2rad(w_deg), np.deg2rad(v_deg), np.deg2rad(inclinaison))
    return np.rad2deg(correction) + factor * np.rad2deg(np.arcsin(np.tan(np.deg2rad(la)) / np.tan(np.deg2rad(inclinaison))))

if __name__ == '__main__':
    p = '.' + str(int(input('Nombre de chiffre après la virgule : '))) + 'f'
    a = float(input('[Demi-grand axe (km)] a = '))
    e = float(input('[Excentricité] e = '))
    i = float(input('[Inclinaison (deg)] i = '))
    w = float(input('[Argument du périgé (deg)] w = '))
    L_omega = float(input('[Longitude du noeud ascendant (deg)] L_omega = '))

    # p = '.3f'
    # a = float(40708)
    # e = float(0.8320)
    # i = float(61)
    # w = float(270)
    # L_omega = float(120)

    r_T = 6378  # km : Rayon de la Terre
    mu_T = 398_600  # km^3/s^2 : Paramètre gravitationnel réduit
    l_a = 0 # deg : Latitude du noeud ascendant

    r_A = a * (1 + e)  # km : Rayon de l'apogé
    r_P = a * (1 - e)  # km : Rayon du périgé

    z_A = r_A - r_T  # km : Altitude de l'apogé
    z_P = r_P - r_T  # km : Altitude du périgé

    T = 2 * np.pi * np.sqrt(np.power(a, 3) / mu_T)  # secondes : Temps d'une orbite
    n = np.sqrt(mu_T / np.power(a, 3))  # rad/sec : Moyen mouvement

    V_A = np.sqrt(2 * (-(mu_T / (2*a)) + (mu_T / r_A)))
    V_P = np.sqrt(2 * (-(mu_T / (2*a)) + (mu_T / r_P)))

    print('== Paramètres orbitaux ==')
    print("Distances")
    print(f" - Rayon de l'apogé : rA = {r_A:{p}} km")
    print(f" - Rayon du périgé : rP = {r_P:{p}} km")
    print(f" - Altitude de l'apogé : zA = {z_A:{p}} km")
    print(f" - Altitude du périgé : zP = {z_P:{p}} km")
    print("Temps")
    print(f" - Temps d'une orbite : T = {T:{p}} secondes")
    d, h, m, s = seconds2dhms(T)
    print(f" - Temps d'une orbite : {d} jours {h} heures {m} minutes et {s:{p}} secondes")
    print(f" - Moyen mouvement : n = {n:{p[:-1]}} rad/sec")
    print(f" - Nombre d'orbites par jour : {86400 / T:{p}}")
    print("Vitesses")
    print(f" - Vitesse à l'apogé: VA = {V_A:{p}} km/s")
    print(f" - Vitesse au périgé: VP = {V_P:{p}} km/s")
    print("Orbite")
    if i == 0:
        print(f" - {i}° = 0° : orbite équatoriale")
    elif i == 90:
        print(f" - {i}° = 90° : orbite polaire")
    elif i < 90:
        print(f" - {i}° < 90° : orbite inclinée directe ou orbite prograde")
    elif i > 90:
        print(f" - {i}° > 90° : orbite inclinée indirecte ou orbite rétrograde")

    # Calcul de la trace au sol
    print("\n== Calcul de la trace au sol ==")
    # Anomalie vraie critique v_c
    v_c = np.rad2deg(np.arccos(-e))

    # Temps de passage au périastre
    v = -w
    tp = -compute_t(v_c, v, e, n)
    print(f"Temps de passage au périastre : {tp:{p}} secondes")
    # print("Entrez les anomalies vraies en degré (-60 -30 0 +30 +60 +90) :")
    vs = np.asarray([float(x) for x in input().strip().split(" ")])
    # vs = np.arange(-60, 340, 30)
    ts = np.asarray([compute_t(v_c, vx, e, n) + tp for vx in vs])

    las = np.rad2deg(np.arcsin(np.sin(np.deg2rad(i)) * np.sin(np.deg2rad(w + vs))))
    los = np.asarray([compute_lo(w, vx, la, i) for vx, la in zip(vs, las)])

    alpha_dot = 360 / 86164

    lss = L_omega + los - alpha_dot * ts
    lss_norm = []
    for ls in lss:
        if ls > 180:
            ls -= 360
        elif ls < -180:
            ls += 360
        lss_norm.append(ls)

    to_print = list(zip(vs, ts, las, los, lss, lss_norm))
    to_print.insert(0, ('v[deg]', 't[sec]', 'la[deg]', 'Lo[deg]', 'Ls[deg]', 'Ls[deg] +- 180'))
    print_table(to_print, use_field_names=True, format=p)

    if input('Dessiner les graphiques ? [o/n] ').strip().lower() == 'o':
        plt.figure()
        plt.plot(vs, las, linestyle='--', marker='o')
        plt.title('Latitudes en fonction des anomalies vraies')
        plt.xlabel('v[deg]')
        plt.ylabel('la[deg]')
        plt.grid()

        plt.figure()
        plt.plot(vs, lss_norm, linestyle='--', marker='o')
        plt.title('Longitudes normalisées en fonction des anomalies vraies (Terre tournante)')
        plt.xlabel('v[deg]')
        plt.ylabel('Lo[deg]')
        plt.grid()

        trace = []
        las_group = []
        lss_group = []
        last_is_out_of_bound = False
        for i, ls in enumerate(lss):
            if not -180 < ls < 180 and not last_is_out_of_bound:
                trace.append((las_group, lss_group))
                las_group = [las[i]]
                lss_group = [lss_norm[i]]
                last_is_out_of_bound = True
            else:
                las_group.append(las[i])
                lss_group.append(lss_norm[i])
                if -180 < ls < 180:
                    last_is_out_of_bound = False
        trace.append((las_group, lss_group))

        plt.figure()
        for i, (las_group, lss_group) in enumerate(trace):
            plt.plot(lss_group, las_group, marker='o', label=f'Tracé n°{i + 1}')
        plt.title('Trace du corps')
        plt.plot(lss_norm[0], las[0], ms=10, marker='x', linestyle='None', label='Départ')
        plt.plot(lss_norm[-1], las[-1], ms=10, marker='x', linestyle='None', label='Arrivé')
        plt.grid()
        plt.xlabel('Lo[deg]')
        plt.ylabel('la[deg]')
        plt.axis((-180, 180, -90, 90))
        plt.legend()
        plt.show()
