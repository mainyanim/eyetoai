from db_test.cond_data import *
import datetime
from pylab import *
import random

def get_name(infile):
    with open(infile, 'r') as f:
        contents_of_file = f.read()
        lines = contents_of_file.splitlines()
    line_number = random.randrange(0, len(lines))
    person_name = lines[line_number]
    return person_name


def findings_mammo():
    arr_temp = []
    for i in range(random.randrange(1, len(get_modality('Mammography').f) + 1)):
        rand_item = random.choice(get_modality('Mammography').f)
        arr_temp.append(rand_item)
    return arr_temp

def findings_us():
    arr_temp = []
    for i in range(random.randrange(1, len(get_modality('US').f) + 1)):
        rand_item = random.choice(get_modality('US').f)
        arr_temp.append(rand_item)
    return arr_temp

def findings_mri():
    arr_temp = []
    for i in range(random.randrange(1, len(get_modality('MRI').f) + 1)):
        rand_item = random.choice(get_modality('MRI').f)
        arr_temp.append(rand_item)
    return arr_temp


def create_report(infile):

    modality = random.choice(df['Modality'].unique())
    #modality = 'Mammography'
    multi_rep = {}
    multi_rep['dateCreated'] = datetime.datetime.now().strftime('%d/%m/%Y')
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
        #condname = random.choice(conditions)
        condname = 'Fibroadenoma'

        if modality == 'Mammography':
            arr_temp = findings_mammo()
            add_f = findings_mammo()
            mammo_m_p = get_cond_population_mammo(condname).mass
            mammo_m_p = np.append(mammo_m_p,'Location')
            mammo_c_p = get_cond_population_mammo(condname).calc
            mammo_a_p = get_cond_population_mammo(condname).assym
            mammo_ln_p = get_cond_population_mammo(condname).lnodes


            m_params_lst = [{'name': _} for _ in mammo_m_p]
            calc_params_lst = [{'name': _} for _ in mammo_c_p]
            assym_params_lst = [{'name': _} for _ in mammo_a_p]
            l_nodes_params_lst = [{'name': _} for _ in mammo_ln_p]

            def construct_dict(x):
                ret = {'name': x}
                if x == 'Mass':
                    new_par_mass = []
                    loc_params = {}
                    loc_mm = random.uniform(0, 28.5)
                    loc_radar = random.randrange(0, 13)
                    loc_params_dict = {'mm': round(loc_mm, 1), 'time': loc_radar}
                    loc_params['parameters'] = loc_params_dict
                    m_params_lst[3].update(loc_params)
                    for k in range(len(mammo_m_p) - 1):

                        try:
                            new_par_mass += [{'value': x} for x in get_cond_population_mammo(condname).marr]
                        except TypeError:
                            pass

                    paired_vals_mass = [{**x, **y} for (x, y) in zip(m_params_lst, new_par_mass)]
                    if 'value' in paired_vals_mass[-1]: del paired_vals_mass[-1]['value']
                    print(paired_vals_mass)
                    ret['parameters'] = paired_vals_mass
                elif x == 'Calcifications':
                    new_par_calc = []
                    new_par_calc += [{'value': x} for x in get_cond_population_mammo(condname).carr]
                    paired_vals_calc = [{**x, **y} for (x, y) in zip(calc_params_lst, new_par_calc)]
                    ret['parameters'] = paired_vals_calc
                elif x == 'Assymetry':
                    new_par_assym = []
                    new_par_assym += [{'value': x} for x in get_cond_population_mammo(condname).aarr]
                    paired_vals_assym = [{**x, **y} for (x, y) in zip(assym_params_lst, new_par_assym)]
                    ret['parameters'] = paired_vals_assym
                else:
                    new_par_l_nodes = []
                    new_par_l_nodes += [{'value': x} for x in get_cond_population_mammo(condname).larr]
                    paired_vals_l_nodes = [{**x, **y} for (x, y) in zip(l_nodes_params_lst, new_par_l_nodes)]
                    ret['parameters'] = paired_vals_l_nodes
                return ret

            report = {'conditionName': condname, 'findings': [construct_dict(x) for x in arr_temp]}



        elif modality == 'US':
            arr_temp = findings_us()
            add_f = findings_us()
            us_m_p = get_cond_population_us(condname).mass
            us_c_p = get_cond_population_us(condname).calc
            us_ln_p = get_cond_population_us(condname).lnodes
            us_sp_c_p = get_cond_population_us(condname).spcases

            m_params_lst = [{'name': _} for _ in us_m_p]
            calc_params_lst = [{'name': _} for _ in us_c_p]
            l_nodes_params_lst = [{'name': _} for _ in us_ln_p]
            sp_c_params_lst = [{'name': _} for _ in us_sp_c_p]

            def construct_dict(x):
                ret = {'name': x}
                if x == 'Mass':
                    new_par_mass = []
                    new_par_mass += [{'value': x} for x in get_cond_population_us(condname).marr]
                    paired_vals_mass = [{**x, **y} for (x, y) in zip(m_params_lst, new_par_mass)]
                    ret['parameters'] = paired_vals_mass
                elif x == 'Calcifications':
                    new_par_calc = []
                    new_par_calc += [{'value': x} for x in get_cond_population_us(condname).carr]
                    paired_vals_calc = [{**x, **y} for (x, y) in zip(calc_params_lst, new_par_calc)]
                    ret['parameters'] = paired_vals_calc
                elif x == 'Lymph nodes':
                    new_par_l_nodes = []
                    new_par_l_nodes += [{'value': x} for x in get_cond_population_us(condname).larr]
                    paired_vals_l_nodes = [{**x, **y} for (x, y) in zip(l_nodes_params_lst, new_par_l_nodes)]
                    ret['parameters'] = paired_vals_l_nodes
                else:
                    new_par_sp_c = []
                    new_par_sp_c += [{'value': x} for x in get_cond_population_us(condname).sparr]
                    paired_vals_l_nodes = [{**x, **y} for (x, y) in zip(sp_c_params_lst, new_par_sp_c)]
                    ret['parameters'] = paired_vals_l_nodes
                return ret

            report = {'conditionName': condname, 'findings': [construct_dict(x) for x in arr_temp]}



        elif modality == 'US':
            arr_temp = findings_mri()
            add_f = findings_mri()
            mri_m_p = get_cond_population_mri(condname).mass
            mri_feat_p = get_cond_population_mri(condname).mrif
            mri_kin_c_p = get_cond_population_mri(condname).kca
            mri_nme_p = get_cond_population_mri(condname).nme
            mri_nef_p = get_cond_population_mri(condname).nef
            mri_ln_p = get_cond_population_mri(condname).lnodes
            mri_fcl_p = get_cond_population_mri(condname).fcl

            m_params_lst = [{'name': _} for _ in mri_m_p]
            features_params_lst = [{'name': _} for _ in mri_feat_p]
            kin_ca_params_lst = [{'name': _} for _ in mri_kin_c_p]
            nme_params_lst = [{'name': _} for _ in mri_nme_p]
            nef_params_lst = [{'name': _} for _ in mri_nef_p]
            l_nodes_params_lst = [{'name': _} for _ in mri_ln_p]
            fcl_params_lst = [{'name': _} for _ in mri_fcl_p]

            def construct_dict(x):
                ret = {'name': x}
                if x == 'Mass':
                    new_par_mass = []
                    new_par_mass += [{'value': x} for x in get_cond_population_mri(condname).marr]
                    paired_vals_mass = [{**x, **y} for (x, y) in zip(m_params_lst, new_par_mass)]
                    ret['parameters'] = paired_vals_mass
                elif x == 'MRI Features':
                    new_par_feat = []
                    new_par_feat += [{'value': x} for x in get_cond_population_mri(condname).mrif]
                    paired_vals_feat = [{**x, **y} for (x, y) in zip(features_params_lst, new_par_feat)]
                    ret['parameters'] = paired_vals_feat
                elif x =='Kinetic curve assessment':
                    new_par_kca = []
                    new_par_kca += [{'value': x} for x in get_cond_population_mri(condname).kca]
                    paired_vals_kca = [{**x, **y} for (x, y) in zip(kin_ca_params_lst, new_par_kca)]
                    ret['parameters'] = paired_vals_kca
                elif x == 'Non - mass enhancement(NME)':
                    new_par_nme = []
                    new_par_nme += [{'value': x} for x in get_cond_population_mri(condname).nme]
                    paired_vals_nme = [{**x, **y} for (x, y) in zip(nme_params_lst, new_par_nme)]
                    ret['parameters'] = paired_vals_nme
                elif x == 'Non - enhancing findings':
                    new_par_nef = []
                    new_par_nef += [{'value': x} for x in get_cond_population_mri(condname).nef]
                    paired_vals_nef = [{**x, **y} for (x, y) in zip(nef_params_lst, new_par_nef)]
                    ret['parameters'] = paired_vals_nef
                elif x == 'Lymph nodes':
                    new_par_l_nodes = []
                    new_par_l_nodes += [{'value': x} for x in get_cond_population_mri(condname).lnodes]
                    paired_vals_l_nodes = [{**x, **y} for (x, y) in zip(l_nodes_params_lst, new_par_l_nodes)]
                    ret['parameters'] = paired_vals_l_nodes
                elif x == 'Fat containing lesions':
                    new_par_fcl = []
                    new_par_fcl += [{'value': x} for x in get_cond_population_mri(condname).fcl]
                    paired_vals_fcl = [{**x, **y} for (x, y) in zip(fcl_params_lst, new_par_fcl)]
                    ret['parameters'] = paired_vals_fcl
                return ret

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
    print(multi_rep)
    return multi_rep



def main():
    create_report(infile='names.txt')


if __name__ == '__main__':
    main()


