
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
MODEL_EMBEDDING = "text-embedding-3-small"  # Para comparação de frases

# Diretório de saída
OUTPUT_DIR = r"path_to_save_files\ ".strip()
HISTORICO_FILE = r"path_to_save_file_with_curiosities_already_posted.txt"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Chave de API da OpenAI
load_dotenv(r"path_to_your_project\.env")
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("Defina a variável de ambiente OPENAI_API_KEY com sua chave da OpenAI.")


def main():
    
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    maestro = BotMaestroSDK.from_sys_args()
    # ## Fetch the BotExecution with details from the task, including parameters
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    # Chave de API da OpenAI
    # API_KEY = maestro.get_credential(label="instagram_credentials", key="api_key")
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
        try:
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
        except Exception as e:
            print(f"Erro ao obter curiosidade inédita: {e}")
            raise

    def obter_curiosidade():
        try:
            """Obtenha uma curiosidade aleatória, de conhecimentos gerais, que será utilizada para gerar um texto e uma imagem, que serão posteriormente utilizados para postar no Instagram."""
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}"
            }
            data = {
                "model": MODEL_TEXT,
                "messages": [{"role": "user", "content": "Me diga uma curiosidade aleatória, de conhecimentos gerais, que será utilizada para gerar um texto e uma imagem, que serão posteriormente utilizados para postar no Instagram. A curiosidade deve ser apresentada em uma frase curta, de poucas palvras, apenas em uma linha. A curiosidade não precisa ser apenas sobre animais, pode ser sobre qualquer assunto, como geografia, história, ciência, tecnologia, cultura, entre outros."}],
                "max_tokens": 50
            }
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"Erro ao obter curiosidade: {e}")
            raise

    def gerar_texto_legenda(curiosidade):
        try:
            """Gera o texto explicativo estilo legenda de Instagram."""
            prompt = f"Escreva um texto, em inglês, explicativo sobre a curiosidade '{curiosidade}', detalhando-a de forma envolvente e fácil de entender, com tom informativo e levemente descontraído, como se fosse uma legenda de Instagram. Finalize o texto com hashtags relevantes para o tema e para aumentar o alcance. Inclua a hashtag #FunFacts no final do texto. Remova do texto qualquer tipo de interação com o prompt. Não esqueça de levar em consideração que esse texto deve ser gerado em inglês."
            
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
        except Exception as e:
            print(f"Erro ao gerar texto da legenda: {e}")
            raise

    def gerar_imagem(curiosidade):
        try:
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
        except Exception as e:
            print(f"Erro ao gerar imagem: {e}")
            raise

    def postar_instagram(username: str, password: str, image_path: str, caption: str):
        try:
            cl = Client()
            cl.login(username, password)
            cl.photo_upload(image_path, caption)
        except Exception as e:
            print(f"Erro ao postar no Instagram: {e}")
            raise

    # ===== Bot =====

    def action():
        print("Obtendo curiosidade inédita...")
        # maestro.alert(
        #     task_id=execution.task_id,
        #     title="Info Alert",
        #     message="Obtendo curiosidade inédita...",
        #     alert_type=AlertType.INFO
        # )
        curiosidade = obter_curiosidade_unica()
        print(f"Curiosidade: {curiosidade}")
        # maestro.alert(
        #     task_id=execution.task_id,
        #     title="Info Alert",
        #     message=f"Curiosidade: {curiosidade}",
        #     alert_type=AlertType.INFO
        # )

        print("Gerando texto...")
        # maestro.alert(
        #     task_id=execution.task_id,
        #     title="Info Alert",
        #     message="Gerando texto...",
        #     alert_type=AlertType.INFO
        # )
        legenda = gerar_texto_legenda(curiosidade)
        caminho_txt = os.path.join(OUTPUT_DIR, f"{curiosidade[:40].replace(' ', '_')}.txt")
        # caminho_txt = f"{curiosidade[:40].replace(' ', '_')}.txt"
        with open(caminho_txt, "w", encoding="utf-8") as f:
            f.write(legenda)
        # maestro.post_artifact(
        #     task_id=execution.task_id,
        #     artifact_name=f"legenda_curiosidade_{curiosidade}",
        #     filepath=caminho_txt
        # )
        # print(f"Legenda salva em {caminho_txt}")

        print("Gerando imagem...")
        # maestro.alert(
        #     task_id=execution.task_id,
        #     title="Info Alert",
        #     message="Gerando imagem...",
        #     alert_type=AlertType.INFO
        # )
        img = gerar_imagem(curiosidade)
        caminho_img = os.path.join(OUTPUT_DIR, f"{curiosidade[:40].replace(' ', '_')}.jpeg")
        # caminho_img = f"{curiosidade[:40].replace(' ', '_')}.jpeg"
        print(f"Caminho da imagem: {caminho_img}")
        with open(caminho_img, "wb") as f:
            f.write(img)
        # maestro.post_artifact(
        #     task_id=execution.task_id,
        #     artifact_name=f"imagem_curiosidade_{curiosidade}",
        #     filepath=caminho_img
        # )
        # print(f"Imagem salva em {caminho_img}")

        print("Postando no Instagram...")
        # maestro.alert(
        #     task_id=execution.task_id,
        #     title="Info Alert",
        #     message="Postando no Instagram...",
        #     alert_type=AlertType.INFO
        # )
        username = os.getenv("INSTAGRAM_USERNAME")
        password = os.getenv("INSTAGRAM_PASSWORD")
        # username = maestro.get_credential(label="instagram_credentials", key="username")
        # password = maestro.get_credential(label="instagram_credentials", key="password")
        if not username or not password:
            raise ValueError("Defina as variáveis de ambiente INSTAGRAM_USERNAME e INSTAGRAM_PASSWORD com suas credenciais do Instagram.")
        postar_instagram(username, password, caminho_img, legenda)
        print("Postagem concluída com sucesso!")
        # maestro.alert(
        #     task_id=execution.task_id,
        #     title="Info Alert",
        #     message=f"Postagem da curiosidade {curiosidade} concluída com sucesso!",
        #     alert_type=AlertType.INFO
        # )

        # maestro.finish_task(
        #     task_id=execution.task_id,
        #     status=AutomationTaskFinishStatus.SUCCESS,
        #     message="Task Finished with SUCCESS."
        # )
    
    return action()

if __name__ == '__main__':
    main()
