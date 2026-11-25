import inspect
import re

from govia_agent_source.ouvidoria import EncaminhamentoAgent, TriagemManifestacaoAgent
from govia_agent_source.ouvidoria.encaminhamento_agent import encaminhar
from govia_agent_source.ouvidoria.triagem_agent import triar
from govia_agent_source.ouvidoria.ferramentas import classificar_manifestacao, mascarar_dados_pessoais


def test_triagem_mascara_dados_pessoais_e_classifica():
    caso = triar("2026-000123", "Reclamação: demora no atendimento. CPF 123.456.789-00, maria@exemplo.com")
    assert "[CPF]" in caso["texto"] and "[EMAIL]" in caso["texto"]
    assert "123.456.789-00" not in caso["texto"]
    assert caso["categoria"] == "reclamacao"
    assert caso["situacao"] == "em_analise"


def test_encaminhamento_exige_aprovacao_humana():
    caso = {"protocolo": "2026-000123", "categoria": "denuncia"}
    pendente = encaminhar(caso, aprovado_por_humano=False)
    assert pendente["situacao"] == "aguardando_aprovacao"
    assert pendente["setor"] == "corregedoria"
    feito = encaminhar(caso, aprovado_por_humano=True)
    assert feito["situacao"] == "encaminhado"


def test_manifestacao_sem_termo_conhecido_nao_e_inventada():
    assert classificar_manifestacao("texto qualquer")["categoria"] == "nao_classificada"
    assert mascarar_dados_pessoais("sem dados") == "sem dados"


def test_agentes_declaram_formato_reconhecido_pelo_scanner():
    for agente in (TriagemManifestacaoAgent, EncaminhamentoAgent):
        fonte = inspect.getsource(agente)
        assert re.search(r"(?m)^\s*kind\s*=\s*[\"']agent[\"']\s*$", fonte)
        assert re.search(r"(?m)^\s*tools\s*=\s*\[[^\]]+\]\s*$", fonte)
        assert re.search(r"(?m)^\s*MODEL_REFERENCE\s*=\s*\"[^\"]+\"\s*$", fonte)
        assert "def " not in fonte


def test_arquivos_dos_agentes_sem_aspas_triplas():
    # O scanner so prova o vinculo agente->modelo/ferramenta sem blocos de aspas triplas.
    import pathlib
    pasta = pathlib.Path(__file__).resolve().parents[1] / "src" / "govia_agent_source" / "ouvidoria"
    for nome in ("triagem_agent.py", "encaminhamento_agent.py"):
        assert chr(34) * 3 not in (pasta / nome).read_text(encoding="utf-8")
