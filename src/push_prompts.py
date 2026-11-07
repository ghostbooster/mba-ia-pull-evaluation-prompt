"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

DICAS DE IMPLEMENTAÇÃO:

- O push é feito pelo cliente do LangSmith:

      from langsmith import Client
      from langchain_core.prompts import ChatPromptTemplate

      client = Client()
      prompt = ChatPromptTemplate.from_messages([
          ("system", system_prompt),
          ("user", user_prompt),
      ])
      url = client.push_prompt(
          f"{username}/bug_to_user_story_v2",
          object=prompt,
          is_public=True,
          description="...",
          tags=[...],
      )

- `username` vem de USERNAME_LANGSMITH_HUB no .env e precisa ser o seu handle
  do Hub. Se você ainda não tem um handle, veja as instruções no .env.example.

- A variável do template precisa ser {bug_report}, que é a chave de entrada
  usada no dataset de avaliação.

- Use `load_yaml` de utils.py para ler o arquivo .yml.
"""

import os
import sys
from dotenv import load_dotenv
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()


def push_prompt_to_langsmith(prompt_name, description: str, prompt_data) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """   
    client = Client()

    try:
        client.push_prompt(
            prompt_identifier=prompt_name,
            object=prompt,
            description=description,
            is_public=True
        )
        return True
    except Exception as e:
        if "Error while trying to commit" not in str(e):
            raise


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    ...


def main():
    """Função principal"""
    ...


if __name__ == "__main__":
    prompt_file = load_yaml("./prompts/bug_to_user_story_v2.yml")

  #  print(prompt_file)

    if 'bug_to_user_story_v2' in prompt_file:
        messages = [
            ("system", prompt_file['bug_to_user_story_v2']['system_prompt']),
            ("human", prompt_file['bug_to_user_story_v2']['user_prompt'])
        ]

        prompt = ChatPromptTemplate.from_messages(messages)    
    
        success = push_prompt_to_langsmith("bug_to_user_story_v2", "Prompt otimizado para conversão de bug em história de usuário", prompt)

        print(success)
    else:
        print("❌ Estrutura de prompt inválida. O arquivo deve conter a chave 'bug_to_user_story_v2'.")
        sys.exit(1)
    sys.exit(main())
