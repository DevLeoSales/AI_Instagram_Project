
# Import for integration with BotCity Maestro SDK
from botcity.maestro import *
import requests
import os
from dotenv import load_dotenv
import math
from instagrapi import Client

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

# Modelos a serem utilizados
MODEL_TEXT = "gpt-4o"
MODEL_IMAGE = "dall-e-3"
MODEL_EMBEDDING = "text-embedding-3-small"  # Para comparação semântica

# Diretório de saída
OUTPUT_DIR = r"C:\dev\Treinamento_BotCity\projeto-leonardo-sales\teste_retorno_api"
HISTORICO_FILE = r"C:\dev\Treinamento_BotCity\projeto-leonardo-sales\historico.txt"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Chave de API da OpenAI
load_dotenv(r"C:\dev\Treinamento_BotCity\projeto-leonardo-sales\.env")
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("Defina a variável de ambiente OPENAI_API_KEY com sua chave da OpenAI.")


def main():
    
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    # maestro = BotMaestroSDK.from_sys_args()
    # ## Fetch the BotExecution with details from the task, including parameters
    # execution = maestro.get_execution()

    # print(f"Task ID is: {execution.task_id}")
    # print(f"Task Parameters are: {execution.parameters}")

    # ===== Funções auxiliares =====

    def verifica_similaridade_texto(texto1, texto2):
        """Calcula similaridade de cosseno entre dois vetores."""
        dot = sum(a * b for a, b in zip(texto1, texto2))
        norm1 = math.sqrt(sum(a * a for a in texto1))
        norm2 = math.sqrt(sum(b * b for b in texto2))
        return dot / (norm1 * norm2)
    
    def gerar_embedding(texto):
        """Gera embedding para um texto usando API OpenAI."""
        url = "https://api.openai.com/v1/embeddings"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        data = {
            "model": MODEL_EMBEDDING,
            "input": texto
        }
        r = requests.post(url, headers=headers, json=data)
        r.raise_for_status()
        return r.json()["data"][0]["embedding"]

    def carregar_historico():
        """Carrega histórico como lista de curiosidades e embeddings."""
        if os.path.exists(HISTORICO_FILE):
            with open(HISTORICO_FILE, "r", encoding="utf-8") as f:
                curiosidades = [l.strip() for l in f.readlines()]
            embeddings = [gerar_embedding(c) for c in curiosidades]
            return curiosidades, embeddings
        return [], []

    def salvar_no_historico(curiosidade):
        """Salva curiosidade no histórico."""
        with open(HISTORICO_FILE, "a", encoding="utf-8") as f:
            f.write(curiosidade.strip() + "\n")

    # ===== Funções de API =====

    def obter_curiosidade_unica():
        """Obtém curiosidade inédita comparando semanticamente com histórico."""
        historico, embeddings_hist = carregar_historico()
        tentativas = 0

        while True:
            tentativas += 1
            curiosidade = obter_curiosidade().strip()
            emb_curiosidade = gerar_embedding(curiosidade)

            similar = False
            for emb_hist in embeddings_hist:
                if verifica_similaridade_texto(emb_curiosidade, emb_hist) > 0.5:
                    similar = True
                    break

            if not similar:
                salvar_no_historico(curiosidade)
                return curiosidade

            if tentativas > 10:
                raise RuntimeError("Não foi possível encontrar uma curiosidade inédita após várias tentativas.")

    def obter_curiosidade():
        """Obtenha uma curiosidade aleatória, de conhecimentos gerais, que será utilizada para gerar um texto e uma imagem, que serão posteriormente utilizados para postar no Instagram."""
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        data = {
            "model": MODEL_TEXT,
            "messages": [{"role": "user", "content": "Me diga uma curiosidade aleatória, de conhecimentos gerais, que será utilizada para gerar um texto e uma imagem, que serão posteriormente utilizados para postar no Instagram. A curiosidade deve ser apresentada em uma frase curta, de poucas palvras, apenas em uma linha."}],
            "max_tokens": 50
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    def gerar_texto_legenda(curiosidade):
        """Gera o texto explicativo estilo legenda de Instagram."""
        prompt = f"Escreva um texto, em inglês, explicativo sobre a curiosidade '{curiosidade}', detalhando-a de forma envolvente e fácil de entender, com tom informativo e levemente descontraído, como se fosse uma legenda de Instagram. Finalize o texto com hashtags relevantes para o tema e para aumentar o alcance. Inclua a hashtag #FunFacts no final do texto. Remova do texto qualquer tipo de interação com o prompt"
        
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        data = {
            "model": MODEL_TEXT,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def gerar_imagem(curiosidade):
        """Gera a imagem com base na curiosidade."""
        # prompt = f"Gere uma arte visual quadrada (formato 1080x1080), com fundo realista e harmônico, contendo apenas a curiosidade '{curiosidade}' escrita de forma clara e chamativa, em português, sem título genérico como 'Curiosidades Gerais'."
        prompt = f"Gere uma arte visual quadrada (formato 1080x1080), realista e harmônica sobre a curiosidade '{curiosidade}' sem ABSOLUTAMENTE NADA escrito, ou seja, não deve haver nenhum tipo de texto na imagem. Faça uma imagem que seja amigável e atraente, o menos assustadora possível, que possa ser usada como uma postagem de Instagram."

        
        url = "https://api.openai.com/v1/images/generations"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        data = {
            "model": MODEL_IMAGE,
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024"
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        image_url = response.json()["data"][0]["url"]

        # Baixar a imagem
        img_data = requests.get(image_url).content
        return img_data

    def postar_instagram(username: str, password: str, image_path: str, caption: str):
        cl = Client()
        cl.login(username, password)
        cl.photo_upload(image_path, caption)
        print("Post feito com sucesso!")

    # ===== Bot =====

    def action():
        print("Obtendo curiosidade inédita...")
        curiosidade = obter_curiosidade_unica()
        print(f"Curiosidade: {curiosidade}")

        print("Gerando texto...")
        legenda = gerar_texto_legenda(curiosidade)
        caminho_txt = os.path.join(OUTPUT_DIR, f"{curiosidade[:40].replace(' ', '_')}.txt")
        with open(caminho_txt, "w", encoding="utf-8") as f:
            f.write(legenda)
        print(f"Legenda salva em {caminho_txt}")

        print("Gerando imagem...")
        img = gerar_imagem(curiosidade)
        caminho_img = os.path.join(OUTPUT_DIR, f"{curiosidade[:40].replace(' ', '_')}.jpeg")
        with open(caminho_img, "wb") as f:
            f.write(img)
        print(f"Imagem salva em {caminho_img}")

        print("Postando no Instagram...")
        username = os.getenv("INSTAGRAM_USERNAME")
        password = os.getenv("INSTAGRAM_PASSWORD")
        if not username or not password:
            raise ValueError("Defina as variáveis de ambiente INSTAGRAM_USERNAME e INSTAGRAM_PASSWORD com suas credenciais do Instagram.")
        postar_instagram(username, password, caminho_img, legenda)
        print("Postagem concluída com sucesso!")
    
    return action()

if __name__ == '__main__':
    main()
