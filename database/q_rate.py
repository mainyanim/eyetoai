from entropy import *

findings = db.reportsNew.distinct("conditions.findings.name",
                                        {"modality": "Mammography"})

