#!/bin/bash

# Adiciona o diretório binário do Python 3 ao PATH
export PATH=$PATH:/usr/local/python3/bin

# Instala o Gunicorn usando pip
pip install gunicorn

# Inicia a aplicação Bottle usando o Gunicorn como servidor web
gunicorn app:app
