# API de Autenticação usando Flask

## 1. Configuração

Instalar o [Python 3.9.9](https://www.python.org/downloads/release/python-399/), o [Postgresql](https://www.postgresql.org) e um SGDB (recomendo o [Dbeaver](https://dbeaver.io/download/))

![Credenciais Postgresql](https://i.imgur.com/GqyHk9K.png)

Altear os seguintes campos para as credênciais do seu banco:

1 - Nome do usuário

2 - Senha

3 - Nome do banco

O localhost é considerando caso você esteja rodando o banco na sua máquina local.

Executar o script para ativar o ambiente virtual:
```console
pip install pipenv
pipenv shell
pipenv install
```

Criar o banco e as tabelas no postgres, para isso execute o seguinte comando:
```console
python
```

Após isso digite:
```console
from app import db
db.create_all()
```

Esse comando procura as configurações do banco no seu arquivo py e cia as tabelas automáticamente, confira então se a tabela está correta em seu SGDB.

Para iniciar a API execute (windows/ubuntu):
```console
python app.py
python3 app.py
```
## 2. Endpoints

Registrar um usuário:

![Post usuario](https://i.imgur.com/UKGJ52x.png)

Autenticar credênciais do usuário:

![Post autenticacao usuario](https://i.imgur.com/4LESYHB.png)

Autenticar JWToken:

![Autenticaao token](https://i.imgur.com/mcVybex.png)


