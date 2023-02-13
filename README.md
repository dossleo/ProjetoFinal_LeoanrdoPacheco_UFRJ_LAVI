# Projeto Final de Graduação - Leonardo Pacheco - UFRJ - LAVI

Database Utilizada: https://www02.smt.ufrj.br/~offshore/mfs/page_01.html

Para executar todo o código, siga os seguintes passos:

1 - Clonar o Repositório GitHub

    É aconselhável utilizar o editor de texto Visual Studio Code para rodar os códigos localmente

2 - Instale o Python 3 em sua máquina

2 - Criar um ambiente virtual

    Utilizando o VS Code, pressione ctrl + J para abrir o terminal

    Em seguida, digite o seguinte comando:

```
python3 -m venv .venv
```

3 - Instale as bibliotecas contidas no arquivo requirements.txt

    Para isto, basta executar

```
pip install -r requirements.txt
```

4 - Baixe a base de dados MAFAULDA

    Baixe e descompacte os arquivos da base de dados numa pasta chamada database/dados_brutos

5 - Configure o arquivo models/__init__.py

    Dentro do arquivo init.py, configure as seguintes variáveis:

    path_dados_brutos -> local onde estão localizados os arquivos da base MAFAULDA

    path_dados_tratados -> local onde quer salvar os dados que serão tratados.

    É necessária a criação da pasta antes da execução do código.

6 - Utilize o arquivo gerar_dados_tratados.py para tratar os dados brutos

    Configure qual o número de harmônicos que deseja utilizar para tratar os dados

7 - Utilize o arquivo rodar_machine_learning.py para executar o algoritmo de aprendizado de máquina


Caso possua alguma dúvida quanto ao algoritmo, entre em contato via e-mail com leonardo.pacheco@poli.ufrj.br
