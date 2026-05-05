# We Garden · Orçamentação Online

## Publicar no Render (gratuito, ~5 minutos)

### 1. GitHub
- Vai a github.com → New repository → nome: `wegarden-orcamentacao`
- Faz upload de todos os ficheiros desta pasta (arrastra a pasta toda para o browser do GitHub)

### 2. Render
- Vai a render.com → cria conta gratuita
- **New +** → **Web Service** → liga ao repositório GitHub
- O Render detecta o `render.yaml` e configura tudo automaticamente
- Clica **Deploy** → em 2-3 minutos tens o link

### 3. Mudar a password
No dashboard do Render → o teu serviço → **Environment**:
- `APP_PASSWORD` → muda para a password que quiseres

### URL final
`https://wegarden-orcamentacao.onrender.com`  
Partilha com a equipa — cada pessoa abre no browser, coloca a password e usa normalmente.

## Como funciona
1. Login com password
2. Carrega o Excel do cliente
3. Clica nos artigos, o motor de busca sugere preços da tabela
4. Clica "Aplicar" nos preços correctos
5. Clica **"⬇ Exportar Excel"** → descarrega o ficheiro original preenchido, com formatação 100% preservada
