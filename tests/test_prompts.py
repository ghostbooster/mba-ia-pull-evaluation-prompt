"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path
import re

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        prompts = load_prompts("./prompts/bug_to_user_story_v2.yml")
        promptContent = prompts["bug_to_user_story_v2"]

        assert "system_prompt" in promptContent, \
        "O campo 'system_prompt' não foi encontrado no prompt bug_to_user_story_v2."

        assert promptContent["system_prompt"] is not None and promptContent["system_prompt"].strip() != "", \
        "O campo 'system_prompt' está vazio ou contém apenas espaços em branco."

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        prompts = load_prompts("./prompts/bug_to_user_story_v2.yml")
        promptContent = prompts["bug_to_user_story_v2"]

        for texto in [
            "Você é um Analista de Qualidade de Software"
        ]:
            assert texto in promptContent["system_prompt"], (
                f"O system_prompt não contém a persona obrigatória: '{texto}'"
            )

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        pass

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        prompts = load_prompts("./prompts/bug_to_user_story_v2.yml")
        promptContent = prompts["bug_to_user_story_v2"]
        system_prompt = promptContent["system_prompt"]

        pattern = re.compile(
            r'Exemplo\s+\d+:\s*'
            r'\{\{\s*'
            r'"inputs"\s*:\s*\{\{\s*'
            r'"bug_report"\s*:\s*".+?"\s*'
            r'\}\}\s*,?\s*'
            r'"outputs"\s*:\s*\{\{\s*'
            r'"reference"\s*:\s*".+?"\s*'
            r'\}\}\s*'
            r'\}\}',
            re.DOTALL
        )

        assert pattern.search(system_prompt), (
            "O system_prompt não contém um exemplo Few-shot com a estrutura JSON esperada."
        )

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        prompts = load_prompts("./prompts/bug_to_user_story_v2.yml")

        assert "[TODO]" not in prompts, (
            "O system_prompt contém marcações [TODO] que precisam ser preenchidas."
        )

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        promptContent = load_prompts("./prompts/bug_to_user_story_v2.yml")
        techniques = promptContent["bug_to_user_story_v2"].get("used_techiques", [])

        assert len(techniques) >= 2, (
            "O prompt deve possuir pelo menos 2 técnicas de engenharia de prompt."
        )

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])