from faker import Faker

fake = Faker("pt_BR")  # Gera dados realistas em português do Brasil

def gerar_nome():
    return fake.first_name()

def gerar_sobrenome():
    return fake.last_name()

def gerar_full_name():
    return fake.name()

def gerar_data_nascimento():
    data = fake.date_of_birth(minimum_age=18, maximum_age=65)
    return data.day, data.strftime("%B"), data.year

def gerar_email(prefix="email"):
    return f"{prefix}.{fake.random_number(digits=5)}".lower()

def gerar_senha():
    return fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
