import importlib.util
import sys
import types
import pathlib
import builtins


def load_cmdargs():
    path = pathlib.Path(__file__).resolve().parents[1] / "subsync" / "cmdargs.py"
    spec = importlib.util.spec_from_file_location("subsync.cmdargs", path)
    module = importlib.util.module_from_spec(spec)

    # Provide dummy translation and description modules
    builtins._ = lambda x: x
    sys.modules['subsync.translations'] = types.SimpleNamespace(_=lambda x: x)

    sys.modules['subsync'] = types.ModuleType('subsync')
    sys.modules['subsync.data'] = types.ModuleType('subsync.data')
    desc = types.ModuleType('subsync.data.descriptions')
    desc.cmdopts = {}
    sys.modules['subsync.data.descriptions'] = desc

    spec.loader.exec_module(module)
    return module


cmdargs = load_cmdargs()


def test_parse_help():
    assert cmdargs.parseCmdArgs(['app', '--help']) == {'help': True}


def test_parse_simple_sync():
    opts = cmdargs.parseCmdArgs([
        'app', 'sync', '--sub', 'sub.srt', '--ref', 'ref.mkv', '--out', 'out.srt'
    ])
    assert opts == {
        'sync': [{
            'sub': {'path': 'sub.srt'},
            'ref': {'path': 'ref.mkv'},
            'out': {'path': 'out.srt'}
        }]
    }


def test_invalid_option(capsys):
    res = cmdargs.parseCmdArgs(['app', '--foo'])
    captured = capsys.readouterr()
    assert res is None
    assert "unrecognized option '--foo'" in captured.err


def test_duplicate_option(capsys):
    res = cmdargs.parseCmdArgs(['app', '--verbose', '1', '--verbose', '2'])
    captured = capsys.readouterr()
    assert res is None
    assert 'verbose' in captured.err
