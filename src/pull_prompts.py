"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull do prompt semente do desafio
3. Salva localmente em prompts/bug_to_user_story_v1.yml

DICAS DE IMPLEMENTAÇÃO:

- O pull é feito pelo cliente do LangSmith:

      from langsmith import Client
      client = Client()
      prompt = client.pull_prompt(
          "leonanluppi/bug_to_user_story_v1",
          dangerously_pull_public_prompt=True,
      )

- O parâmetro `dangerously_pull_public_prompt=True` é obrigatório sempre que o
  identificador tem dono explícito ("owner/nome"). O LangSmith bloqueia esse pull
  por padrão porque um prompt do Hub é um objeto LangChain serializado, que pode
  vir de terceiros. Aqui o prompt é o do desafio, então o risco é conhecido.

- O retorno é um ChatPromptTemplate. Para extrair o conteúdo das mensagens,
  use a serialização nativa do LangChain (`prompt.messages`, e o atributo
  `.prompt.template` de cada mensagem).

- Use `save_yaml` de utils.py para gravar o resultado no arquivo .yml.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client
from utils import save_yaml, check_env_vars, print_section_header
import yaml

load_dotenv()

def str_representer(dumper, data):
    if "\n" in data:
        return dumper.represent_scalar(
            "tag:yaml.org,2002:str",
            data.rstrip("\n") + "\n",
            style="|"
        )

    return dumper.represent_scalar(
        "tag:yaml.org,2002:str",
        data
    )

def pull_prompts_from_langsmith():
    client = Client()
    prompt = client.pull_prompt(
        "leonanluppi/bug_to_user_story_v1",
        dangerously_pull_public_prompt=True,
    )

    yaml_data = {
        "bug_to_user_story_v1": {
            "system_prompt": prompt.messages[0].prompt.template + "\n",
            "user_prompt": prompt.messages[1].prompt.template
        }
        }

    yaml.add_representer(str, str_representer)

    save_yaml(
        yaml_data,
        "../prompts/bug_to_user_story_v1_temp.yml"       
    )

    if (not Path("../prompts/bug_to_user_story_v2.yml").exists() or
        input("Deseja substituir o arquivo a ser editado prompts/bug_to_user_story_v2.yml? (s/n): ").lower() == "s"
    ):
        save_yaml(
            yaml_data,
            "../prompts/bug_to_user_story_v2.yml"
        )
        print("Arquivo prompts/bug_to_user_story_v2.yml atualizado com sucesso.")

def main():
    """Função principal"""
    ...


if __name__ == "__main__":
    pull_prompts_from_langsmith()
    sys.exit(main())
