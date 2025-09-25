# 🐾 Sistema de Agendamento Petshop

Este projeto é um sistema de agendamento de banhos para um pet shop.  
Ele permite que clientes agendem horários, e que os gerentes consultem e administrem os agendamentos.  
Também expõe uma **API REST** para integração com outros sistemas.

---

## 🚀 Funcionalidades

- Cadastro de **categorias de animais** (ex.: Cachorro, Gato, Coelho).
- Agendamento de banho com:
  - Data
  - Categoria do animal
  - Nome e telefone do cliente
  - Nome do pet (opcional)
- Limite de agendamentos por dia (capacidade diária).
- Painel de gerenciamento para listar agendamentos por data.
- API REST com:
  - Criação de reservas (`POST /api/bookings`)
  - Listagem de reservas (`GET /api/bookings?date=YYYY-MM-DD`)
  - Relatório de banhos do mês anterior por categoria (`GET /api/categories/{id}/previous-month-bookings`)
  - Atualização de status da reserva (`PATCH /api/bookings/{id}`)

---

## 📂 Estrutura do Projeto

Ultima.School/
└── petshop/
    ├── app/
    │   ├── __init__.py        # inicializa o Flask e o banco
    │   ├── models.py          # tabelas e funções de criação do schema
    │   ├── routes.py          # rotas da API (endpoints Flask)
    │   ├── services.py        # regras de negócio (capacidade, validações)
    │   ├── templates/         # páginas HTML (se tiver interface web)
    │   └── static/            # CSS, JS, imagens
    ├── migrations/            # scripts SQL de criação/alteração de tabelas
    │   └── 001_init.sql
    ├── tests/                 # testes automatizados
    ├── petshop.db             # banco SQLite (gerado depois) (Criado na raiz do Projeto)
    ├── requirements.txt       # dependências (Flask, etc.)
    ├── README.md
    └── run.py                 # ponto de entrada da aplicação


---

## ⚙️ Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/Rogerio5/petshop.git
   cd petshop
