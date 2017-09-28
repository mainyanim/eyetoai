from db_test.cond_data import *

f_mammo = get_cond_population_mri('Fibroadenoma')

import pandas as pd
import random
import datetime
import pymongo
from pymongo import MongoClient
import collections
import bson
from bson.codec_options import CodecOptions



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


def create_report(infile):

    modality = random.choice(df['Modality'].unique())

    multi_rep = {}
    multi_rep['dateCreated'] = datetime.datetime.now().strftime('%d %m %Y')
    multi_rep['doctor'] = {}
    multi_rep['doctor']['id'] = random.randint(0, 5001)
    multi_rep['doctor']['name'] = get_name(infile)
    multi_rep['patient'] = {}
    multi_rep['patient']['id'] = random.randint(0, 5001)
    multi_rep['patient']['name'] = get_name(infile)
    multi_rep['modality'] = modality
    multi_rep['conditions'] = {}



    def subreport():
        report = {}
        report['conditionNname'] = {}
        condname = random.choice(conditions)

        def findings_mammo():
            arr_temp = []
            for i in range(random.randrange(1, len(get_modality('Mammography')[1]))):
                rand_item = random.choice(get_modality('Mammography')[1])
                arr_temp.append(rand_item)
            return arr_temp

        def findings_us():
            arr_temp = []
            for i in range(random.randrange(1, len(get_modality('US')[1]))):
                rand_item = random.choice(get_modality('US')[1])
                arr_temp.append(rand_item)
            return arr_temp

        def findings_mri():
            arr_temp = []
            for i in range(random.randrange(1, len(get_modality('MRI')[1]))):
                rand_item = random.choice(get_modality('MRI')[1])
                arr_temp.append(rand_item)
            return arr_temp


        if modality == 'Mammography':
            arr_temp = get_modality('Mammography')[1]
            add_f = findings_mammo()
            # list of dictionaries for findings
            # create a dict for mass parameters


            def construct_dict(x):
                ret = {'name': x}
                if x == 'Mass':
                    new_par_mass = []
                    loc_params = {}
                    loc_mm = random.uniform(0, 28.5)
                    loc_radar = random.randrange(0, 13)
                    loc_params_dict = {'mm': round(loc_mm, 1), 'time': loc_radar}
                    # a loop for getting random option for each parameter in a finding (as a test used mass)
                    for k in range(len(mass_lst) -1):
                        try:
                            new_par_mass += [{'value': x} for x in condition.get_random_parameter(mass_ps[mass_lst[k]])]
                        except TypeError:
                            pass
                    paired_vals_mass = [{**x, **y} for (x, y) in zip(m_params_lst, new_par_mass)]
                    paired_vals_mass.append(m_params_lst[-1])
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
        """
        elif modality == 'US':
            arr_temp = findings_us()
            add_f = findings_us()

            # list of dictionaries for findings

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
            arr_temp = findings_mri()
            add_f = findings_mri()

            # list of dictionaries for findings

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
        """
        report = {'conditionName': condname, 'findings': [construct_dict(x) for x in arr_temp]}
        def randf():
            c = random.randint(0,1)
            if c == 1:
                multi_rep['nonAssociatedFindings'] = [construct_dict(x) for x in add_f]
            else:
                pass

        randf()
        return report

    cond_arr = [subreport() for _ in range(random.randrange(1, 4))]
    multi_rep['conditions'] = cond_arr
    return multi_rep


def main():
    import pprint
    """"
    client = MongoClient('localhost', 27017)
    db = client.reports
    reportsColl= db.reportsColl

    reports_arr = []
    """
    for _ in range(1):
        report_new = create_report(infile="first-names.txt")
        print(report_new)
        #reports_arr.append(report_new)
    #result = reportsColl.insert_many(reports_arr)
    #print(reportsColl.count())



if __name__ == '__main__':
    main()