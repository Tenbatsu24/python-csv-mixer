import pandas as pd
import numpy as np
from scipy.linalg import block_diag
import os

from Student import Student


def init_lists():
    canvas_df = pd.read_csv("../Data/canvas.csv")
    student_df = pd.read_csv("../Data/houses.csv")
    minors_df = pd.read_csv("../Data/exception_minor.csv")
    math_df = pd.read_csv("../Data/only_math.csv")
    do_group_list = student_df['do_group'].dropna().unique()
    houses_list = student_df[student_df['house'] != 'GUEST']['house'].dropna().unique()
    minor_studies_df = minors_df['study'].dropna().unique()
    return student_df, canvas_df, minors_df, math_df, do_group_list, houses_list, minor_studies_df


def generate_history_matrix():
    history_df = pd.DataFrame({})
    for file in os.listdir("../History"):
        if file.endswith(".csv"):
            if history_df.empty:
                history_df = pd.read_csv("{}{}".format("../History/", file))
            else:
                history_df = pd.merge(history_df, pd.read_csv("{}{}".format("../History/", file)), on="s_number")
    return history_df


student_list, canvas_list, exception_minors, exception_only_math, do_groups, houses, minor_studies = init_lists()
print(do_groups, houses, minor_studies)

history_array = generate_history_matrix()

print(student_list.groupby('house')['s_number'].count())
print(student_list.groupby('do_group')['s_number'].count())

student_list = student_list[~student_list['s_number'].isin(exception_only_math['s_number'])]
student_list = student_list[~student_list['s_number'].isin(exception_minors['s_number'])]

print(student_list.groupby('house')['s_number'].count())
print(student_list.groupby('do_group')['s_number'].count())

split_on_do_groups = {}
for do_group in do_groups:
    split_on_do_groups[do_group] = student_list[student_list['do_group'] == do_group]

split_on_houses = {}
for house in houses:
    split_on_houses[house] = student_list[student_list['house'] == house]

split_minors_on_study = {}
for study in minor_studies:
    split_minors_on_study[study] = exception_minors[exception_minors['study'] == study]

do_group_matrix = np.array([], dtype=int)
do_group_student_list = []
for do_group in split_on_do_groups:
    do_group_values = split_on_do_groups[do_group]['s_number'].values

    do_group_student_list += [
        Student(row[0], house=row[1], do_group=row[2])
        for index, row in split_on_do_groups[do_group].iterrows()
    ]

    n = split_on_do_groups[do_group]['s_number'].count()
    sub_matrix = np.zeros((n, n), dtype=int)
    for s_r in range(0, n - 1):
        row_copy = np.arange(1, n)
        for s_c in range(s_r + 1, n):
            week_no = row_copy
            week_no = np.array([x for x in week_no if x not in sub_matrix[:, s_c]])
            week_no = np.array([y for y in week_no if y not in sub_matrix[s_r, :s_c]])
            sub_matrix[s_r][s_c] = sub_matrix[s_c][s_r] = potential = np.random.choice(week_no)
    do_group_matrix = block_diag(do_group_matrix, sub_matrix)

house_student_list = []
house_matrix = np.array([], dtype=int)
for house in houses:
    house_values = split_on_houses[house]['s_number'].values

    house_student_list += [
        Student(row[0], house=row[1])
        for index, row in split_on_houses[house].iterrows()
    ]

    n = split_on_houses[house]['s_number'].count()
    sub_matrix = np.zeros((n, n), dtype=int)
    for s_r in range(0, n - 1):
        row_copy = np.arange(1, n)
        for s_c in range(s_r + 1, n):
            week_no = row_copy
            week_no = np.array([x for x in week_no if x not in sub_matrix[:, s_c]])
            week_no = np.array([y for y in week_no if y not in sub_matrix[s_r, :s_c]])
            sub_matrix[s_r][s_c] = sub_matrix[s_c][s_r] = potential = np.random.choice(week_no)
    house_matrix = block_diag(house_matrix, sub_matrix)

print("Matrix:\n", house_matrix[1:, :])
print(house_student_list[0])
