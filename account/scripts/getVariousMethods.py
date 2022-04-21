import uuid
def getErrorDict(errors):
    l = []
    for i in errors :
        for j in errors[i] : 
            l.append(j)
    return l

def getUUID() :
    uuid_token = ""
    for i in range(3):
        uuid_token += str(uuid.uuid4())
    return uuid_token.strip()