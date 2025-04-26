import os
import pandas as pd
import pytest
from controle_migracao import config


def test_arquivos_existem():
    assert os.path.exists(config.DATA_FILE), "Arquivo data.csv não encontrado!"
    assert os.path.exists(config.FLUXOS_FILE), "Arquivo fluxos.csv não encontrado!"
    assert os.path.exists(config.CONTROLE_FILE), "Arquivo controle_fluxos.csv não encontrado!"


def test_atualizar_disponibilidade_nao_quebra():
    try:
        config.atualizar_disponibilidade_para_migrar()
    except Exception as e:
        pytest.fail(f"Erro ao executar atualizar_disponibilidade_para_migrar: {e}")
