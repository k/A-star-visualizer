# Aggregate each heuristic across all algorithms
# Aggregate each heuristic modifier across a_star
# Aggregate each algorithm across all heuristics
# Aggregate each anchor heuristic for a_star_sequential a_star_integrated
# Aggregate each modifier across all algorithms
#
# These can be done in excel by duplicating the sheet and sorting/aggregating:
# Fix w1, increase w2 as function of running time
# Fix w2, increase w1 as functino of running time
import csv
import numpy as np


base_names = ['c', 'm', 'd', 'e']
modifier_names = ['a', 'f', 's']
algorithm_names = ['uniform_cost_search', 'a_star', 'a_star_w', 'a_star_sequential', 'a_star_integrated']


def aggregate_heuristics(writer, n, header):
    writer.writerow(['Heuristic'] + header[5:10])
    for h in base_names:
        arr = []
        for r in n:
            if h in r[1]:
                arr.append(r[5:10])
        mean = np.mean(np.array(arr).astype('float'), 0)
        str_list = [h] + list(mean.astype('str'))
        writer.writerow(str_list)

    for m in modifier_names:
        arr = []
        for r in n:
            if m in r[1]:
                arr.append(r[5:10])
        mean = np.mean(np.array(arr).astype('float'), 0)
        str_list = [m] + list(mean.astype('str'))
        writer.writerow(str_list)

    for h in base_names:
        for m in modifier_names:
            arr = []
            for r in n:
                if h+m in r[1]:
                    arr.append(r[5:10])
            mean = np.mean(np.array(arr).astype('float'), 0)
            str_list = [h+m] + list(mean.astype('str'))
            writer.writerow(str_list)

dname = 'csv-2-19/'
fname = 'benchmarks.csv'
new_fnames = ['heuristics.csv', 'heuristics-astar.csv', 'algorithms.csv',
              'sorted-w1.csv', 'sorted-w2.csv', 'sorted-w1-w2.csv', 'anchors.csv']

with open(dname + fname, 'r') as csvreadfile:
    m = np.genfromtxt(csvreadfile, dtype='str', delimiter=',')
    header = list(m[0])
    with open(dname + new_fnames[0], 'w') as csvwritefile:
        writer = csv.writer(csvwritefile, quoting=csv.QUOTE_MINIMAL)
        aggregate_heuristics(writer, m[1:], header)

    with open(dname + new_fnames[1], 'w') as csvwritefile:
        writer = csv.writer(csvwritefile, quoting=csv.QUOTE_MINIMAL)

        a_stars = []  # Filter to find a_stars
        for r in m[1:]:
            if r[0] == 'a_star':
                a_stars.append(r)

        n = np.array(a_stars)
        aggregate_heuristics(writer, n, header)

    with open(dname + new_fnames[2], 'w') as csvwritefile:
        writer = csv.writer(csvwritefile, quoting=csv.QUOTE_MINIMAL)
        writer.writerow([header[0]] + header[5:10])
        for a in algorithm_names:
            filtered = []  # Filter to find a_stars
            for r in m[1:]:
                if a == 'a_star_w':
                    if r[0] == 'a_star' and r[2].astype('float') > 1:
                        filtered.append(r)
                elif a == 'a_star':
                    if r[0] == 'a_star' and r[2].astype('float') == 1:
                        filtered.append(r)
                elif r[0] == a:
                    filtered.append(r)
            arr = []
            for r in filtered:
                arr.append(r[5:10])

            mean = np.mean(np.array(arr).astype('float'), 0)
            str_list = [a] + list(mean.astype('str'))
            writer.writerow(str_list)

# w1 sorted
    with open(dname + new_fnames[3], 'w') as csvwritefile:
        writer = csv.writer(csvwritefile, quoting=csv.QUOTE_MINIMAL)
        writer.writerow([header[2]]+header[5:10])
        for w in [1, 1.25, 2, 3, 4, 10]:
            arr = []
            for r in m[1:]:
                if r[2] != '' and float(r[2]) == w:
                    arr.append(r[5:10])
            mean = np.mean(np.array(arr).astype('float'), 0)
            str_list = [w] + list(mean.astype('str'))
            writer.writerow(str_list)

# w2 sorted
    with open(dname + new_fnames[4], 'w') as csvwritefile:
        writer = csv.writer(csvwritefile, quoting=csv.QUOTE_MINIMAL)
        writer.writerow([header[3]]+header[5:10])
        for w in [1, 1.25, 2, 3, 4, 10]:
            arr = []
            for r in m[1:]:
                if r[3] != '' and float(r[3]) == w:
                    arr.append(r[5:10])
            mean = np.mean(np.array(arr).astype('float'), 0)
            str_list = [w] + list(mean.astype('str'))
            writer.writerow(str_list)

# w1, w2 sorted
    with open(dname + new_fnames[5], 'w') as csvwritefile:
        writer = csv.writer(csvwritefile, quoting=csv.QUOTE_MINIMAL)
        writer.writerow([header[2], header[3]]+header[5:10])
        for w1 in [1, 1.25, 2, 3, 4, 10]:
            filtered = []
            for r in m[1:]:
                if r[2] != ''and float(r[2]) == w1:
                    filtered.append(r)

            for w2 in [1, 1.25, 2, 3, 4, 10]:
                arr = []
                for r in filtered:
                    if r[3] != ''and float(r[3]) == w2:
                        arr.append(r[5:10])
                mean = np.mean(np.array(arr).astype('float'), 0)
                str_list = [w1, w2] + list(mean.astype('str'))
                writer.writerow(str_list)
