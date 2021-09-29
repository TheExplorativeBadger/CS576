from application_driver.helper_modules import stringMethods

def lacI_bound(lactose, lacI):
    return (lacI and not lactose)

def CAP_bound(glucose, CAP):
    return (CAP and not glucose)

def lacZ(is_lacI_bound, is_CAP_bound):
    if (is_lacI_bound and is_CAP_bound):
        return "absent"
    elif (is_lacI_bound and not is_CAP_bound):
        return "absent"
    elif (not is_lacI_bound and is_CAP_bound):
        return "high"
    else:
        return "low"
    return "low"

def lacZ_full_circuit(lactose, lacI, glucose, CAP):
    return lacZ(lacI_bound(lactose, lacI), CAP_bound(glucose, CAP))

def read_lacZ_full_circuit_inputs(filename):
    lines = []
    with open(filename) as f:
        lines = f.readlines()
    
    listOfTupules = []
    for line in lines:
        curLineStringPieces = line.split()
        curLineBooleanPieces = []
        for curLine in curLineStringPieces:
            curLineBooleanPieces.append(stringMethods.str_to_bool(curLine))
        listOfTupules.append(curLineBooleanPieces)
        
    return listOfTupules

def call_lacZ_full_circuit_on_list(inputs_list):
    lacZStatusList = []
    for line in inputs_list:
        lacZStatusList.append(lacZ_full_circuit(*line))  
    return lacZStatusList