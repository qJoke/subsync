import importlib.util
import sys
import types
import pathlib


def load_utils():
    path = pathlib.Path(__file__).resolve().parents[1] / "subsync" / "utils.py"
    spec = importlib.util.spec_from_file_location("subsync.utils", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules['subsync.translations'] = types.SimpleNamespace(_=lambda x: x)
    spec.loader.exec_module(module)
    return module

utils = load_utils()


def test_file_size_fmt_bytes():
    assert utils.fileSizeFmt(500) == "500.0 B"


def test_file_size_fmt_kilobytes():
    assert utils.fileSizeFmt(2048) == "2.0 kB"


def test_file_size_fmt_megabytes():
    assert utils.fileSizeFmt(2 * 1000 * 1000) == "2.0 MB"


def test_file_size_fmt_gigabytes():
    assert utils.fileSizeFmt(3 * 1000 * 1000 * 1000) == "3.0 GB"


