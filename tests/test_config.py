import os
import config


def test_files_exist():
    assert os.path.exists(config.DATA_FILE)
    assert os.path.exists(config.FLUXOS_FILE)
    assert os.path.exists(config.CONTROLE_FILE)
