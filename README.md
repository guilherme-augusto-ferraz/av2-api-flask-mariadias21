# API de Biblioteca (Flask)

Este projeto é uma API parar gerenciamento de uma biblioteca pessoal. O sistema permite o cadastro de usuários, autenticação via Token (JWT) e operações completas de CRUD (Criar, Ler, Atualizar, Deletar) para livros.

##  Instalação e Configuração

### 1. Clone ou baixe o repositório

### 2. Crie um ambiente virtual (Opcional, mas recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
````

### 3\. Instale as dependências

As bibliotecas necessárias estão listadas no arquivo `requirements.txt`.

```bash
pip install -r requirements.txt

## Como Rodar

Para iniciar o servidor de desenvolvimento:

```bash
python app.py

O servidor iniciará (por padrão) em: `http://127.0.0.1:5000/`.


## Testes Automatizados

O projeto inclui scripts de teste para verificar o funcionamento das rotas e da lógica de banco de dados.

Para rodar o teste detalhado (com narração passo a passo):

```bash
python testes.py

##  Endpoints da API

Para acessar as rotas protegidas, é necessário enviar o cabeçalho: `Authorization: Bearer <seu_token>`.

### Usuários (`/api/usuarios`)

| Método | Rota | Descrição | Auth |
| :--- | :--- | :--- | :--- |
| `POST` | `/registrar` | Cria um novo usuário (Requer: `nome_usuario`, `email`, `senha`) 
| `POST` | `/login` | Retorna o **Token JWT** (Requer: `nome_usuario`, `senha`) 
| `GET` | `/perfil` | Verifica se o token é válido e retorna mensagem de sucesso 

### Livros (`/api/livros`)

| Método | Rota | Descrição | Auth |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Lista todos os livros do usuário logado 
| `POST` | `/` | Cadastra um novo livro (Requer: `titulo`, `autor`) 
| `GET` | `/<id>` | Detalhes de um livro específico 
| `PUT` | `/<id>` | Atualiza dados de um livro 
| `DELETE`| `/<id>` | Remove um livro do banco de dados 

-----

## Estrutura do Projeto

```text
/
├── app.py                
├── banco_dados.py        
├── configuracao.py       
├── autenticacao.py       
├── requirements.txt      
├── testes.py             
├── models/               
│   ├── usuario.py
│   └── livro.py
└── routes/               
    ├── usuarios.py
    └── livros.py
```

-----

## Exemplo de Requisição (CURL)

**Criar um livro (via terminal):**

```bash
curl POST [http://127.0.0.1:5000/api/livros](http://127.0.0.1:5000/api/livros) \
  -H "Authorization: Bearer <SEU_TOKEN_AQUI>" \
  -H "Content-Type: application/json" \
  -d '{"titulo": "O Senhor dos Anéis", "autor": "Tolkien"}'