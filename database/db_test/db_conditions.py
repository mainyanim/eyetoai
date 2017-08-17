import pandas as pd
import random
import datetime

df = pd.read_excel("output.xlsx")

conditions_dict = {'Fibroadenoma':0, 'Papilloma':25}

birads_list = ['birad0', 'birad1', 'birad2', 'birad3', 'birad4', 'birad5', 'birad5']
modalities_list = ['Mammography', 'US', 'MRI']

mammo_findings_list = ['Mass', 'Calcifications', 'Assymetry', 'Lymph nodes']
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

        """
         Every line contains arrays of rows where needed parameters are located.
         For instance, mass has 3 params - shape, margin and density and in excel file
         shape located in the row 0, margin in the row 1, density in the row 3, etc.
        """

        #Mammography
        self.m_mass_loc = [0, 1, 2]
        self.m_calc_loc = [3, 4, 5]
        self.m_assym_loc = [6]
        self.m_lymph_n = [7]
        # US
        self.us_mass_loc = [8, 9, 10, 11]
        self.us_calc_loc = [12]
        self.us_lymph_n = [13]
        self.us_sp_c = [14]
        # MRI
        self.mri_mass = [15, 16, 17]
        self.mri_features = [18]
        self.mri_kca_ = [19]
        self.mri_nme = [20, 21]
        self.mri_nef = [22]
        self.mri_lymph_n = [23]
        self.mri_fcl = [24]

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


def create_loc_dict(modality_param_arr, param_loc):
    """

    :param modality_param_arr: arrays contains parameters for specified modality
    :param location: array contains probability location defined above in def__init__
    :return: dictionary that allows to fetch data
    """
    data_dict = dict(zip(modality_param_arr, param_loc))
    return data_dict

def get_name(infile):
    with open(infile, 'r') as f:
        contents_of_file = f.read()
        lines = contents_of_file.splitlines()
    line_number = random.randrange(0, len(lines))
    person_name = lines[line_number]
    return person_name

"""
f_new = [(x + 25) for x in f.m_mass_loc]
c0_mammo_mass = create_loc_dict(mammo_mass_params, f_new)
in order to check how can I apply scalar functions to arrs defined these two functions

print(fibroadenoma.get_random_parameter(c0_mammo_mass['Shape']))
print(fibroadenoma.get_random_parameter(f_mammo_mass['Margin']))
print(fibroadenoma.get_random_parameter(f_mammo_mass['Density']))
print(fibroadenoma.get_random_parameter(f_mammo_lymph['Lymph nodes']))
"""

def create_report(infile):
    conditions_list = [*conditions_dict]
    condname = random.choice(conditions_list)
    report = {}
    report['date_created'] = datetime.datetime.now().strftime('%d %m %Y')
    report['doctor'] = {}
    report['doctor']['id'] = random.randint(0,5001)
    report['doctor']['name'] = get_name(infile)
    report['patient'] = {}
    report['patient']['id'] = random.randint(0, 5001)
    report['patient']['name'] = get_name(infile)
    report['conditions'] = {}
    report['conditions']['name'] = condname

    condition = Condition(cond_name=condname, birads=birads_list, modalities=modalities_list,
                          mammo_findings=mammo_findings_list,us_findings=us_findings_list,
                          mri_findings=mri_findings_list)
    #modality = random.choice(condition.modalities)
    modality = 'Mammography'
    report['modality'] = modality


    if modality == 'Mammography':
        findings_list = condition.mammo_findings
    elif modality == 'US':
        findings_list = condition.us_findings
    else:
        findings_list = condition.mri_findings

    arr_temp = []
    for i in range(random.randrange(1,len(findings_list))):
        #rand_item = random.choice(findings_list)
        rand_item = random.choice(mammo_findings_list)
        arr_temp.append(rand_item)

    #list of dictionaries for findings
    report['conditions'][condname] = {'findings': [{'name': x} for x in arr_temp]}

    #create a dict for mass parameters
    mass_ps = create_loc_dict(mammo_mass_params, condition.m_mass_loc)
    mass_lst = [*mass_ps]
    m_params_lst = [{'name': _} for _ in mass_lst]




    #report['conditions'][condname]['findings'] = {'parameters': [{'name': _} for _ in mass_lst]} overrides existed structure
    calc_ps = create_loc_dict(mammo_calc_params, condition.m_calc_loc)
    calc_lst = [*calc_ps]
    calc_params_lst = [{'name': _} for _ in calc_lst]




    def construct_dict(x):
        ret = {'name': x}
        if x == 'Mass':
            new_par_mass = []
            # a loop for getting random option for each parameter in a finding (as a test used mass)
            for k in range(len(mass_lst)):
                new_par_mass += [{'value': x} for x in condition.get_random_parameter(mass_ps[mass_lst[k]])]
            paired_vals_mass = [{**x, **y} for (x, y) in zip(m_params_lst, new_par_mass)]
            ret['parameters'] = paired_vals_mass
        elif x == 'Calcifications':
            new_par_calc = []
            for k in range(len(calc_lst)):
                new_par_calc += [{'value': x} for x in condition.get_random_parameter(calc_ps[calc_lst[k]])]
            paired_vals_calc = [{**x, **y} for (x, y) in zip(calc_params_lst, new_par_calc)]
            ret['parameters'] = paired_vals_calc
        else:
            ret['parameters'] = 'regular_test'
        return ret

    report['conditions'][condname] = {'findings': [construct_dict(x) for x in arr_temp]}


    """report['conditions']['findings'] 
    report['conditions']['findings']['parameters']
    """
    print(report)

def main():
    create_report("first-names.txt")

if __name__ == '__main__':
    main()
