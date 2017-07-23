import pandas as pd
import numpy as np
import random
import json
from openpyxl import load_workbook
import os
from openpyxl import Workbook
import math
from collections import defaultdict

# define values check and append to arr
# define probability array
# read excel

df = pd.read_excel("output.xlsx")
wb = load_workbook('output.xlsx')
ws = wb.get_sheet_by_name('Sheet1')  # Define worksheet


def get_dic_from_two_lists(keys, values):
    return {keys[i]: values[i] for i in range(len(keys))}


# Define function to normalize arr values
def normalize(items):
    problist = [x / sum(items) for x in items]


# def probslist

def concatvals(row, start, stop):
    prob_head = list(df)[start:stop]
    width = stop - start
    col = start
    val_arr = []
    prob_arr = []
    for i in range(width):
        value_temp = df.iloc[row - 2, col]
        if isinstance(value_temp, float) is False:
            value = [x.strip() for x in value_temp.split(',')]
            len_val = len(value)
            prob_arr += [prob_head[i] for _ in range(len_val)]
            val_arr += value[0:len_val]
        col += 1
    randparameter = (", ".join(random.choices(val_arr, prob_arr, k=1)))
    return randparameter


def grab_data(r, s, x, y):
    ps = [concatvals(r + s, x, y)]
    return ps


def create_rep(arr, row_data, condname, modality):  # get findings
    params = []
    # to_json = []
    if condname == 'mass' and modality == 'Mammography':
        for i in range(len(arr)):
            params += grab_data(row_data, 0, 14, 19)
            row_data += 1

    elif condname == 'calcifications' and modality == 'Mammography':
        for i in range(len(arr)):
            params += grab_data(row_data, 3, 14, 19)
            row_data += 1

    elif condname == 'assymetry' and modality == 'Mammography':
        for i in range(len(arr)):
            params += grab_data(row_data, 6, 14, 19)
            row_data += 1

    elif condname == 'lymphNodes' and modality == 'Mammography':
        for i in range(len(arr)):
            params += grab_data(row_data, 7, 14, 19)
            row_data += 1

    elif condname == 'mass' and modality == 'US':
        for i in range(len(arr)):
            params += grab_data(row_data, 8, 14, 19)
            row_data += 1

    elif condname == 'calcificationsUs' and modality == 'US':
        for i in range(len(arr)):
            params += grab_data(row_data, 12, 14, 19)
            row_data += 1

    elif condname == 'lymphNodes' and modality == 'US':
        for i in range(len(arr)):
            params += grab_data(row_data, 13, 14, 19)
            row_data += 1

    elif condname == 'specialCases' and modality == 'US':
        for i in range(len(arr)):
            params += grab_data(row_data, 14, 14, 19)
            row_data += 1

    elif condname == 'mass' and modality == 'MRI':
        for i in range(len(arr)):
            params += grab_data(row_data, 15, 14, 19)
            row_data += 1

    elif condname == 'mriFeatures' and modality == 'MRI':
        for i in range(len(arr)):
            params += grab_data(row_data, 18, 14, 19)
            row_data += 1

    elif condname == 'kineticCurveAssessment' and modality == 'MRI':
        for i in range(len(arr)):
            params += grab_data(row_data, 19, 14, 19)
            row_data += 1

    elif condname == 'nonMassEnhancement(NME)' and modality == 'MRI':
        for i in range(len(arr)):
            params += grab_data(row_data, 20, 14, 19)
            row_data += 1

    elif condname == 'nonEnhancingFindings' and modality == 'MRI':
        for i in range(len(arr)):
            params += grab_data(row_data, 22, 14, 19)
            row_data += 1

    elif condname == 'lymphNodes' and modality == 'MRI':
        for i in range(len(arr)):
            params += grab_data(row_data, 22, 14, 19)
            row_data += 1

    elif condname == 'fatContainingLesions' and modality == 'MRI':
        for i in range(len(arr)):
            params += grab_data(row_data, 24, 14, 19)
            row_data += 1
    fs = get_dic_from_two_lists(arr, params)
    return fs


def get_name(infile):
    with open(infile, 'r') as f:
        contents_of_file = f.read()
        lines = contents_of_file.splitlines()
    line_number = random.randrange(0, len(lines))
    person_name = lines[line_number]
    return person_name


def get_numcond():
    names = len(df.Name.unique())
    return names


def get_cond_name():
    name_arr = df.Name.unique()
    n = list(name_arr)
    n_arr = []
    for i in range(len(name_arr)):
        if (isinstance(n[i], float)) is False:
            n_arr += [n[i]]
    rand_cond_name = random.choice(n_arr)
    return rand_cond_name


def camelCase(st):
    output = ''.join(x for x in st.title() if x.isalpha())
    return output[0].lower() + output[1:]


class AutoTree(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value


def check_row(cond_name):
    from xlrd import open_workbook
    book = open_workbook("output.xlsx")
    for sheet in book.sheets():
        for rowidx in range(sheet.nrows):
            row = sheet.row(rowidx)
            for colidx, cell in enumerate(row):
                if cell.value == cond_name:
                    return rowidx + 1


def get_birad(row, col, width):
    val_head = list(df)[2:9]
    val_arr = []
    prob_arr = []
    for i in range(width):
        value = df.iloc[row - 2, col]
        val_arr += [val_head[i]]
        prob_arr += [value]
        col += 1
    randp = (", ".join(random.choices(val_arr, prob_arr, k=1)))
    return randp


# Create random with parameter of report numbers

def generate_report(infile, items):

    for c in range(items):
        filename = 'report' + str(c) + '.json'
        name = get_cond_name()
        row = check_row(name)
        # Read BiRads Probabilities into list
        # Read BiRads into list
        person_name = get_name(infile)
        p_id = random.randrange(100)
        p_age = random.randrange(25, 65)

        num_cond = random.randrange(1, 5)

        "create list of values and slice empty entities from list"
        rm = df['Relevant modalities'].values.tolist()[0:26]
        #r = 'Mammography'
        r = random.choice(rm)
        # mammo params
        findings = AutoTree()
        findings['report'] = {}
        findings['report']['id'] = p_id
        findings['report']['name'] = person_name
        findings['report']['age'] = p_age
        findings['report']['relevantModality'] = r
        findings['report']['numberOfConditions'] = num_cond

        if r == 'Mammography':
            f_temp = df['Relevant findings'].values.tolist()[0:8]
            f_list = [x for i, x in enumerate(f_temp) if i == f_temp.index(x)]
            f_num_total = len(f_list)
            f_rand = random.randrange(1, f_num_total + 1)
            iter_params_mass = ['shape', 'margin', 'density']
            iter_params_calc = ['typicallyBenign', 'suspiciousMorphology', 'distribution']
            iter_params_a = ['assymetry']
            iter_params_lymph = ['lymphNodes']
            for i in range(num_cond):
                br = get_birad(row, 2, 7)
                cond = camelCase(get_cond_name())
                findings[cond]['biRad'] = br

                findings[cond]['relevantFinding'] = []
                #f = 'mass'
                for k in range(f_rand + 1):
                    f = camelCase(random.choice(f_list))
                    if f == 'mass':
                            rep_temp = create_rep(iter_params_mass, row, f, r)
                            findings[cond]['relevantFinding'] += [{f:rep_temp}]
                            pass
                    elif f == 'calcifications':
                            rep_temp = create_rep(iter_params_calc, row, f, r)
                            findings[cond]['relevantFinding'] += [{f:rep_temp}]
                            pass
                    elif f == 'assymetry':
                            rep_temp = create_rep(iter_params_a, row, f, r)
                            findings[cond]['relevantFinding'] += [{f:rep_temp}]
                            pass
                    elif f == 'lymphNodes':
                            rep_temp = create_rep(iter_params_lymph, row, f, r)
                            findings[cond]['relevantFinding'] += [{f:rep_temp}]
                            pass
            with open(filename, 'w') as f:
                json.dump(findings, f, indent = 4)



        elif r == 'US':
            f_temp = df['Relevant findings'].values.tolist()[8:15]
            f_list = [x for i, x in enumerate(f_temp) if i == f_temp.index(x)]
            f_num_total = len(f_list)
            f_rand = random.randrange(1, f_num_total + 1)

            us_params_mass = ['shape', 'margin', 'echo', 'posterior']
            us_params_calc = ['calcifications']
            us_params_l_nodes = ['lymphNodes']
            us_params_sp_cases = ['specialCases']

            for i in range(num_cond):
                br = get_birad(row, 2, 7)
                cond = camelCase(get_cond_name())
                findings[cond]['biRad'] = br
                findings[cond]['relevantFinding'] = []
                # f = 'mass'
                for k in range(f_rand + 1):
                    f = camelCase(random.choice(f_list))
                    if f == 'mass':
                        rep_temp = create_rep(us_params_mass, row, f, r)
                        findings[cond]['relevantFinding'] += [{f: rep_temp}]

                    elif f == 'calcificationsUs':
                        rep_temp = create_rep(us_params_calc, row, f, r)
                        findings[cond]['relevantFinding'] += [{f: rep_temp}]
                    elif f == 'lymphNodes':
                        rep_temp = create_rep(us_params_l_nodes, row, f, r)
                        findings[cond]['relevantFinding'] += [{f: rep_temp}]
                    else:
                        rep_temp = create_rep(us_params_sp_cases, row, f, r)
                        findings[cond]['relevantFinding'] += [{f: rep_temp}]

            with open(filename, 'w') as f:
                json.dump(findings, f, indent = 4)



        elif r == 'MRI':
            f_temp = df['Relevant findings'].values.tolist()[15:25]
            f_list = [x for i, x in enumerate(f_temp) if i == f_temp.index(x)]
            f_num_total = len(f_list)
            f_rand = random.randrange(1, f_num_total + 1)
            mri_params_mass = ['shape', 'margin', 'internalEnhancement']
            mri_params_mri_f = ['mriFeatures']
            mri_params_kin_c_a = ['kineticCurveAssessment']
            mri_params_nme = ['distribution', 'internalEnhancementPatterns']
            mri_params_nef = ['nonEnhancingPatterns']
            mri_params_l_nodes = ['lymphNodes']
            mri_params_fcl = ['fatContainingLesions']
            for i in range(num_cond):
                br = get_birad(row, 2, 7)
                cond = camelCase(get_cond_name())
                findings[cond]['biRad'] = br
                findings[cond]['relevantFinding'] = []
                # f = 'mass'
                for k in range(f_rand + 1):
                    f = camelCase(random.choice(f_list))
                    if f == 'mass':
                        rep_temp = create_rep(mri_params_mass, row, f, r)
                        findings[cond]['relevantFinding'] += [{f: rep_temp}]

                    elif f == 'mriFeatures':
                        rep_temp = create_rep(mri_params_mri_f, row, f, r)
                        findings[cond]['relevantFinding'] += [{f: rep_temp}]
                    elif f == 'kineticCurveAssessment':
                        rep_temp = create_rep(mri_params_kin_c_a, row, f, r)
                        findings[cond]['relevantFinding'] += [{f: rep_temp}]
                    elif f == 'nonMassEnhancement(NME)':
                        rep_temp = create_rep(mri_params_nme, row, f, r)
                        findings[cond]['relevantFinding'] += [{f: rep_temp}]
                    elif f == 'nonEnhancingFindings':
                        rep_temp = create_rep(mri_params_nef, row, f, r)
                        findings[cond]['relevantFinding'] += [{f: rep_temp}]
                    elif f == 'lymphNodes':
                        rep_temp = create_rep(mri_params_l_nodes, row, f, r)
                        findings[cond]['relevantFinding'] += [{f: rep_temp}]
                    elif f == 'fatContainingLesions':
                        rep_temp = create_rep(mri_params_fcl, row, f, r)
                        findings[cond]['relevantFinding'] += [{f: rep_temp}]
            with open(filename, 'w') as f:
                json.dump(findings, f, indent = 4)


def main():
    generate_report("first-names.txt", 10)

if __name__== "__main__":
  main()