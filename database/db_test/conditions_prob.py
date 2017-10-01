import pymongo


class Condition:
    def __init__(self, no_of_findings, findings=[]):
        self.n = no_of_findings
        self.findings = ['Mass', 'Calcifications', 'Assymetry', 'Lymph nodes']

    def inputFinding(self):
        self.findings = [(input("Enter finding " + str(i + 1) + " : ")) for i in range(self.n)]

    def show_f_list(self):
        findings_list = [self.findings[x] for x in range(self.n)]
        print(findings_list)

    def dispFinding(self):
        for i in range(self.n):
            print("Finding", i + 1, "is", self.findings[i])


class Fibroadenoma(Condition):
    def __init__(self):
        Condition.__init__(self, 4)

    def showFindings(self):
        self.findings = ['Mass', 'Calcification', 'Assymetrty', 'Lymph nodes']
        return self.findings

    def set_parameters(self, params_mass, params_calc, params_assym, params_l_nodes):
        self.parameters_mass = params_mass
        self.parameters_calc = params_calc
        self.parameters_assym = params_assym
        self.parameters_l_nodes = params_l_nodes
        return self.parameters_mass, self.parameters_calc, self.parameters_assym, self.parameters_l_nodes

    def set_mass(self, shape_val, margin_val, density_val):
        self.shape_val = shape_val
        self.margin_val = margin_val
        self.density_val = density_val
        shape_dict = {self.parameters_mass[0]: shape_val}
        margin_dict = {self.parameters_mass[1]: margin_val}
        density_dict = {self.parameters_mass[2]: density_val}
        print(shape_dict, margin_dict, density_dict)
        return shape_dict, margin_dict, density_dict

    def set_calc(self, benign_val, susp_morp_val):
        self.benign_val = benign_val
        self.susp_morp_val = susp_morp_val
        benign_dict = {self.parameters_calc[0]: benign_val}
        susp_morp_dict = {self.parameters_calc[1]: susp_morp_val}
        print(benign_dict, susp_morp_dict)
        return benign_dict, susp_morp_dict


a = Fibroadenoma()
a.set_parameters(['Shape', 'Margin', 'Density'],
                 ['Typically benign', 'Suspicious morphology', 'Distribution'],
                 ['Assymetry'], ['Lymph nodes'])
a.set_mass(['Oval', 'Round', 'Irregular'], ['Circumscribed', 'Obscured', 'Microlobulated', 'Indistinct', 'Spiculated'],
           ['High density', 'Equal density', 'Low density', 'Fat-containing'])
a.set_calc(['Coarse or “popcorn-like”', 'Skin', 'Vascular',
            'Large rod-like', 'Round', 'Rim', 'Dystrophic', 'Milk of calcium', 'Suture'],
           ['Amorphous', 'Coarse heterogeneous', 'Fine pleomorphic', 'Fine linear or fine-linear branching'])

