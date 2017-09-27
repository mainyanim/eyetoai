import pandas as pd
import random
import collections

import sys
from sklearn import preprocessing
import numpy as np


df = pd.read_excel('F:\Work\db\eyetoai\eyetoai\database\db_test\data.xlsx')
conditions = list(df)[4:]

def get_val_prob(finding, group, condition):
    mod_find_group = finding.groupby(['Parameter']).get_group(group)
    group_val = mod_find_group['Value'].unique()
    prob = list(mod_find_group[condition])
    return group_val, prob


def get_population(arr):
    popul = random.choices(arr[0], weights=arr[1], k=1)
    return popul


def get_modality(modality):
    ModalityData = collections.namedtuple('ModalityData', 'mod f')
    mod = df.groupby(['Modality']).get_group(modality)
    f = mod['Finding'].unique()
    modality_data = ModalityData(mod=mod, f = f)
    return modality_data


def get_finding_param(modality, cond_findings, idx):
    Data = collections.namedtuple('Data', 'finding params')
    mod_finding = modality.groupby(['Finding']).get_group(cond_findings[idx])
    mod_f_params = mod_finding['Parameter'].unique()
    data = Data(finding=mod_finding,params=mod_f_params)
    return data


def get_cond_population_mammo(condition):
    ConditionData = collections.namedtuple('ConditionData', 'mass calc assym lnodes'
                                                            ' marr carr aarr larr')
    # Mammo
    mammo = get_modality('Mammography').mod
    mammo_findings = get_modality('Mammography').f

    # mass
    mammo_mass = get_finding_param(mammo, mammo_findings, 0).finding
    mammo_m_p = get_finding_param(mammo, mammo_findings, 0).params

    mammo_mass_shape_prob = get_val_prob(mammo_mass, mammo_m_p[0], condition)
    mammo_mass_margin_prob = get_val_prob(mammo_mass, mammo_m_p[1], condition)
    mammo_mass_density_prob = get_val_prob(mammo_mass, mammo_m_p[2], condition)

    p_mass_shape = get_population(mammo_mass_shape_prob)
    p_mass_margin = get_population(mammo_mass_margin_prob)
    p_mass_density = get_population(mammo_mass_density_prob)

    # calcification
    mammo_calc = get_finding_param(mammo, mammo_findings, 1).finding
    mammo_c_p = get_finding_param(mammo, mammo_findings, 1).params

    mammo_calc_tb_prob = get_val_prob(mammo_calc, mammo_c_p[0], condition)
    mammo_calc_s_m_prob = get_val_prob(mammo_calc, mammo_c_p[1], condition)
    mammo_calc_d_prob = get_val_prob(mammo_calc, mammo_c_p[2], condition)

    p_c_tb = get_population(mammo_calc_tb_prob)
    p_c_sm = get_population(mammo_calc_s_m_prob)
    p_c_d = get_population(mammo_calc_d_prob)

    # assymetry
    mammo_assym = get_finding_param(mammo, mammo_findings, 2).finding
    mammo_a_p = get_finding_param(mammo, mammo_findings, 2).params

    mammo_assym_prob = get_val_prob(mammo_assym, mammo_a_p[0], condition)
    p_assym = get_population(mammo_assym_prob)

    # l_nodes
    mammo_l_nodes = get_finding_param(mammo, mammo_findings, 3).finding
    mammo_ln_p = get_finding_param(mammo, mammo_findings, 3).params

    mammo_ln_prob = get_val_prob(mammo_l_nodes, mammo_ln_p[0], condition)

    p_lnodes = get_population(mammo_ln_prob)
    mass_arr = [*p_mass_shape, *p_mass_margin, *p_mass_density]
    calc_arr = [*p_c_tb, *p_c_sm, *p_c_d]

    # list of populated values
    condition_data = ConditionData(mass=mammo_m_p, calc=mammo_c_p,
                                   assym=mammo_a_p, lnodes=mammo_ln_p,
                                   marr = mass_arr, carr = calc_arr,
                                   aarr= p_assym, larr= p_lnodes)

    return condition_data


def get_cond_population_us(condition):
    # US
    ConditionData = collections.namedtuple('ConditionData', 'mass calc lnodes spcases '
                                                            ' marr carr larr sparr')
    us = get_modality('US').mod
    us_findings = get_modality('US').f

    # array(['Mass', 'Calcifications US', 'Lymph nodes', 'Special cases'], dtype=object)

    # mass
    us_mass = get_finding_param(us, us_findings, 0).finding
    us_m_p = get_finding_param(us, us_findings, 0).params

    us_mass_shape_prob = get_val_prob(us_mass, us_m_p[0], condition)
    us_mass_margin_prob = get_val_prob(us_mass, us_m_p[1], condition)
    us_mass_echo_prob = get_val_prob(us_mass, us_m_p[2], condition)
    us_mass_posterior_prob = get_val_prob(us_mass, us_m_p[3], condition)

    p_mass_shape = get_population(us_mass_shape_prob)
    p_mass_margin = get_population(us_mass_margin_prob)
    p_mass_echo = get_population(us_mass_echo_prob)
    p_mass_posterior = get_population(us_mass_posterior_prob)

    # calcifications
    us_calc = get_finding_param(us, us_findings, 1).finding
    us_calc_p = get_finding_param(us, us_findings, 1).params

    us_calc_us_prob = get_val_prob(us_calc, us_calc_p[0], condition)
    p_us_calc_us = get_population(us_calc_us_prob)

    # lymph nodes

    us_ln = get_finding_param(us, us_findings, 2).finding
    us_ln_p = get_finding_param(us, us_findings, 2).params

    us_ln_prob = get_val_prob(us_ln, us_ln_p[0], condition)
    p_us_ln = get_population(us_ln_prob)

    # special cases
    us_sp_c = get_finding_param(us, us_findings, 3).finding
    us_sp_c_p = get_finding_param(us, us_findings, 3).params

    us_sp_c_prob = get_val_prob(us_sp_c, us_sp_c_p[0], condition)
    p_us_sp_c = get_population(us_sp_c_prob)

    mass_arr = [*p_mass_shape, *p_mass_margin, *p_mass_echo, *p_mass_posterior]

    condition_data = ConditionData(mass=us_m_p, calc=us_calc_p,
                                   lnodes=us_ln_p,spcases=us_sp_c_p,
                                   marr=mass_arr, carr=p_us_calc_us,
                                   larr=p_us_ln, sparr=p_us_sp_c)
    return condition_data

def get_cond_population_mri(condition):
    # MRI
    ConditionData = collections.namedtuple('ConditionData', 'mass mrif kca nme'
                                                            ' nef lnodes fcl '
                                                            ' marr mrifarr kcaarr '
                                                            ' nmearr nefarr lnarr fclarr')
    mri = get_modality('MRI').mod
    mri_findings = get_modality('MRI').f


    # mass
    mri_mass = get_finding_param(mri, mri_findings, 0).finding
    mri_m_p = get_finding_param(mri, mri_findings, 0).params

    mri_mass_shape_prob = get_val_prob(mri_mass, mri_m_p[0], condition)
    mri_mass_margin_prob = get_val_prob(mri_mass, mri_m_p[1], condition)
    mri_mass_int_enh = get_val_prob(mri_mass, mri_m_p[2], condition)

    p_mass_shape = get_population(mri_mass_shape_prob)
    p_mass_margin = get_population(mri_mass_margin_prob)
    p_mass_int_enh = get_population(mri_mass_int_enh)

    # mri features
    mri_feat = get_finding_param(mri, mri_findings, 1).finding
    mri_feat_p = get_finding_param(mri, mri_findings, 1).params

    mri_feat_prob = get_val_prob(mri_feat, mri_feat_p[0], condition)
    p_mri_feat = get_population(mri_feat_prob)

    # kinetic curve assessment

    mri_kin_c = get_finding_param(mri, mri_findings, 2).finding
    mri_kin_c_p = get_finding_param(mri, mri_findings, 2).params

    mri_kin_c_prob = get_val_prob(mri_kin_c, mri_kin_c_p[0], condition)

    p_mri_kin_c = get_population(mri_kin_c_prob)

    #nme (2)

    mri_nme = get_finding_param(mri, mri_findings, 3).finding
    mri_nme_p = get_finding_param(mri, mri_findings, 3).params

    mri_nme_d_prob = get_val_prob(mri_nme, mri_nme_p[0], condition)
    mri_nme_iep_prob = get_val_prob(mri_nme, mri_nme_p[1], condition)

    p_mri_nme_d = get_population(mri_nme_d_prob)
    p_mri_nme_iep =  get_population(mri_nme_iep_prob)

    #nef

    mri_nef = get_finding_param(mri, mri_findings, 4).finding
    mri_nef_p = get_finding_param(mri, mri_findings, 4).params

    mri_nef_prob = get_val_prob(mri_nef, mri_nef_p[0], condition)
    p_mri_nef = get_population(mri_nef_prob)


    #lnodes

    mri_ln = get_finding_param(mri, mri_findings, 5).finding
    mri_ln_p = get_finding_param(mri, mri_findings, 5).params

    mri_ln_prob = get_val_prob(mri_ln, mri_ln_p[0], condition)
    p_mri_ln = get_population(mri_ln_prob)

    #fcl

    mri_fcl = get_finding_param(mri, mri_findings, 6).finding
    mri_fcl_p = get_finding_param(mri, mri_findings, 6).params

    mri_fcl_prob = get_val_prob(mri_fcl, mri_fcl_p[0], condition)
    p_fcl = get_population(mri_fcl_prob)
    
    mass_arr = [*p_mass_shape, *p_mass_margin, *p_mass_int_enh]
    nme_arr = [*p_mri_nme_d,*p_mri_nme_iep ]

    populations = [mass_arr, [p_mri_feat],
                   [p_mri_kin_c], [p_mri_nme_d,p_mri_nme_iep ], [p_mri_nef],
                   [p_mri_ln],[p_fcl] ]

    condition_data = ConditionData(mass = mri_m_p, mrif = mri_feat_p,
                                   kca = mri_kin_c_p, nme = mri_nme_p,
                                   nef = mri_nef_p, lnodes = mri_ln_p,
                                   fcl = mri_fcl_p,
                                   marr = mass_arr, mrifarr = p_mri_feat,
                                   kcaarr = p_mri_kin_c, nmearr = nme_arr,
                                   nefarr= p_mri_nef, lnarr = p_mri_ln,
                                   fclarr = p_fcl)


    return condition_data

