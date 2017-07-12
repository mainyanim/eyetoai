import numpy as np

"""
This is an example of how parameters, findings and conditions can be incorporated together
"""
author = 'michael_kolomenkin'

class Parameter:
    """
    The parameters that describe a findings
    """

    def __init__(self, par_type, values=[], name=''):
        # The parameters is a list of values of the same type
        # Values are not passed for int or float types
        self.name = name
        self.par_type = par_type
        if par_type == '3D':
            self.values = np.zeros(3)
        elif par_type == 'int':
            self.values = np.zeros(1, dtype='int')
        elif par_type == 'float':
            self.values = np.zeros(1)
        elif par_type == 'string':
            self.values = values
        else:
            raise 'Exception'


class Finding:
    """
    Findings - description of entities that exist in an image
    """

    def __init__(self, parameters, name=''):
        # List of parameters of type Parameter
        self.parameters = parameters
        self.name = name


class ParameterDistribution:
    """
    The class keeps the probability of each parameter value for each
    """
    def __init__(self):
        self.probabilities = dict()


class ConditionFinding:
    """
    This class describes findings of specific conditions. Opposed to general findings,
    specific findings describe the probability of each parameter to appear for given condition
    """

    """
    TODO: The probabilities described here are only suitable for independent case, i.e.
    Probability(parameter | condition1 & condition2) =
    Probability(parameter | condition1) * Probability(parameter | condition2)
    """

    def __init__(self, finding_list, name):
        # Keep the reference to all findings
        # TODO: probably not the best way, consider moving to a static variable
        self.finding_list = finding_list
        # ID of the appropriate medical finding
        self.find_id = ConditionFinding.set_id_from_list(finding_list, name)
        # list_of_distributions
        # The finding has N parameters. Parameter i has M_i possible values
        # The list is of size N
        self.dict_of_distributions = {}
        name_list = self.get_list_of_parameter_names()
        for name in name_list:
            self.dict_of_distributions[name] = ParameterDistribution
        #
        # [ParameterDistribution] * self.get_number_of_parameters()

    def get_number_of_parameters(self):
        """
        :return: the number of parameter that the finding has
        """
        return len(self.finding_list[self.find_id].parameters)

    def get_list_of_parameter_names(self):
        name_list = [param.name for param in self.finding_list[self.find_id].parameters]
        return name_list

    def get_name(self):
        return self.finding_list[self.find_id].name

    @staticmethod
    def set_id_from_list(finding_list, name):
        # Go over the whole list until find the finding with the same name
        # return -1 if nothing found
        ret = -1
        for cnt, finding in enumerate(finding_list):
            if finding.name == name:
                ret = cnt
                break
        return ret

class Condition:
    """
    This class defines condition
    """
    def __init__(self, finding_list, finding_names_list):
        # TODO: Finding should be dict and not list
        self.findings = list()
        for name in finding_names_list:
            finding = ConditionFinding(finding_list=finding_list, name=name)
            self.findings.append(finding)

    def generate_parameters(self, finding_name):
        """
        Set parameters of a finding according to the predefined probabilities
        :return:
        """
        id = -1
        for ind, finding in enumerate(self.findings):
            if finding.get_name() == finding_name:
                id = ind
                break
        if id == -1:
            return
        # Go over all parameters of this finding
        parameter_names = self.findings[id].get_list_of_parameter_names()
        # TODO: go over all parameter_names
        # dict = {}
        # for param in self.findings[id]
        for name in parameter_names:
            # TODO - currently works only for shape
            if name != 'Shape':
                continue
            # self.findings[id].dict_of_distributions[name]
            # TODO: Decide where to keep it
            chosen_param = np.random.choice(list(self.findings[id].dict_of_distributions[name].keys()),
                             p=list(self.findings[id].dict_of_distributions[name].values()))
            print(chosen_param)



def normalize_prob_dictionary(prob_dict):
    """
    Given a dictionary that describes probabilities of parameter values,
    normalize the probabilities so that they sum up to 1
    :param dict:
    :return:
    """
    sum = np.sum(list(prob_dict.values()))
    if sum > 0:
        for key in prob_dict.keys():
            prob_dict[key] /= sum
    return prob_dict



def define_fibroadenoma(finding_list):
    """
    Define fibroadenoma
    :return:
    """
    # name_list = ['Mass','Calcification','Assymetry','Lymph nodes']
    name_list = ['Mass']
    fibroadenoma = Condition(finding_list=finding_list, finding_names_list=name_list)
    # for mass. Mass has 4 parameters
    # First shape
    # shape has three possible value
    # TODO: fibroadenoma.findings[0] -> fibroadenoma.findings['Mass']
    fibroadenoma.findings[0].dict_of_distributions['Shape'] = {'Round': 50.0, 'Oval': 50.0, 'Irregular': 1.0}
    fibroadenoma.findings[0].dict_of_distributions['Shape'] = \
        normalize_prob_dictionary(fibroadenoma.findings[0].dict_of_distributions['Shape'])
    """
    fibroadenoma.findings[1].dict_of_distributions['Margin'] = {'Circumscribed': 50.0, 'Obscured': 5.0, 'Microlobulated': 5.0, 'Indistinct': 5.0, 'Spiculated': 5.0}
    fibroadenoma.findings[1].dict_of_distributions['Margin'] = \
        normalize_prob_dictionary(fibroadenoma.findings[1].dict_of_distributions['Margin'])
    """
    return fibroadenoma


def define_mass_mammo():
    """

    :return:
     Finding of type mass
    """
    mass_parameters = list()
    mass_parameters.append(Parameter(par_type='int', name='Number'))
    mass_parameters.append(Parameter(par_type='string', name='Density',
                                     values=['High density', 'Equal density', 'Low density', 'Fat-containing']))
    mass_parameters.append(Parameter(par_type='string', name='Shape',
                                     values=['Oval', 'Round', 'Irregular']))
    mass_parameters.append(Parameter(par_type='3D', name='Location'))
    mass_parameters.append(Parameter(par_type='string', name = 'Margin',
                                     values=['Circumscribed', 'Obscured', 'Microlobulated', 'Indistinct', 'Spiculated']))
    mass = Finding(parameters=mass_parameters, name='Mass')

    return mass


def define_calcifications_mammo():
    """

    :return:
     Finfing of type calcification
    """

    calc_parameters = list()
    calc_parameters.append(Parameter(par_type= 'int', name = 'Number'))
    calc_parameters.append(Parameter(par_type='string', name = 'Typically benign',
                                    values = ['Skin', 'Vascular', 'Coarse or “popcorn-like”', 'Large rod-like', 'Round', 'Rim', 'Dystrophic', 'Milk of calcium', 'Suture']))
    calc_parameters.append(Parameter(par_type='string', name = 'Suspicious morphology',
                                     values = ['Amorphous', 'Coarse heterogeneous', 'Fine pleomorphic', 'Fine linear or fine-linear branching']))
    calc_parameters.append(Parameter(par_type='string', name = 'Distribution',
                                    values = ['Diffuse', 'Regional', 'Grouped', 'Linear', 'Segmental']))
    calcifications = Finding(parameters=calc_parameters, name = 'Calcifications')

    return calcifications

def define_assymetry_mammo():
    """

    :return:
    Finding of type assymetry
    """

    assym_parameters = list()
    assym_parameters.append(Parameter(par_type='string',name = 'Assymetries',
                                      values=['Asymmetry', 'Global asymmetry', 'Focal asymmetry', 'Developing asymmetry']))
    assymetry = Finding(parameters=assym_parameters, name = 'Assymetries')

    return assymetry

def define_mass_us():
    mass_parameters = list()
    mass_parameters.append(Parameter(par_type='int', name = 'Number'))
    mass_parameters.append(Parameter(par_type='string', name = 'Orientation',
                                     values=['Parallel', 'Not parallel']))
    mass_parameters.append(Parameter(par_type='string', name = 'Shape',
                                     values = ['Oval', 'Round', 'Irregular']))
    mass_parameters.append(Parameter(par_type='string', name = 'Margin',
                                     values = ['Circumscribed', 'Not circumscribed', 'Indistinct (Not circumscribed)',
                                               'Angular (Not circumscribed)', 'Microlobulated (Not circumscribed)',
                                               'Spiculated (Not circumscribed)']))
    mass_parameters.append(Parameter(par_type='string', name = 'Echo pattern',
                                     values = ['Anechoic', 'Hyperechoic', 'Complex cystic and solid', 'Hypoechoic',
                                               'Isoechoic', 'Heterogeneous']))
    mass_parameters.append(Parameter(par_type='string', name = 'Posterior features',
                                     values=['No posterior features', 'Enhancement', 'Shadowing', 'Combined pattern']))
    mass = Finding(parameters=mass_parameters, name = 'Mass')

    return mass

def define_calcifications_us():
    calc_parameters = list()
    calc_parameters.append(Parameter(par_type='int', name = 'Number'))
    calc_parameters.append(Parameter(par_type='string', name = 'Calcifications US',
                                     values = ['Calcifications in a mass', 'Calcifications outside of a mass',
                                               'Intraductal calcifications']))
    calcifications = Finding(parameters=calc_parameters, name = 'Calcifications')

    return calcifications



def define_findings_set():
    finding_list = list()
    mass = define_mass()
    # density = define_density()
    finding_list.append(mass)
    # finding_list.append(density) - but density is finding's parameter - how to resolve?

    return finding_list


if __name__ == "__main__":
    # Here we will keep all the findings
    finding_list = define_findings_set()
    conditions_list = list()
    # Set medical database
    fibroadenoma = define_fibroadenoma(finding_list)
    conditions_list.append(fibroadenoma)
    # choose parameter
    fibroadenoma.generate_parameters('Mass')




