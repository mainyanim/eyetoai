from mongoengine import *
from mongoengine.context_managers import switch_db

connect(db = 'eyetoai',
        host='mongodb://yuri:rxLPDCJPXWHOozeV@cluster0-shard-00-00-lnxfa.mongodb.net:27017,cluster0-shard-00-01-lnxfa.mongodb.net:27017,cluster0-shard-00-02-lnxfa.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')

class ICD(EmbeddedDocument):
    name = DynamicField()

class Value(EmbeddedDocument):
    name = StringField()
    prob = IntField()


class Parameter(EmbeddedDocument):
    name = StringField()
    p_values = ListField(EmbeddedDocumentField(Value))

class Finding(EmbeddedDocument):
    name = StringField()
    parameters = ListField(EmbeddedDocumentField(Parameter))

class Condition(Document):
    name = StringField()
    findings = ListField(EmbeddedDocumentField(Finding))
    code = EmbeddedDocumentField(ICD)


def define_fibroadenoma():
    #Mass
    i = ICD(name = 'D24')
    v1 = Value(name='Oval', prob=1)
    v2 = Value(name='Round', prob=0)
    v3 = Value(name='Irregular', prob=0)

    v2_1 = Value(name='Circumscribed', prob=0)
    v2_2 = Value(name='Obscured', prob=0)
    v2_3 = Value(name='Microlobulated', prob=1)
    v2_4 = Value(name='Indistinct', prob=0)
    v2_5 = Value(name='Spiculated', prob=0)

    v3_1 = Value(name='High density', prob=1)
    v3_2 = Value(name='Equal density', prob=0)
    v3_3 = Value(name='Low density', prob=0)
    v3_4 = Value(name='Fat-containing', prob=0)

    shape = [v1, v2, v3]
    margin = [v2_1, v2_2, v2_3, v2_4, v2_5]
    density = [v3_1, v3_2, v3_3, v3_4]

    #Calcifications

    v_1 = Value(name = 'Coarse or “popcorn-like', prob = 1)
    v_2 = Value(name = 'Skin', prob = 0)
    v_3 = Value(name = 'Vascular', prob = 0)
    v_4 = Value(name = 'Large rod-like', prob = 0)
    v_5 = Value(name = 'Round', prob = 0)
    v_6 = Value(name = 'Rim', prob = 0)
    v_7 = Value(name = 'Dystrophic', prob = 0)
    v_8 = Value(name = 'Milk of calcium', prob = 0)
    v_9 = Value(name = 'Suture', prob = 0)

    v_2_1 = Value(name = 'Amorphous', prob = 0)
    v_2_2 = Value(name = 'Coarse heterogeneous', prob = 1)
    v_2_3 = Value(name = 'Fine pleomorphic', prob = 0)
    v_2_4 = Value(name = 'Fine linear or fine-linear branching', prob = 0)

    v_3_1 = Value(name = 'Diffuse', prob = 0)
    v_3_2 = Value(name = 'Regional', prob = 1)
    v_3_3 = Value(name = 'Grouped', prob = 0)
    v_3_4 = Value(name = 'Linear', prob = 0)
    v_3_5 = Value(name = 'Segmental', prob = 0)
    typically_benign = [v_1, v_2, v_3, v_4, v_5, v_6, v_7, v_8, v_9]
    suspicious_morphology = [v_2_1, v_2_2, v_2_3, v_2_3]
    distribition = [v_3_1, v_3_2, v_3_3, v_3_3, v_3_4, v_3_5]

    #Assymetry

    v_4_1 = Value(name = 'Asymmetry', prob = 0)
    v_4_2 = Value(name = 'Global asymmetry', prob = 1)
    v_4_3 = Value(name = 'Focal asymmetry', prob = 0)
    v_4_5 = Value(name = 'Developing asymmetry', prob = 0)
    assymetry = [v_4_1, v_4_2, v_4_3, v_4_5]

    #Lymph nodes


    v_5_1 = Value(name = 'Lymph nodes – intramammary', prob = 1)
    v_5_2 = Value(name = 'Lymph nodes – axillary', prob = 0)
    lymph_nodes = [v_5_1, v_5_2]

    #mass_params
    shape_par = Parameter(name = 'Shape', p_values = shape)
    margin_par = Parameter(name = 'Margin', p_values = margin)
    density_par = Parameter(name = 'Density', p_values = density)
    mass_params = [shape_par, margin_par, density_par]

    #calc params
    typ_b_par = Parameter(name = 'Typically benign”', p_values = typically_benign)
    susp_morph_par = Parameter(name = 'Suspicious morphology', p_values = suspicious_morphology)
    distribition_par = Parameter(name = 'Distribution', p_values = distribition)
    calc_params = [typ_b_par, susp_morph_par, distribition_par]

    #assym params
    assym_par = Parameter(name = 'Assymetry', p_values = assymetry)

    #lymph_nodes
    lymph_nodes_par = Parameter(name = 'Lymph nodes', p_values = lymph_nodes)

    f1 = Finding(name = 'Mass',  parameters = mass_params )
    f2 = Finding(name = 'Calcifications', parameters = calc_params)
    f3 = Finding(name = 'Assymetry', parameters = [assym_par])
    f = Condition(name = 'Fibroadenoma', findings = [f1, f2, f3,], code = i)
    f.save()
    return f

if __name__ == '__main__':
    define_fibroadenoma()