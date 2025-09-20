import os
try:
    import keyring
except ImportError:
    keyring = None
    
service_name ="GITHUB_TOKEN"
username = "LAB_EXPERIMENTACAO"

def get_github_token():
    """
    Recupera o token do GitHub de forma segura:
    - Primeiro tenta via variável de ambiente GITHUB_TOKEN
    - Depois tenta via keyring (se disponível)
    """
    token = os.getenv("GITHUB_TOKEN")
    if token:
        return token

    if keyring:
        token = keyring.get_password(service_name, username)
        if token:
            return token

    raise EnvironmentError(
        "Nenhum token do GitHub encontrado. "
        "Configure no keyring ou na variável de ambiente 'GITHUB_TOKEN'."
    )