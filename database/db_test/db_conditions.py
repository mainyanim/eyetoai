from openpyxl import load_workbook
from openpyxl import Workbook
import pandas as pd
import random
import numpy as np

df = pd.read_excel("output.xlsx")

birads_list = ['birad0', 'birad1', 'birad2', 'birad3', 'birad4', 'birad5', 'birad5']
modalities_list = ['Mammography', 'US', 'MRI']

mammo_findigs_list = ['Mass', 'Calcifications', 'Assymetry', 'Lymph nodes']
us_findings_list = ['Mass', 'Calcifications US', 'Lymph nodes', 'Special cases']
mri_findings_list = ['Mass', 'MRI Features', 'Kinetic curve assessment',
                     'Non-mass enhancement (NME)', 'Non-enhancing findings',
                     'Lymph nodes', 'Fat containing lesions']

"""Mammography parameters"""
mammo_mass_params = ['Shape', 'Margin', 'Density']
mammo_calc_params = ['Typically benign', 'Suspicious morphology', 'Distribution']
mammo_assym_params = ['Assymetry']
mammo_lymph_nodes_params = ['Lymph nodes']

"""US parameters"""
us_mass_params = ['Shape', 'Margin', 'Echo', 'Posterior']
us_calc_params = ['Calcifications US']
us_lymph_nodes_params = mammo_lymph_nodes_params
us_sp_cases_params = ['Special cases']

"""MRI parameters"""
mri_mass_params = ['Shape', 'Margin', 'Internal enhancement']
mri_mri_features_params = ['MRI Features']
mri_kin_c_a_params = ['Kinetic curve assessment']
mri_nme_params = ['Distribution', 'Internal enhancement patterns']
mri_nef_params = ['Non-enhancing findings']
mri_lymph_nodes_params = mammo_lymph_nodes_params
mri_fcl_params = ['Fat containing lesions']



class Condition:
    """
    Return all parameters associated with the condition
    """
    def __init__(self, cond_name, birads, modalities, mammo_findings,
                 us_findings, mri_findings):
        self.cond_name = cond_name
        self.birads = birads
        self.modalities = modalities
        self.mammo_findings = mammo_findings
        self.us_findings = us_findings
        self.mri_findings = mri_findings

    @classmethod
    def get_random_parameter(self, row):
        """
            In order to keep up the distribution we need to use method to get random parameter
            :row: the row in the excel file where condition is located. Arrays of rows located in
            the class for each condition and using create_loc_dict function we can store an
            associated data.
            We can use the function given by the key value(fibroadenoma_mass['Shape']).
            Depending on the condition, the only data that can be different is parameter option,
            and mapping to the row we can specify this exact parameter option.
            :return: returns random parameter value (depending on probability)
        """
        start = 14
        stop = 19
        prob_head = list(df)[start:stop]
        width = stop - start
        col = start
        val_arr = []
        prob_arr = []
        for i in range(width):
            value_temp = df.iloc[row, col]
            if isinstance(value_temp, float) is False:
                value = [x.strip() for x in value_temp.split(',')]
                len_val = len(value)
                prob_arr += [prob_head[i] for _ in range(len_val)]
                val_arr += value[0:len_val]
            col += 1
        randparameter = random.choices(val_arr, prob_arr, k=1)
        return randparameter

class Fibroadenoma:
    """
    Every line contains arrays of rows where needed parameters are located.
    For instance, mass has 3 params - shape, margin and density and in excel file
    shape located in the row 0, margin in the row 1, density in the row 3, etc.
    """
    def __init__(self):
        self.mass_loc = [0, 1, 2]
        self.calc_loc = [4, 5, 6]
        self.assym_loc = [6]
        self.lymph_n = [7]

def create_loc_dict(modality_param_arr, param_loc):
    """

    :param modality_param_arr: arrays contains parameters for specified modality
    :param location: array contains probability location defined above in def__init__
    :return: dictionary that allows to fetch data
    """
    data_dict = dict(zip(modality_param_arr, param_loc))
    return data_dict


f = Fibroadenoma()
fibroadenoma_mass = create_loc_dict(mammo_mass_params, f.mass_loc)
fibroadenoma_lymph = create_loc_dict(mammo_lymph_nodes, f.lymph_n)


fibroadenoma = Condition('Fibroadenoma', birads_list, modalities_list, mammo_findigs_list, us_findings_list, mri_findings_list)

print(fibroadenoma.get_random_parameter(fibroadenoma_mass['Shape']))
print(fibroadenoma.get_random_parameter(fibroadenoma_mass['Margin']))
print(fibroadenoma.get_random_parameter(fibroadenoma_mass['Density']))
print(fibroadenoma.get_random_parameter(fibroadenoma_lymph['Lymph nodes']))