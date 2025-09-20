import os
try:
    import keyring
except ImportError:
    keyring = None

# Função para obter o token do GitHub
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
        token = keyring.get_password("github", "token")
        if token:
            return token

    raise EnvironmentError(
        "Nenhum token do GitHub encontrado. "
        "Defina a variável de ambiente GITHUB_TOKEN ou configure no keyring."
    )