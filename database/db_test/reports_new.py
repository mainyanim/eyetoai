import pandas as pd
import sys
from sklearn import preprocessing
import numpy as np
import random

df = pd.read_excel('F:\Work\db\eyetoai\eyetoai\database\db_test\data.xlsx')


def get_val_prob(finding, group, condition):
    mod_find_group = finding.groupby(['Parameter']).get_group(group)
    group_val = mod_find_group['Value'].unique()
    prob = list(mod_find_group[condition])
    return group_val, prob


def get_population(arr):
    population = random.choices(arr[0], weights=arr[1], k=1)
    return population


def get_modality(modality):
    mod = df.groupby(['Modality']).get_group(modality)
    f = mod['Finding'].unique()
    return mod, f


def get_finding_param(modality, cond_findings, idx):
    mod_finding = modality.groupby(['Finding']).get_group(cond_findings[idx])
    mod_f_params = mod_finding['Parameter'].unique()
    return mod_finding, mod_f_params


def get_cond_population_mammo(condition):
    # Mammo
    mammo = get_modality('Mammography')[0]
    mammo_findings = get_modality('Mammography')[1]

    # mass
    mammo_mass = get_finding_param(mammo, mammo_findings, 0)[0]
    mammo_m_p = get_finding_param(mammo, mammo_findings, 0)[1]

    mammo_mass_shape_prob = get_val_prob(mammo_mass, mammo_m_p[0], condition)
    mammo_mass_margin_prob = get_val_prob(mammo_mass, mammo_m_p[1], condition)
    mammo_mass_density_prob = get_val_prob(mammo_mass, mammo_m_p[2], condition)

    p_mass_shape_cond = get_population(mammo_mass_shape_prob)
    p_mass_margin_cond = get_population(mammo_mass_margin_prob)
    p_mass_density = get_population(mammo_mass_density_prob)

    # calcification
    mammo_calc = get_finding_param(mammo, mammo_findings, 1)[0]
    mammo_c_p = get_finding_param(mammo, mammo_findings, 1)[1]

    mammo_calc_tb_prob = get_val_prob(mammo_calc, mammo_c_p[0], condition)
    mammo_calc_s_m_prob = get_val_prob(mammo_calc, mammo_c_p[1], condition)
    mammo_calc_d_prob = get_val_prob(mammo_calc, mammo_c_p[2], condition)

    p_c_tb = get_population(mammo_calc_tb_prob)
    p_c_sm = get_population(mammo_calc_s_m_prob)
    p_c_d = get_population(mammo_calc_d_prob)

    # assymetry
    mammo_assym = get_finding_param(mammo, mammo_findings, 2)[0]
    mammo_a_p = get_finding_param(mammo, mammo_findings, 2)[1]

    mammo_assym_prob = get_val_prob(mammo_assym, mammo_a_p[0], condition)
    p_assym = get_population(mammo_assym_prob)

    # l_nodes
    mammo_l_nodes = get_finding_param(mammo, mammo_findings, 3)[0]
    mammo_ln_p = get_finding_param(mammo, mammo_findings, 3)[1]

    mammo_ln_prob = get_val_prob(mammo_l_nodes, mammo_ln_p[0], condition)

    p_lnodes = get_population(mammo_ln_prob)

    # list of populated values
    populations = [[p_mass_shape_cond, p_mass_margin_cond, p_mass_density],
                   [p_c_tb, p_c_sm, p_c_d], p_assym, p_lnodes]

    return populations


f = get_cond_population_mammo('Fibroadenoma')
print(f)