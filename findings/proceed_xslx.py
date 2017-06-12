from openpyxl import load_workbook
from openpyxl import Workbook

INPUT_FILE = 'google_form_pure.xlsx'
OUTPUT_FILE = 'output.xlsx'


class GetParams:
    """Return names of params (margin, shape, etc)"""
    def __init__(self, row):
        self.row = [str(cell.value).replace('\n', '').strip() for cell in row]

        # BiRad params

        self.mass_shape = self.get_params(10, 13)
        self.lymph_nodes = self.get_params(44, 46)

        # Mammography params
        self.mammo_mass_margin = self.get_params(13, 18)
        self.mammo_mass_density = self.get_params(18, 22)
        self.mammo_calcifications_typically_benign = self.get_params(22, 31)
        self.mammo_calcifications_suspicious_morphology = self.get_params(31, 35)
        self.mammo_calcifications_suspicious_distribution = self.get_params(35, 40)
        self.mammo_asymmetries = self.get_params(40, 44)

        # US params
        self.us_mass_margin = self.get_params(57, 63)
        self.us_mass_echo_pattern = self.get_params(63, 69)
        self.us_mass_posterior_features = self.get_params(69, 73)
        self.us_calcifications = self.get_params(73, 76)
        self.us_special_cases = self.get_params(88, 97)

        # MRI params
        self.mri_mass_margin = self.get_params(102, 106)
        self.mri_mass_internal_enhacement = self.get_params(106, 110)
        self.mri_features = self.get_params(110, 113)
        self.mri_kinetic_curve_assessment = self.get_params(113, 119)
        self.mri_nme_distribution = self.get_params(120, 126)
        # Non-mass enhancement (NME) - Internal enhancement patterns
        self.mri_nme_iep = self.get_params(126, 130)
        # Non-enhancing findings
        self.mri_nef = self.get_params(130, 137)
        # Fat containing lesions
        self.mri_fcl = self.get_params(139, 144)

    def get_params(self, start, stop):
        return [x.split('[')[1][:-1] for x in self.row[start:stop]]


class SetParams:
    """Create list of params for output file"""
    def __init__(self, params_name, row):
        self.row = row

        # Mammography params
        self.mammo_params = {
            'Mass': {
                'Shape': {
                    'Typical': self.return_params(10, 13, 't',
                                                  params_name.mass_shape),
                    'Possible': self.return_params(10, 13, 'p',
                                                   params_name.mass_shape),
                    'Atypical': self.return_params(10, 13, 'a',
                                                   params_name.mass_shape),
                    'Pathogenomonic': self.return_params(10, 13, 'pat',
                                                         params_name.mass_shape),
                    'Unrelated': self.return_params(10, 13, 'u',
                                                    params_name.mass_shape),
                    'Negative': self.return_params(10, 13, 'n',
                                                   params_name.mass_shape),
                    'Ignore': self.return_params(10, 13, 'i',
                                                 params_name.mass_shape),
                },
                'Margin': {
                    'Typical': self.return_params(13, 18, 't',
                                                  params_name.mammo_mass_margin),
                    'Possible': self.return_params(13, 18, 'p',
                                                   params_name.mammo_mass_margin),
                    'Atypical': self.return_params(13, 18, 'a',
                                                   params_name.mammo_mass_margin),
                    'Pathogenomonic': self.return_params(13, 18, 'pat',
                                                         params_name.mammo_mass_margin),
                    'Unrelated': self.return_params(13, 18, 'u',
                                                    params_name.mammo_mass_margin),
                    'Negative': self.return_params(13, 18, 'n',
                                                   params_name.mammo_mass_margin),
                    'Ignore': self.return_params(13, 18, 'i',
                                                 params_name.mammo_mass_margin),
                },
                'Density': {
                    'Typical': self.return_params(18, 22, 't',
                                                  params_name.mammo_calcifications_typically_benign),
                    'Possible': self.return_params(18, 22, 'p',
                                                   params_name.mammo_calcifications_typically_benign),
                    'Atypical': self.return_params(18, 22, 'a',
                                                   params_name.mammo_calcifications_typically_benign),
                    'Pathogenomonic': self.return_params(18, 22, 'pat',
                                                         params_name.mammo_calcifications_typically_benign),
                    'Unrelated': self.return_params(18, 22, 'u',
                                                    params_name.mammo_calcifications_typically_benign),
                    'Negative': self.return_params(18, 22, 'n',
                                                   params_name.mammo_calcifications_typically_benign),
                    'Ignore': self.return_params(18, 22, 'i',
                                                 params_name.mammo_calcifications_typically_benign),
                }
            },
            'Calcifications': {
                'Typically benign': {
                    'Typical': self.return_params(22, 31, 't',
                                                  params_name.mammo_calcifications_typically_benign),
                    'Possible': self.return_params(22, 31, 'p',
                                                   params_name.mammo_calcifications_typically_benign),
                    'Atypical': self.return_params(22, 31, 'a',
                                                   params_name.mammo_calcifications_typically_benign),
                    'Pathogenomonic': self.return_params(22, 31, 'pat',
                                                         params_name.mammo_calcifications_typically_benign),
                    'Unrelated': self.return_params(22, 31, 'u',
                                                    params_name.mammo_calcifications_typically_benign),
                    'Negative': self.return_params(22, 31, 'n',
                                                   params_name.mammo_calcifications_typically_benign),
                    'Ignore': self.return_params(22, 31, 'i',
                                                 params_name.mammo_calcifications_typically_benign),
                },
                'Suspicious morphology': {
                    'Typical': self.return_params(31, 35, 't',
                                                  params_name.mammo_calcifications_suspicious_morphology),
                    'Possible': self.return_params(31, 35, 'p',
                                                   params_name.mammo_calcifications_suspicious_morphology),
                    'Atypical': self.return_params(31, 35, 'a',
                                                   params_name.mammo_calcifications_suspicious_morphology),
                    'Pathogenomonic': self.return_params(31, 35, 'pat',
                                                         params_name.mammo_calcifications_suspicious_morphology),
                    'Unrelated': self.return_params(31, 35, 'u',
                                                    params_name.mammo_calcifications_suspicious_morphology),
                    'Negative': self.return_params(31, 35, 'n',
                                                   params_name.mammo_calcifications_suspicious_morphology),
                    'Ignore': self.return_params(31, 35, 'i',
                                                 params_name.mammo_calcifications_suspicious_morphology),
                },
                'Distribution': {
                    'Typical': self.return_params(35, 40, 't',
                                                  params_name.mammo_calcifications_suspicious_distribution),
                    'Possible': self.return_params(35, 40, 'p',
                                                   params_name.mammo_calcifications_suspicious_distribution),
                    'Atypical': self.return_params(35, 40, 'a',
                                                   params_name.mammo_calcifications_suspicious_distribution),
                    'Pathogenomonic': self.return_params(35, 40, 'pat',
                                                         params_name.mammo_calcifications_suspicious_distribution),
                    'Unrelated': self.return_params(35, 40, 'u',
                                                    params_name.mammo_calcifications_suspicious_distribution),
                    'Negative': self.return_params(35, 40, 'n',
                                                   params_name.mammo_calcifications_suspicious_distribution),
                    'Ignore': self.return_params(35, 40, 'i',
                                                 params_name.mammo_calcifications_suspicious_distribution),
                }
            },
            'Assymetry': {
                'Assymetry': {
                    'Typical': self.return_params(40, 44, 't',
                                                  params_name.mammo_asymmetries),
                    'Possible': self.return_params(40, 44, 'p',
                                                   params_name.mammo_asymmetries),
                    'Atypical': self.return_params(40, 44, 'a',
                                                   params_name.mammo_asymmetries),
                    'Pathogenomonic': self.return_params(40, 44, 'pat',
                                                         params_name.mammo_asymmetries),
                    'Unrelated': self.return_params(40, 44, 'u',
                                                    params_name.mammo_asymmetries),
                    'Negative': self.return_params(40, 44, 'n',
                                                   params_name.mammo_asymmetries),
                    'Ignore': self.return_params(40, 44, 'i',
                                                 params_name.mammo_asymmetries),
                }
            },
            'Lymph nodes': {
                'Lymph nodes': {
                    'Typical': self.return_params(44, 46, 't',
                                                  params_name.lymph_nodes),
                    'Possible': self.return_params(44, 46, 'p',
                                                   params_name.lymph_nodes),
                    'Atypical': self.return_params(44, 46, 'a',
                                                   params_name.lymph_nodes),
                    'Pathogenomonic': self.return_params(44, 46, 'pat',
                                                         params_name.lymph_nodes),
                    'Unrelated': self.return_params(44, 46, 'u',
                                                    params_name.lymph_nodes),
                    'Negative': self.return_params(44, 46, 'n',
                                                   params_name.lymph_nodes),
                    'Ignore': self.return_params(44, 46, 'i',
                                                 params_name.lymph_nodes),
                }
            },
        }

        # US params
        self.us_params = {
            'Mass': {
                'Shape': {
                    'Typical': self.return_params(54, 57, 't',
                                                  params_name.mass_shape),
                    'Possible': self.return_params(54, 57, 'p',
                                                   params_name.mass_shape),
                    'Atypical': self.return_params(54, 57, 'a',
                                                   params_name.mass_shape),
                    'Pathogenomonic': self.return_params(54, 57, 'pat',
                                                         params_name.mass_shape),
                    'Unrelated': self.return_params(54, 57, 'u',
                                                    params_name.mass_shape),
                    'Negative': self.return_params(54, 57, 'n',
                                                   params_name.mass_shape),
                    'Ignore': self.return_params(54, 57, 'i',
                                                 params_name.mass_shape),
                },
                'Margin': {
                    'Typical': self.return_params(57, 63, 't',
                                                  params_name.us_mass_margin),
                    'Possible': self.return_params(57, 63, 'p',
                                                   params_name.us_mass_margin),
                    'Atypical': self.return_params(57, 63, 'a',
                                                   params_name.us_mass_margin),
                    'Pathogenomonic': self.return_params(57, 63, 'pat',
                                                         params_name.us_mass_margin),
                    'Unrelated': self.return_params(57, 63, 'u',
                                                    params_name.us_mass_margin),
                    'Negative': self.return_params(57, 63, 'n',
                                                   params_name.us_mass_margin),
                    'Ignore': self.return_params(57, 63, 'i',
                                                 params_name.us_mass_margin),
                },
                'Echo': {
                    'Typical': self.return_params(63, 69, 't',
                                                  params_name.us_mass_echo_pattern),
                    'Possible': self.return_params(63, 69, 'p',
                                                   params_name.us_mass_echo_pattern),
                    'Atypical': self.return_params(63, 69, 'a',
                                                   params_name.us_mass_echo_pattern),
                    'Pathogenomonic': self.return_params(63, 69, 'pat',
                                                         params_name.us_mass_echo_pattern),
                    'Unrelated': self.return_params(63, 69, 'u',
                                                    params_name.us_mass_echo_pattern),
                    'Negative': self.return_params(63, 69, 'n',
                                                   params_name.us_mass_echo_pattern),
                    'Ignore': self.return_params(63, 69, 'i',
                                                 params_name.us_mass_echo_pattern),
                },
                'Posterior': {
                    'Typical': self.return_params(69, 73, 't',
                                                  params_name.us_mass_posterior_features),
                    'Possible': self.return_params(69, 73, 'p',
                                                   params_name.us_mass_posterior_features),
                    'Atypical': self.return_params(69, 73, 'a',
                                                   params_name.us_mass_posterior_features),
                    'Pathogenomonic': self.return_params(69, 73, 'pat',
                                                         params_name.us_mass_posterior_features),
                    'Unrelated': self.return_params(69, 73, 'u',
                                                    params_name.us_mass_posterior_features),
                    'Negative': self.return_params(69, 73, 'n',
                                                   params_name.us_mass_posterior_features),
                    'Ignore': self.return_params(69, 73, 'i',
                                                 params_name.us_mass_posterior_features),
                }
            },
            'Calcifications US': {
                'Calcifications US': {
                    'Typical': self.return_params(73, 76, 't',
                                                  params_name.us_calcifications),
                    'Possible': self.return_params(73, 76, 'p',
                                                   params_name.us_calcifications),
                    'Atypical': self.return_params(73, 76, 'a',
                                                   params_name.us_calcifications),
                    'Pathogenomonic': self.return_params(73, 76, 'pat',
                                                         params_name.us_calcifications),
                    'Unrelated': self.return_params(73, 76, 'u',
                                                    params_name.us_calcifications),
                    'Negative': self.return_params(73, 76, 'n',
                                                   params_name.us_calcifications),
                    'Ignore': self.return_params(73, 76, 'i',
                                                 params_name.us_calcifications),
                }
            },
            'Lymph nodes': {
                'Lymph nodes': {
                    'Typical': self.return_params(76, 78, 't',
                                                  params_name.lymph_nodes),
                    'Possible': self.return_params(76, 78, 'p',
                                                   params_name.lymph_nodes),
                    'Atypical': self.return_params(76, 78, 'a',
                                                   params_name.lymph_nodes),
                    'Pathogenomonic': self.return_params(76, 78, 'pat',
                                                         params_name.lymph_nodes),
                    'Unrelated': self.return_params(76, 78, 'u',
                                                    params_name.lymph_nodes),
                    'Negative': self.return_params(76, 78, 'n',
                                                   params_name.lymph_nodes),
                    'Ignore': self.return_params(76, 78, 'i',
                                                 params_name.lymph_nodes),
                }
            },
            'Special cases': {
                'Special cases': {
                    'Typical': self.return_params(88, 97, 't',
                                                  params_name.us_special_cases),
                    'Possible': self.return_params(88, 97, 'p',
                                                   params_name.us_special_cases),
                    'Atypical': self.return_params(88, 97, 'a',
                                                   params_name.us_special_cases),
                    'Pathogenomonic': self.return_params(88, 97, 'pat',
                                                         params_name.us_special_cases),
                    'Unrelated': self.return_params(88, 97, 'u',
                                                    params_name.us_special_cases),
                    'Negative': self.return_params(88, 97, 'n',
                                                   params_name.us_special_cases),
                    'Ignore': self.return_params(88, 97, 'i',
                                                 params_name.us_special_cases),
                }
            }
        }

        # MRI params
        self.mri_params = {
            'Mass': {
                'Shape': {
                    'Typical': self.return_params(99, 102, 't',
                                                  params_name.mass_shape),
                    'Possible': self.return_params(99, 102, 'p',
                                                   params_name.mass_shape),
                    'Atypical': self.return_params(99, 102, 'a',
                                                   params_name.mass_shape),
                    'Pathogenomonic': self.return_params(99, 102, 'pat',
                                                         params_name.mass_shape),
                    'Unrelated': self.return_params(99, 102, 'u',
                                                    params_name.mass_shape),
                    'Negative': self.return_params(99, 102, 'n',
                                                   params_name.mass_shape),
                    'Ignore': self.return_params(99, 102, 'i',
                                                 params_name.mass_shape),
                },
                'Margin': {
                    'Typical': self.return_params(102, 106, 't',
                                                  params_name.mri_mass_margin),
                    'Possible': self.return_params(102, 106, 'p',
                                                   params_name.mri_mass_margin),
                    'Atypical': self.return_params(102, 106, 'a',
                                                   params_name.mri_mass_margin),
                    'Pathogenomonic': self.return_params(102, 106, 'pat',
                                                         params_name.mri_mass_margin),
                    'Unrelated': self.return_params(102, 106, 'u',
                                                    params_name.mri_mass_margin),
                    'Negative': self.return_params(102, 106, 'n',
                                                   params_name.mri_mass_margin),
                    'Ignore': self.return_params(102, 106, 'i',
                                                 params_name.mri_mass_margin),
                },
                'Internal enhacement': {
                    'Typical': self.return_params(106, 110, 't',
                                                  params_name.mri_mass_internal_enhacement),
                    'Possible': self.return_params(106, 110, 'p',
                                                   params_name.mri_mass_internal_enhacement),
                    'Atypical': self.return_params(106, 110, 'a',
                                                   params_name.mri_mass_internal_enhacement),
                    'Pathogenomonic': self.return_params(106, 110, 'pat',
                                                         params_name.mri_mass_internal_enhacement),
                    'Unrelated': self.return_params(106, 110, 'u',
                                                    params_name.mri_mass_internal_enhacement),
                    'Negative': self.return_params(106, 110, 'n',
                                                   params_name.mri_mass_internal_enhacement),
                    'Ignore': self.return_params(106, 110, 'i',
                                                 params_name.mri_mass_internal_enhacement),
                }
            },
            'MRI features': {
                'MRI features': {
                    'Typical': self.return_params(110, 113, 't',
                                                  params_name.mri_features),
                    'Possible': self.return_params(110, 113, 'p',
                                                   params_name.mri_features),
                    'Atypical': self.return_params(110, 113, 'a',
                                                   params_name.mri_features),
                    'Pathogenomonic': self.return_params(110, 113, 'pat',
                                                         params_name.mri_features),
                    'Unrelated': self.return_params(110, 113, 'u',
                                                    params_name.mri_features),
                    'Negative': self.return_params(110, 113, 'n',
                                                   params_name.mri_features),
                    'Ignore': self.return_params(110, 113, 'i',
                                                 params_name.mri_features),
                }
            },
            'Kinetic curve assessment': {
                'Kinetic curve assessment': {
                    'Typical': self.return_params(113, 119, 't',
                                                  params_name.mri_kinetic_curve_assessment),
                    'Possible': self.return_params(113, 119, 'p',
                                                   params_name.mri_kinetic_curve_assessment),
                    'Atypical': self.return_params(113, 119, 'a',
                                                   params_name.mri_kinetic_curve_assessment),
                    'Pathogenomonic': self.return_params(113, 119, 'pat',
                                                         params_name.mri_kinetic_curve_assessment),
                    'Unrelated': self.return_params(113, 119, 'u',
                                                    params_name.mri_kinetic_curve_assessment),
                    'Negative': self.return_params(113, 119, 'n',
                                                   params_name.mri_kinetic_curve_assessment),
                    'Ignore': self.return_params(113, 119, 'i',
                                                 params_name.mri_kinetic_curve_assessment),
                }
            },
            'Non-mass enhancement (NME)': {
                'Distribution': {
                    'Typical': self.return_params(120, 126, 't',
                                                  params_name.mri_nme_distribution),
                    'Possible': self.return_params(120, 126, 'p',
                                                   params_name.mri_nme_distribution),
                    'Atypical': self.return_params(120, 126, 'a',
                                                   params_name.mri_nme_distribution),
                    'Pathogenomonic': self.return_params(120, 126, 'pat',
                                                         params_name.mri_nme_distribution),
                    'Unrelated': self.return_params(120, 126, 'u',
                                                    params_name.mri_nme_distribution),
                    'Negative': self.return_params(120, 126, 'n',
                                                   params_name.mri_nme_distribution),
                    'Ignore': self.return_params(120, 126, 'i',
                                                 params_name.mri_nme_distribution),
                },
                'Internal enhancement patterns': {
                    'Typical': self.return_params(126, 130, 't',
                                                  params_name.mri_nme_iep),
                    'Possible': self.return_params(126, 130, 'p',
                                                   params_name.mri_nme_iep),
                    'Atypical': self.return_params(126, 130, 'a',
                                                   params_name.mri_nme_iep),
                    'Pathogenomonic': self.return_params(126, 130, 'pat',
                                                         params_name.mri_nme_iep),
                    'Unrelated': self.return_params(126, 130, 'u',
                                                    params_name.mri_nme_iep),
                    'Negative': self.return_params(126, 130, 'n',
                                                   params_name.mri_nme_iep),
                    'Ignore': self.return_params(126, 130, 'i',
                                                 params_name.mri_nme_iep),
                }
            },
            'Non-enhancing findings': {
                'Non-enhancing findings': {
                    'Typical': self.return_params(130, 137, 't',
                                                  params_name.mri_nef),
                    'Possible': self.return_params(130, 137, 'p',
                                                   params_name.mri_nef),
                    'Atypical': self.return_params(130, 137, 'a',
                                                   params_name.mri_nef),
                    'Pathogenomonic': self.return_params(130, 137, 'pat',
                                                         params_name.mri_nef),
                    'Unrelated': self.return_params(130, 137, 'u',
                                                    params_name.mri_nef),
                    'Negative': self.return_params(130, 137, 'n',
                                                   params_name.mri_nef),
                    'Ignore': self.return_params(130, 137, 'i',
                                                 params_name.mri_nef),
                }
            },
            'Lymph nodes': {
                'Lymph nodes': {
                    'Typical': self.return_params(137, 139, 't',
                                                  params_name.lymph_nodes),
                    'Possible': self.return_params(137, 139, 'p',
                                                   params_name.lymph_nodes),
                    'Atypical': self.return_params(137, 139, 'a',
                                                   params_name.lymph_nodes),
                    'Pathogenomonic': self.return_params(137, 139, 'pat',
                                                         params_name.lymph_nodes),
                    'Unrelated': self.return_params(137, 139, 'u',
                                                    params_name.lymph_nodes),
                    'Negative': self.return_params(137, 139, 'n',
                                                   params_name.lymph_nodes),
                    'Ignore': self.return_params(137, 139, 'i',
                                                 params_name.lymph_nodes),
                }
            },
            'Fat containing lesions': {
                'Fat containing lesions': {
                    'Typical': self.return_params(139, 144, 't',
                                                  params_name.mri_fcl),
                    'Possible': self.return_params(139, 144, 'p',
                                                   params_name.mri_fcl),
                    'Atypical': self.return_params(139, 144, 'a',
                                                   params_name.mri_fcl),
                    'Pathogenomonic': self.return_params(139, 144, 'pat',
                                                         params_name.mri_fcl),
                    'Unrelated': self.return_params(139, 144, 'u',
                                                    params_name.mri_fcl),
                    'Negative': self.return_params(139, 144, 'n',
                                                   params_name.mri_fcl),
                    'Ignore': self.return_params(139, 144, 'i',
                                                 params_name.mri_fcl),
                }
            },
        }

    def return_params(self, start, stop, params_type, param_name):
        """
        :param params_type: t - typical, p - possible, a - atypical,
         pat - Pathogenomonic, u - Unrelated, n - Negative, i - Ignore
        :return: string
        """
        pt = {
            't': 'Typical', 'p': 'Possible', 'a': 'Atypical',
            'pat': 'Pathogenomonic', 'u': 'Unrelated',
            'n': 'Negative', 'i': 'Ignore'
        }
        string = ', '.join([param_name[count]
                            for count, cell in enumerate(self.row[start:stop])
                            if pt[params_type] in cell])
        return string


def read_file():
    """Return data from input file as dictionary"""
    # Read file
    wb = load_workbook(INPUT_FILE)
    ws = wb.worksheets[0]
    return ws


def ch_none(string):
    if 'None' not in string:
        return True
    else:
        return False


def get_dictionary(file_data):
    """Return data from file as list of dictionaries"""
    data_iter_rows = list(file_data.iter_rows())
    params = GetParams(data_iter_rows[0])
    data_list = []
    for rows in data_iter_rows[1:]:
        row = [str(cell.value).replace('\n', '').strip() for cell in rows]
        rel_modalities = [x.strip() for x in row[4].split(',') if ch_none(x)]
        unique_finding = ', '.join([x for x in row[163:173] if ch_none(x)])
        params_list = SetParams(params, row)
        dict_birad = {'Typical': 50, 'Possible': 30, 'None':1, 'Ignore': 'Ignore'}
        d = {'Name': row[1], 'Condition description': row[2],
             'Relevant modalities': rel_modalities,
             'Unique findings': unique_finding,
             'mammo_params': params_list.mammo_params,
             'us_params': params_list.us_params,
             'mri_params': params_list.mri_params,
             'birad[0]': dict_birad[row[153]],
             'birad[1]': dict_birad[row[154]],
             'birad[2]': dict_birad[row[155]],
             'birad[3]': dict_birad[row[156]],
             'birad[4]': dict_birad[row[157]],
             'birad[5]': dict_birad[row[158]],
             'birad[6]': dict_birad[row[159]],
             'Associated conditions': row[160],
             'Differential diagnosis': row[162],
             }
        data_list.append(d)
    return data_list


def get_row_nr(file_row, param_name):
    """Return dict of params for output file"""
    if param_name == 'mammo_params':
        name = 'Mammography'
    elif param_name == 'us_params':
        name = 'US'
    else:
        name = 'MRI'
    data = []
    for mp_key, mv in file_row[param_name].items():
        for sub_mp_key, _ in file_row[param_name][mp_key].items():
            d1 = {'Relevant findings': mp_key, 'Parameters': sub_mp_key,
                  'Relevant modalities': name}
            for smk, smv in file_row[param_name][mp_key][sub_mp_key].items():
                if smv:
                    d2 = {smk: smv}
                    d1 = {**d1, **d2}
            data.append(d1)
    return data


def get_output_list(file_row):
    """Return list of dict for output file"""
    data = []
    list_mammo = get_row_nr(file_row, 'mammo_params')
    list_us = get_row_nr(file_row, 'us_params')
    list_mri = get_row_nr(file_row, 'mri_params')
    all_params = list_mammo + list_us + list_mri
    for x in range(len(all_params)):
        d = {'Name': '', 'Condition description': '',
             'Unique findings': '','Additional info':'','birad[0]':'','birad[1]':'',
             'birad[2]':'','birad[3]':'','birad[4]':'','birad[5]':'','birad[6]':'', 'Associated conditions': '', 'Differential diagnosis': ''}
        nd = {**d, **all_params[x]}
        if x == 0:
            nd['Name'] = file_row['Name']
            nd['Condition description'] = file_row['Condition description']
            nd['Unique findings'] = file_row['Unique findings']
            nd['birad[0]'] = file_row['birad[0]']
            nd['birad[1]'] = file_row['birad[1]']
            nd['birad[2]'] = file_row['birad[2]']
            nd['birad[3]'] = file_row['birad[3]']
            nd['birad[4]'] = file_row['birad[4]']
            nd['birad[5]'] = file_row['birad[5]']
            nd['birad[6]'] = file_row['birad[6]']
            nd['Associated conditions'] = file_row['Associated conditions']
            nd['Differential diagnosis'] = file_row['Differential diagnosis']
        data.append(nd)
    return data


def save_output(output_list):
    """Save data in output file"""
    wb = Workbook()
    ws1 = wb.active
    ws1.title = 'Sheet1'
    # Create title for columns
    columns_titles = ['Name', 'Condition description', 'birad[0]','birad[1]','birad[2]','birad[3]','birad[4]','birad[5]','birad[6]','Relevant modalities',
                      'Relevant findings', 'Unique findings','Additional info',
                      'Parameters', 50, 30, 1,
                      'Pathogenomonic', 'Unrelated', 'Negative',
                      'Ignore', 'Associated conditions', 'Differential diagnosis', 'Notes']
    ws1.append(columns_titles)
    # Create list for output file
    for ol in output_list:
        for o in ol:
            cr_list = create_list(o)
            ws1.append(cr_list)
    wb.save(filename=OUTPUT_FILE)


def create_list(row):
    """Return list for output file"""
    name = row['Name']
    cd = row['Condition description']
    br0 = row['birad[0]']
    br1 = row['birad[1]']
    br2 = row['birad[2]']
    br3 = row['birad[3]']
    br4 = row['birad[4]']
    br5 = row['birad[5]']
    br6 = row['birad[6]']
    rm = row['Relevant modalities']
    rf = row['Relevant findings']
    uf = row['Unique findings']
    ai = row['Additional info']
    params = row['Parameters']
    try:
        t = row['Typical']
    except:
        t = ''
    try:
        p = row['Possible']
    except:
        p = ''
    try:
        a = row['Atypical']
    except:
        a = ''
    try:
        pat = row['Pathogenomonic']
    except:
        pat = ''
    try:
        u = row['Unrelated']
    except:
        u = ''
    try:
        n = row['Negative']
    except:
        n = ''
    try:
        i = row['Ignore']
    except:
        i = ''
    try:
        notes = row['Notes']
    except:
        notes = ''
    ac = row['Associated conditions']
    dd = row['Differential diagnosis']
    return [name, cd, br0, br1, br2, br3, br4, br5, br6, rm, rf, uf, ai, params, t, p, a, pat, u, n, i, ac, dd, notes]


def main():
    file_data = read_file()
    dictionary_data = get_dictionary(file_data)
    output_list = [get_output_list(x) for x in dictionary_data]
    save_output(output_list)


if __name__ == '__main__':
    main()
