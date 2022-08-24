import re

def validate_cnpj(cnpj):
    padrao = re.compile(r"(^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$)")
    resp = re.match(padrao, cnpj)
    if not resp:
        return False
    return True

def validate_cpf(cpf):
    padrao = re.compile(r"^([0-9]{3}[.]?[0-9]{3}[.]?[0-9]{3}[-]?[0-9]{2})$")
    resp = re.match(padrao, cpf)
    if not resp:
        return False
    return True

#def validate_telefone(telefone):


#def validate_cep(cep):


print(validate_cnpj('21.176.914/0001-88'))