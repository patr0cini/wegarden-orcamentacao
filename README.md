# We Garden · Orçamentação Online

Ferramenta de orçamentação automática para paisagismo, disponível em:
**[wegarden-orcamentacao.onrender.com](https://wegarden-orcamentacao.onrender.com)**

---

## Funcionalidades

### Mapa de quantidades (ficheiro do cliente)
- Carrega qualquer formato de Excel de mapa de quantidades (LQPU, Budget, MQT, SP, etc.)
- Lista todos os artigos com descrição, unidade e quantidade
- Motor de busca automático com 49.500 artigos da tabela de preços integrada
- Pesquisa manual por palavras-chave
- **Preços compostos** — selecciona sub-artigos e o total é calculado para o artigo pai
- Pré-visualização do Excel no browser (todas as folhas)
- Exportar Excel com formatação 100% preservada
- Upload directo para pasta do SharePoint

### Criar novo orçamento (a partir do modelo We Garden)
- Editor com capítulos, sub-capítulos e artigos
- Nome da obra editável
- Motor de busca de preços integrado
- Totais automáticos por capítulo e geral
- Exportar Excel com formatação do template We Garden

### Guardar e histórico
- Autosave automático — guarda no browser a cada 3 segundos
- Base de dados no servidor — acesso de qualquer computador
- Painel **📋 Orçamentos** com todos os orçamentos guardados
- Abrir, duplicar ou eliminar orçamentos
- Nome de utilizador para saber quem criou cada orçamento

---

## Publicar / actualizar no Render

### Primeira vez
1. Cria um repositório no [GitHub](https://github.com) e faz upload de todos os ficheiros
2. Vai a [render.com](https://render.com) → **New +** → **Web Service** → liga ao repositório
3. O Render detecta o `render.yaml` e configura automaticamente
4. Clica **Deploy**

### Actualizar
Sempre que alterares ficheiros no GitHub, o Render faz redeploy automaticamente.

---

## Variáveis de ambiente (Render → Environment)

| Variável | Descrição |
|---|---|
| `APP_PASSWORD` | Password de acesso à ferramenta |
| `SECRET_KEY` | Chave secreta das sessões (gerada automaticamente) |
| `AZURE_CLIENT_ID` | ID da app Azure para SharePoint |
| `AZURE_TENANT_ID` | ID do tenant Azure |
| `AZURE_CLIENT_SECRET` | Segredo da app Azure |
| `APP_BASE_URL` | URL público da aplicação |
| `DATABASE_URL` | URL da base de dados PostgreSQL (opcional — ver nota abaixo) |

> **Nota sobre a base de dados:** Sem `DATABASE_URL`, a aplicação usa SQLite local e os orçamentos apagam-se quando o Render reinicia o serviço (plano gratuito reinicia após inactividade). Para persistência permanente, adiciona uma base de dados PostgreSQL gratuita no Render: **New → PostgreSQL** → copia o *Internal Database URL* → define como `DATABASE_URL` nas variáveis de ambiente.

---

## Configuração SharePoint (Azure AD)

1. [portal.azure.com](https://portal.azure.com) → **Microsoft Entra ID** → **App registrations** → **New registration**
2. Nome: `WeGarden Orçamentação` · Tipo: *Single tenant*
3. Redirect URI: `Web` → `https://wegarden-orcamentacao.onrender.com/auth/callback`
4. **API permissions** → Microsoft Graph → Delegated → `Sites.ReadWrite.All` → Grant admin consent
5. **Certificates & secrets** → New client secret → copia o valor para `AZURE_CLIENT_SECRET`

---

## Estrutura do projecto

```
wegarden-app/
├── app.py              # Backend Python (Flask + SQLAlchemy)
├── requirements.txt    # Dependências Python
├── render.yaml         # Configuração Render
├── README.md           # Este ficheiro
└── static/
    └── index.html      # Frontend completo (HTML + CSS + JS + base de dados de preços)
```

---

## Correr localmente

```bash
pip install -r requirements.txt
python app.py
```

Abre `http://localhost:5000` — password padrão: `wegarden2026`

---

*We Garden · [www.wegarden.pt](https://www.wegarden.pt)*
