import re

def get_f_params_val(modality, cond, user_input):
    return {
        "$and": [
            {"modality": re.compile(modality, re.IGNORECASE)},
            {"conditions": {
                "$elemMatch": {
                    "conditionName": re.compile(cond, re.IGNORECASE) ,
                    "findings": {
                        "$elemMatch": {
                            "name": re.compile(user_input["name"], re.IGNORECASE),
                            "$and": [
                                {
                                    "parameters": {
                                        "$elemMatch": {
                                            "name": re.compile(query_tuple[0], re.IGNORECASE),
                                            "value": re.compile(query_tuple[1], re.IGNORECASE)
                                        }
                                    }
                                }
                            for query_tuple in user_input["parameters"]]
                        }
                    }
                }
            }}
        ]
    }


def get_value(modality, finding, parameter):
    return [
        {
            "$match": {"modality": re.compile(modality, re.IGNORECASE)}
        },
        {
            "$unwind": "$conditions"
        },
        {
            "$unwind": "$conditions.findings"
        },
        {
            "$match": {"conditions.findings.name": re.compile(finding, re.IGNORECASE)}
        },
        {
            "$unwind": "$conditions.findings.parameters"
        },
        {
            "$match": {"conditions.findings.parameters.name": re.compile(parameter, re.IGNORECASE)}
        },
        {
            "$group": {"_id": "null", "uniqueValues": {"$addToSet": "$conditions.findings.parameters.value"}}
        }
    ]


def get_parameter_names(modality, finding):
    return [
        {
            "$match": {"modality": re.compile(modality, re.IGNORECASE)}
        },
        {
            "$unwind": "$conditions"
        },
        {
            "$unwind": "$conditions.findings"
        },
        {
            "$match": {"conditions.findings.name": re.compile(finding, re.IGNORECASE)}
        },
        {
            "$unwind": "$conditions.findings.parameters"
        },
        {
            "$match": {"conditions.findings.parameters.value": {"$exists": "true"}}
        },
        {
            "$group": {"_id": "null", "uniqueValues": {"$addToSet": "$conditions.findings.parameters.name"}}
        }
    ]
