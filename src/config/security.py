from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


def check_password(password: str, hash_password: str) -> bool:
    """
    Função para verificar se a password está correta,
    comparando a password em texto puro, informada pelo
    usuário, e o hash da password que está salvo no bd
    durante a criação da conta.
    """

    return CRIPTO.verify(password, hash_password)


def generate_hash_password(password: str) -> str:

    """
    Função que gera e retorna o hash da password
    """
    return CRIPTO.hash(password)
