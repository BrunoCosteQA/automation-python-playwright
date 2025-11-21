import unicodedata
from dataclasses import dataclass
from util.faker_data import fake


def sanitizar(texto: str) -> str:
    """Remove acentos, troca espaços por ponto e deixa apenas caracteres válidos."""
    # Remove acentos
    nfkd = unicodedata.normalize("NFKD", texto)
    texto = "".join([c for c in nfkd if not unicodedata.combining(c)])

    # Troca espaços por ponto
    texto = texto.replace(" ", ".")

    # Mantém apenas caracteres permitidos
    permitido = "abcdefghijklmnopqrstuvwxyz0123456789."
    texto = "".join([c.lower() for c in texto.lower() if c in permitido])

    return texto


def limitar_tamanho_username(username: str, max_length: int = 30) -> str:
    """Garante que o username tenha no máximo 30 caracteres."""
    return username[:max_length]


@dataclass
class UserData:
    nome: str
    sobrenome: str
    email: str
    senha: str
    dia: str
    mes: str
    ano: str
    genero: str


class UserBuilder:
    """Builder para criação de dados de usuário utilizando Faker."""

    @staticmethod
    def build(genero: str = "Homem") -> UserData:
        nome = fake.first_name_male() if genero == "Homem" else fake.first_name_female()
        sobrenome = fake.last_name()

        # Sanitiza nome e sobrenome
        nome_sanit = sanitizar(nome)
        sobrenome_sanit = sanitizar(sobrenome)

        # Cria username base
        username_base = f"{nome_sanit}.{sobrenome_sanit}.{fake.random_int(1000,9999)}"

        # Limita username para no máximo 30 caracteres
        username_final = limitar_tamanho_username(username_base)

        dia = str(fake.random_int(min=1, max=28))
        mes = fake.month_name().capitalize()
        ano = str(fake.random_int(min=1980, max=2004))

        senha = fake.password(
            length=12,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True
        )

        return UserData(
            nome=nome,
            sobrenome=sobrenome,
            email=username_final,
            senha=senha,
            dia=dia,
            mes=mes,
            ano=ano,
            genero=genero
        )
