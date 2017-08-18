import pandas as pd
import random
import datetime

df = pd.read_excel("output.xlsx")

conditions_dict = {'Fibroadenoma':0,
                   'Papilloma':25,
                   'Condition 1': 50,
                   'Invasive ductal carcinoma (IDC)': 75,
                   'Mastitis': 100,
                   'Lymphoma': 125,
                   'Fibroadenoma 2': 150,
                   'Lipoma': 175,
                   'INVASIVE LOBULAR CARCINOMA(ILC)' : 200,
                   'Sebaceous cysts': 225,
                   'Galactocele': 250,
                   'Duct ectasia': 275,
                   'Epidermal inclusion cyst': 300,
                   'Fibrocystic breast changes': 325,
                   'Fibroadenoma 3': 350,
                   'Intramammary lymph nodes': 375,
                   'Hamartoma': 400,
                   'Lipoma 2': 425,
                   'Fibromatosis': 450,
                   'Fibrosis': 475,
                   'Adenosis': 500,
                   'Diabetic mastopathy': 525,
                   'Granular cell tumor': 550,
                   'Fat necrosis': 575}

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
        self.m_lymph_n_loc = [7]
        # US
        self.us_mass_loc = [8, 9, 10, 11]
        self.us_calc_loc = [12]
        self.us_lymph_n_loc = [13]
        self.us_sp_c = [14]
        # MRI
        self.mri_mass_loc = [15, 16, 17]
        self.mri_features_loc = [18]
        self.mri_kca_loc = [19]
        self.mri_nme_loc = [20, 21]
        self.mri_nef_loc = [22]
        self.mri_lymph_n_loc = [23]
        self.mri_fcl_loc = [24]

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

def create_report():

    conditions_list = [*conditions_dict]
    condname = random.choice(conditions_list)
    condname_id = conditions_dict.get(condname)

    report = {}

    condition = Condition(cond_name=condname, birads=birads_list, modalities=modalities_list,
                          mammo_findings=mammo_findings_list,us_findings=us_findings_list,
                          mri_findings=mri_findings_list)


    modality = random.choice(condition.modalities)
    #modality = 'Mammography'
    report['modality'] = modality


    if modality == 'Mammography':
        findings_list = condition.mammo_findings
        arr_temp = []
        for i in range(random.randrange(1, len(findings_list))):
            rand_item = random.choice(mammo_findings_list)
            arr_temp.append(rand_item)

        # list of dictionaries for findings
        report[condname] = {'findings': [{'name': x} for x in arr_temp]}

        # create a dict for mass parameters
        mass_ps = create_loc_dict(mammo_mass_params, [(x + condname_id) for x in condition.m_mass_loc])
        mass_lst = [*mass_ps]
        m_params_lst = [{'name': _} for _ in mass_lst]

        # report['conditions'][condname]['findings'] = {'parameters': [{'name': _} for _ in mass_lst]} overrides existed structure
        calc_ps = create_loc_dict(mammo_calc_params, [(x + condname_id) for x in condition.m_calc_loc])
        calc_lst = [*calc_ps]
        calc_params_lst = [{'name': _} for _ in calc_lst]

        assym_ps = create_loc_dict(mammo_assym_params, [(x + condname_id) for x in condition.m_assym_loc])
        assym_lst = [*assym_ps]
        assym_params_lst = [{'name': _} for _ in assym_lst]

        l_nodes_ps = create_loc_dict(mammo_lymph_nodes_params, [(x + condname_id) for x in condition.m_lymph_n_loc])
        l_nodes_lst = [*l_nodes_ps]
        l_nodes_params_lst = [{'name': _} for _ in l_nodes_lst]

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
            elif x == 'Assymetry':
                new_par_assym = []
                for k in range(len(assym_lst)):
                    new_par_assym += [{'value': x} for x in condition.get_random_parameter(assym_ps[assym_lst[k]])]
                paired_vals_assym = [{**x, **y} for (x, y) in zip(assym_params_lst, new_par_assym)]
                ret['parameters'] = paired_vals_assym
            else:
                new_par_l_nodes = []
                for k in range(len(l_nodes_lst)):
                    new_par_l_nodes += [{'value': x} for x in
                                        condition.get_random_parameter(l_nodes_ps[l_nodes_lst[k]])]
                paired_vals_l_nodes = [{**x, **y} for (x, y) in zip(l_nodes_params_lst, new_par_l_nodes)]
                ret['parameters'] = paired_vals_l_nodes
            return ret
    elif modality == 'US':
        findings_list = condition.us_findings
        arr_temp = []
        for i in range(random.randrange(1, len(findings_list))):
            rand_item = random.choice(us_findings_list)
            arr_temp.append(rand_item)

        # list of dictionaries for findings
        report[condname] = {'findings': [{'name': x} for x in arr_temp]}

        # create a dict for mass parameters
        mass_ps = create_loc_dict(us_mass_params, [(x + condname_id) for x in condition.us_mass_loc])
        mass_lst = [*mass_ps]
        m_params_lst = [{'name': _} for _ in mass_lst]

        # report['conditions'][condname]['findings'] = {'parameters': [{'name': _} for _ in mass_lst]} overrides existed structure
        calc_ps = create_loc_dict(us_calc_params, [(x + condname_id) for x in condition.us_calc_loc])
        calc_lst = [*calc_ps]
        calc_params_lst = [{'name': _} for _ in calc_lst]

        l_nodes_ps = create_loc_dict(us_lymph_nodes_params, [(x + condname_id) for x in condition.us_lymph_n_loc])
        l_nodes_lst = [*l_nodes_ps]
        l_nodes_params_lst = [{'name': _} for _ in l_nodes_lst]

        sp_cases_ps = create_loc_dict(us_sp_cases_params, [(x + condname_id) for x in condition.us_sp_c])
        sp_cases_lst = [*sp_cases_ps]
        us_sp_cases_params_lst = [{'name': _} for _ in sp_cases_lst]

        def construct_dict(x):
            ret = {'name': x}
            if x == 'Mass':
                new_par_mass = []
                # a loop for getting random option for each parameter in a finding (as a test used mass)
                for k in range(len(mass_lst)):
                    new_par_mass += [{'value': x} for x in condition.get_random_parameter(mass_ps[mass_lst[k]])]
                paired_vals_mass = [{**x, **y} for (x, y) in zip(m_params_lst, new_par_mass)]
                ret['parameters'] = paired_vals_mass
            elif x == 'Calcifications US':
                new_par_calc = []
                for k in range(len(calc_lst)):
                    new_par_calc += [{'value': x} for x in condition.get_random_parameter(calc_ps[calc_lst[k]])]
                paired_vals_calc = [{**x, **y} for (x, y) in zip(calc_params_lst, new_par_calc)]
                ret['parameters'] = paired_vals_calc
            elif x == 'Special cases':
                new_par_sp_cases = []
                for k in range(len(sp_cases_lst)):
                    new_par_sp_cases += [{'value': x} for x in condition.get_random_parameter(sp_cases_ps[sp_cases_lst[k]])]
                paired_vals_assym = [{**x, **y} for (x, y) in zip(us_sp_cases_params_lst, new_par_sp_cases)]
                ret['parameters'] = paired_vals_assym
            else:
                new_par_l_nodes = []
                for k in range(len(l_nodes_lst)):
                    new_par_l_nodes += [{'value': x} for x in
                                        condition.get_random_parameter(l_nodes_ps[l_nodes_lst[k]])]
                paired_vals_l_nodes = [{**x, **y} for (x, y) in zip(l_nodes_params_lst, new_par_l_nodes)]
                ret['parameters'] = paired_vals_l_nodes
            return ret
    else:
        findings_list = condition.mri_findings
        arr_temp = []
        for i in range(random.randrange(1, len(findings_list))):
            rand_item = random.choice(mri_findings_list)
            arr_temp.append(rand_item)

        # list of dictionaries for findings
        report[condname] = {'findings': [{'name': x} for x in arr_temp]}

        # create a dict for mass parameters
        mass_ps = create_loc_dict(mri_mass_params, [(x + condname_id) for x in condition.mri_mass_loc])
        mass_lst = [*mass_ps]
        m_params_lst = [{'name': _} for _ in mass_lst]

        # report['conditions'][condname]['findings'] = {'parameters': [{'name': _} for _ in mass_lst]} overrides existed structure
        features_ps = create_loc_dict(mri_mri_features_params, [(x + condname_id) for x in condition.mri_features_loc])
        features_lst = [*features_ps]
        features_params_lst = [{'name': _} for _ in features_lst]

        kin_ca_ps = create_loc_dict(mri_kin_c_a_params , [(x + condname_id) for x in condition.mri_kca_loc])
        kin_ca_lst = [*kin_ca_ps]
        kin_ca_params_lst = [{'name': _} for _ in kin_ca_lst]

        nme_ps = create_loc_dict(mri_nme_params, [(x + condname_id) for x in condition.mri_nme_loc])
        nme_ps_lst = [*nme_ps]
        nme_params_lst = [{'name': _} for _ in nme_ps_lst]

        nef_ps = create_loc_dict(mri_nef_params, [(x + condname_id) for x in condition.mri_nef_loc])
        nef_ps_lst = [*nef_ps]
        nef_params_lst = [{'name': _} for _ in nef_ps_lst]

        l_nodes_ps = create_loc_dict(mri_lymph_nodes_params, [(x + condname_id) for x in condition.mri_lymph_n_loc])
        l_nodes_lst = [*l_nodes_ps]
        l_nodes_params_lst = [{'name': _} for _ in l_nodes_lst]

        fcl_ps = create_loc_dict(mri_fcl_params, [(x + condname_id) for x in condition.mri_fcl_loc])
        fcl_ps_lst = [*fcl_ps]
        fcl_params_lst = [{'name': _} for _ in fcl_ps_lst]

        def construct_dict(x):
            ret = {'name': x}
            if x == mri_findings_list[0]:
                new_par_mass = []
                # a loop for getting random option for each parameter in a finding (as a test used mass)
                for k in range(len(mass_lst)):
                    new_par_mass += [{'value': x} for x in condition.get_random_parameter(mass_ps[mass_lst[k]])]
                paired_vals_mass = [{**x, **y} for (x, y) in zip(m_params_lst, new_par_mass)]
                ret['parameters'] = paired_vals_mass
            elif x == mri_findings_list[1]:
                new_par_feat = []
                for k in range(len(features_lst)):
                    new_par_feat+= [{'value': x} for x in
                                         condition.get_random_parameter(features_ps[features_lst[k]])]
                paired_vals_feat = [{**x, **y} for (x, y) in zip(features_params_lst, new_par_feat)]
                ret['parameters'] = paired_vals_feat
            elif x == mri_findings_list[2]:
                new_par_kca = []
                for k in range(len(kin_ca_lst)):
                    new_par_kca += [{'value': x} for x in condition.get_random_parameter(kin_ca_ps[kin_ca_lst[k]])]
                paired_vals_kca = [{**x, **y} for (x, y) in zip(kin_ca_params_lst, new_par_kca)]
                ret['parameters'] = paired_vals_kca
            elif x == mri_findings_list[3]:
                new_par_nme = []
                for k in range(len(nme_ps_lst)):
                    new_par_nme += [{'value': x} for x in
                                         condition.get_random_parameter(nme_ps[nme_ps_lst[k]])]
                paired_vals_nme = [{**x, **y} for (x, y) in zip(nme_params_lst, new_par_nme)]
                ret['parameters'] = paired_vals_nme
            elif x == mri_findings_list[4]:
                new_par_nef = []
                for k in range(len(nef_ps_lst)):
                    new_par_nef += [{'value': x} for x in
                                         condition.get_random_parameter(nef_ps[nef_ps_lst[k]])]
                paired_vals_nef = [{**x, **y} for (x, y) in zip(nef_params_lst, new_par_nef)]
                ret['parameters'] = paired_vals_nef
            elif x == mri_findings_list[5]:
                new_par_l_nodes = []
                for k in range(len(l_nodes_lst)):
                    new_par_l_nodes += [{'value': x} for x in
                                        condition.get_random_parameter(l_nodes_ps[l_nodes_lst[k]])]
                paired_vals_l_nodes = [{**x, **y} for (x, y) in zip(l_nodes_params_lst, new_par_l_nodes)]
                ret['parameters'] = paired_vals_l_nodes
            elif x == mri_findings_list[6]:
                new_par_fcl = []
                for k in range(len(fcl_ps_lst)):
                    new_par_fcl += [{'value': x} for x in
                                    condition.get_random_parameter(fcl_ps[fcl_ps_lst[k]])]
                paired_vals_fcl = [{**x, **y} for (x, y) in zip(fcl_params_lst, new_par_fcl)]
                ret['parameters'] = paired_vals_fcl
            return ret

    report[condname] = {'findings': [construct_dict(x) for x in arr_temp]}

    return report

def multi_report(infile):
    multi_rep = {}
    multi_rep['date_created'] = datetime.datetime.now().strftime('%d %m %Y')
    multi_rep['doctor'] = {}
    multi_rep['doctor']['id'] = random.randint(0, 5001)
    multi_rep['doctor']['name'] = get_name(infile)
    multi_rep['patient'] = {}
    multi_rep['patient']['id'] = random.randint(0, 5001)
    multi_rep['patient']['name'] = get_name(infile)
    multi_rep['conditions'] = {}
    cond_arr =  [(create_report()) for _ in range(1, 4) ]
    multi_rep['conditions'] = cond_arr
    print(multi_rep)
def main():
    """
    TODO:

     4. Add several conditions:
     save current condition and add to another, bigger one

     5. Add random findings (not belonging to any condition)

    """
    #create_report("first-names.txt")
    multi_report(infile="first-names.txt")
if __name__ == '__main__':
    main()
