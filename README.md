# AI Instagram Automation

Automação em Python (com suporte em PowerShell) para gerar e publicar **posts no Instagram** automaticamente utilizando IA.

##  Estrutura do Projeto

- **`bot.py`**  
  Script principal responsável por orquestrar a geração de conteúdo e a publicação dos posts.

- **Script de deploy**  
  Scripts úteis para configuração automatizada e execução:
  - `build.bat` — para ambientes Windows (batch)
  - `build.ps1` — para PowerShell
  - `build.sh` — para ambientes Unix/Linux (bash)

- **`.vscode/`**  
  Configurações específicas do Visual Studio Code (possivelmente com ajustes de depuração ou ambiente).

- **`requirements.txt`**  
  Lista de dependências Python necessárias para o funcionamento da automação.

- **`resources/`**  
  Diretório reservado para ativos como imagens, templates, prompts ou outros recursos de mídia utilizados pela IA.

- **`historico.txt`**  
  Registro com anotações ou histórico de versões, alterações e observações relevantes.

- **`projeto_leonardo_sales.botproj`**  
  Arquivo de projeto (provavelmente do Visual Studio ou outra IDE), possivelmente para facilidade de edição/depuração durante o desenvolvimento.

- **`.env`**  
  Arquivo de configuração para variáveis de ambiente sensíveis (como tokens ou credenciais).

---

## ​ Requisitos

- Python 3.x  
- Ferramentas de Shell conforme necessário:
  - Windows: suporte a `.bat` ou PowerShell (`.ps1`)
  - Mac/Linux: bash (`.sh`)

- Dependências externas (se especificadas em `requirements.txt`)

---

##  Como Usar

1. Clone este repositório:
    ```bash
    git clone https://github.com/DevLeoSales/AI_Instagram_Project.git
    cd AI_Instagram_Project
    ```

2. Crie e preencha o arquivo `.env` com as variáveis de ambiente necessárias (por exemplo, credenciais da API do Instagram, chaves de IA etc.).

3. Instale as dependências Python:
    ```bash
    pip install -r requirements.txt
    ```

4. Execute o script principal:
    ```bash
    python bot.py
    ```

5. Alternativamente, use os scripts de inicialização:
   - No Windows:
     ```bash
     build.bat
     ```
   - No PowerShell:
     ```powershell
     ./build.ps1
     ```
   - No Linux/Mac:
     ```bash
     ./build.sh
     ```

---

##  Como Funciona (resumo)

- `bot.py` gera conteúdo usando IA (por exemplo, via API do OpenAI ou outra) com base em entradas/autoresets.
- Após gerar o post (imagem e/ou texto), publica automaticamente no Instagram.
- O histórico de posts e resultados pode ser registrado em `historico.txt`.

---

## ​ Personalize conforme:

- **Objetivos do bot**: que tipo de conteúdo ele gera? (legendas, imagens, hashtags, stories?)
- **Fontes de IA**: Qual API de IA está sendo usada? (ex.: OpenAI, DALL·E, Stable Diffusion, etc.)

---

##  Contato

Caso tenha dúvidas ou queira contribuir, entre em contato com **leonardo.t.sales94@gmail.com**.

---

### Exemplo completo em Markdown:

```markdown
# AI Instagram Automation

Automação em Python (com opção de uso via PowerShell ou Shell) para gerar e publicar posts no Instagram automaticamente usando inteligência artificial.

## Estrutura do Projeto

- **`bot.py`** — Script principal de geração e publicação de posts.
- **`build.bat`**, **`build.ps1`**, **`build.sh`** — Scripts de execução em diferentes ambientes.
- **`.vscode/`** — Configurações da IDE.
- **`requirements.txt`** — Dependências Python.
- **`resources/`** — Ativos de mídia, templates, prompts etc.
- **`historico.txt`** — Histórico e anotações de versões.
- **`projeto_leonardo_sales.botproj`** — Arquivo de projeto/IDE.
- **`.env`** — Variáveis sensíveis (API keys, credenciais).

## Requisitos

- Python 3.x
- Ferramentas conforme seu ambiente (Windows, PowerShell, bash)
- Dependências conforme `requirements.txt`

## Como Usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/DevLeoSales/AI_Instagram_Project.git
   cd AI_Instagram_Project
Configure o .env com suas variáveis.

Instale as dependências:

bash
Copy
Edit
pip install -r requirements.txt
Execute:

bash
Copy
Edit
python bot.py
Ou use os scripts:

build.bat

./build.ps1

./build.sh

Descrição do Funcionamento
O bot usa IA para criar conteúdo (texto/imagem).

Publica automaticamente no Instagram.

Registra histórico e logs em historico.txt.

Personalização
Finalidade do conteúdo gerado.

APIs de IA utilizadas.

Contato
Desenvolvido por DevLeoSales
