import pandas as pd
import sys
from sklearn import preprocessing
import numpy as np
import random

df = pd.read_excel('data.xlsx')
mammo = df.groupby(['Modality']).get_group('Mammography')
mammo_findings = mammo['Finding'].unique()

mammo_mass = mammo.groupby(['Finding']).get_group('Mass')
mammo_mass_parameters = mammo_mass['Parameter'].unique()

mammo_calc = mammo.groupby(['Finding']).get_group('Calcifications')
mammo_calc_parameters = mammo_calc['Parameter'].unique()

def get_val_prob(finding, group, condition):
    mod_find_group = finding.groupby(['Parameter']).get_group(group)
    group_val = mod_find_group['Value'].unique()
    prob = list(mod_find_group[condition])
    return group_val, prob

def get_population(arr):
    population = random.choices(arr[0], weights=arr[1], k=1)
    return population

mammo_mass_shape_prob = get_val_prob(mammo_mass, 'Shape', 'Fibroadenoma')
mammo_mass_margin_prob = get_val_prob(mammo_mass, 'Margin', 'Fibroadenoma')
mammo_mass_density_prob = get_val_prob(mammo_mass, 'Density', 'Fibroadenoma')

population_mass_shape_fibro = get_population(mammo_mass_shape_prob)
