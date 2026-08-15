# Ink Studio - Sistema de Gerenciamento para Tatuadores

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

Um sistema completo, premium e responsivo desenvolvido em **Python (Django)** para automatizar a vida de um tatuador solo. O projeto atua tanto como um portfólio público elegante para clientes, quanto como um painel de administração poderoso para controle financeiro e de agendamentos.

## 🚀 Principais Funcionalidades

### 1. Portfólio Público (Visão do Cliente)
- **Galeria Interativa**: Exibição dos trabalhos com filtros CSS (animação suave em cascata) e lightbox para visualização em tela cheia.
- **Formulário de Agendamento**: Interface limpa para captura de leads, permitindo ao cliente solicitar horários com envio de imagem de referência.
- **Design Premium**: Estética *"Dark Glassmorphism"* usando cores de alto contraste (Preto e Dourado) e tipografia moderna (*Outfit* e *Playfair Display*).

### 2. Painel de Controle (Visão do Tatuador)
- **Gestão de Agendamentos**: Visualização de horários pendentes e confirmados.
- **Termo de Consentimento Automático em PDF**: Botão nativo para geração (via impressão `HTML/@media print`) de um termo pré-preenchido com os dados da tatuagem, pronto para assinatura física do cliente no estúdio.
- **Automação de WhatsApp (Click-to-Chat)**: Ao confirmar um agendamento, o sistema gera dinamicamente um link do WhatsApp com mensagem pré-preenchida (incluindo o nome do cliente, data e horário) e abre automaticamente para envio.
- **Resumo Financeiro (Dashboard)**:
  - Integração com **Chart.js** para gráficos interativos.
  - Gráfico de Linha demonstrando a evolução do faturamento.
  - Gráfico de Pizza (Donut) evidenciando as formas de pagamento (Pix, Cartão, Dinheiro).
  - Filtro dinâmico e inteligente por período: *Hoje*, *Últimos 7 dias*, *Este Mês* e *Este Ano*.
- **Gestão de Conteúdo**:
  - Adição e remoção de novas tatuagens no portfólio.
  - Atualização da biografia e adição de diplomas/certificações (com modal de recorte de imagem).

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python, Django, PostgreSQL
- **Frontend**: HTML5, Vanilla CSS (Variáveis, Flexbox, CSS Grid), Vanilla Javascript
- **Bibliotecas**: Chart.js (Gráficos), Cropper.js (Edição de imagens)

## ⚙️ Como Executar o Projeto

### 🐳 Opção 1: Usando Docker (Recomendado para Avaliação/Portfólio)
Esta opção sobe a aplicação inteira e um banco de dados **PostgreSQL** oficial sem precisar instalar nada além do Docker.

1. Certifique-se de ter o **Docker Desktop** instalado e aberto.
2. Abra o terminal na pasta raiz e rode o comando:
   ```bash
   docker compose up --build -d
   ```
3. Acesse `http://127.0.0.1:8000/`.
4. *Nota:* Um superusuário será gerado automaticamente para acessar o painel (`Usuário: kaua | Senha: 12345678`).

### 💻 Opção 2: Localmente (Sem Docker - Modo Raiz)
Certifique-se de ter o [Python](https://www.python.org/) instalado em sua máquina.

1. Clone o repositório ou baixe a pasta do projeto.
2. Abra o terminal na pasta raiz do projeto (onde está o arquivo `manage.py`).
3. Crie um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   ```
4. Ative o ambiente virtual:
   - **Windows**: `venv\Scripts\activate`
   - **Linux/Mac**: `source venv/bin/activate`
5. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```
   *(Nota: O arquivo requirements.txt já inclui o Django, PostgreSQL adapter e bibliotecas de imagem).*
6. Aplique as migrações do banco de dados:
   ```bash
   python manage.py migrate
   ```
7. Crie um superusuário para acessar o painel de administração:
   ```bash
   python manage.py createsuperuser
   ```
8. Inicie o servidor local:
   ```bash
   python manage.py runserver
   ```
9. Acesse no seu navegador:
   - Site Principal: `http://127.0.0.1:8000/`
   - Painel do Tatuador: Acesse a página principal e clique em "Acesso Restrito" no menu superior (ou acesse via `/dashboard/`).

## 💡 Estrutura de Navegação do Painel (Abas)

Para manter a fluidez de uma aplicação moderna, o painel de controle funciona no formato "Single Page Application" (SPA) usando JavaScript para alternar as abas. O estado da aba ativa é preservado usando a memória temporária do navegador (`sessionStorage`), garantindo que formulários e filtros não quebrem o fluxo do usuário ao recarregar a página.
