# 🗓️ Gerenciador de Eventos

![Preview](https://github.com/user-attachments/assets/21df6081-e8eb-486f-b3c4-a0c5ba3447c0)

Sistema completo de gerenciamento de eventos com CRUD, filtros avançados e visualização em calendário. Desenvolvido com Python + Flask + SQLite + Tailwind CSS.

---

## 🚀 Tecnologias

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-CDN-06B6D4?style=flat&logo=tailwindcss&logoColor=white)

---

## ✨ Funcionalidades

- **CRUD Completo** – Criar, listar, visualizar, editar e excluir eventos
- **Categorias** – Conferência, Workshop, Meetup, Webinar, Social, Esportivo, Cultural, Outro (cada uma com cor visual)
- **Status** – Planejado, Confirmado, Em Andamento, Concluído, Cancelado
- **Filtros Avançados** – Por categoria, status, intervalo de datas e busca por texto
- **Calendário Mensal** – Visualize eventos no calendário, navegue entre meses, clique para ver detalhes
- **Dashboard** – Estatísticas, próximos eventos, eventos por categoria e por status
- **API JSON** – Endpoint `/api/events` com suporte a filtros via query params
- **Design Dark Theme** – Interface moderna e responsiva com Tailwind CSS via CDN

---

## 📦 Como Rodar Localmente

### Pré-requisitos

- Python 3.10 ou superior

### 1. Clone o repositório

```bash
git clone https://github.com/Beto2024/08-Gerenciador-de-Eventos.git
cd 08-Gerenciador-de-Eventos
```

### 2. (Opcional) Crie um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Inicie a aplicação

```bash
python app.py
```

O banco de dados SQLite será criado e populado automaticamente com 15 eventos de exemplo na primeira execução.

Acesse: **http://localhost:5000**

---

## 📁 Estrutura do Projeto

```
08-Gerenciador-de-Eventos/
├── app.py                    # Aplicação Flask principal (rotas)
├── config.py                 # Configurações (DB, categorias, status)
├── requirements.txt          # Dependências Python
├── README.md
├── .gitignore
├── database/
│   └── init_db.py            # Criação do schema e seed de dados
├── models/
│   └── event.py              # Operações com SQLite (CRUD + queries)
├── static/
│   ├── css/
│   │   └── custom.css        # Estilos customizados (dark theme)
│   └── js/
│       ├── calendar.js       # Lógica do calendário
│       ├── filters.js        # Lógica dos filtros dinâmicos
│       └── main.js           # Scripts principais
└── templates/
    ├── base.html             # Template base com Tailwind CSS (CDN)
    ├── 404.html              # Página de erro 404
    ├── index.html            # Dashboard principal
    ├── events/
    │   ├── list.html         # Lista com filtros e paginação
    │   ├── create.html       # Formulário de criação
    │   ├── edit.html         # Formulário de edição
    │   └── detail.html       # Detalhes do evento
    ├── calendar/
    │   └── view.html         # Visualização em calendário
    └── components/
        ├── navbar.html       # Barra de navegação
        ├── event_card.html   # Card de evento reutilizável
        └── filters.html      # Componente de filtros
```

---

## 🛣️ Rotas da Aplicação

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Dashboard principal |
| GET | `/events` | Lista de eventos (com filtros e paginação) |
| GET | `/events/create` | Formulário de criação |
| POST | `/events/create` | Criar evento |
| GET | `/events/<id>` | Detalhes do evento |
| GET | `/events/<id>/edit` | Formulário de edição |
| POST | `/events/<id>/edit` | Atualizar evento |
| POST | `/events/<id>/delete` | Excluir evento |
| GET | `/calendar` | Redireciona para o mês atual |
| GET | `/calendar/<year>/<month>` | Calendário de mês específico |
| GET | `/api/events` | API JSON com filtros via query params |

### Parâmetros da API (`/api/events`)

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `category` | string | Filtrar por categoria (slug) |
| `status` | string | Filtrar por status (slug) |
| `start_from` | date | Data de início mínima (YYYY-MM-DD) |
| `start_to` | date | Data de início máxima (YYYY-MM-DD) |
| `search` | string | Busca em título e descrição |
| `page` | int | Número da página (padrão: 1) |

---

## 🗄️ Banco de Dados

```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE,
    start_time TIME,
    end_time TIME,
    location TEXT,
    category TEXT NOT NULL DEFAULT 'outro',
    status TEXT NOT NULL DEFAULT 'planejado',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 📄 Licença

Este projeto está sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.