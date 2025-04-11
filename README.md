# Projeto Diagnóstico

O objetivo do Sistema de Diagnóstico é fornecer uma análise da empresa, permitindo que ela identifique áreas de melhoria e oportunidades de desenvolvimento através dos cursos oferecidos em parceria com o Hub de Inovação Fronteira da UEM. 

O sistema visa facilitar o processo de coleta de dados e geração de relatórios a fim de apoiar a tomada de decisão estratégica.

## Tecnologias Utilizadas
- Python
- Django
- Django REST Framework
- MySQL

## Funcionalidades
- API RESTful para gerenciamento de usuários, questionários e respostas.
- Autenticação JWT personalizada.
- Suporte a múltiplos tipos de questionários.
- Geração de relatórios empresariais.

## Como Executar o Projeto

### Pré-requisitos
- Python (3.12.3)
- MySQL

### Passos
1. Clone o repositório:
   ```bash
   git clone https://github.com/Yoshifg/projeto_diagnostico_api.git
   ```
   
2. Navegue até o diretório do projeto:
   ```bash
   cd projeto_diagnostico_api
   ```
   
3. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
   
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
5. Configure o banco de dados no arquivo .env.local e aplique as migrações:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. Inicie o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```

