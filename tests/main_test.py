import argparse
import pytest
import sys
from datetime import datetime
from unittest import mock
from todome.main import parse_args
from todome.main import virtualenv_check
from todome.main import mark
from todome.main import create_markdown_file
from todome.main import write_lines
from todome.main import add


def test_args():
    sys.argv = ['todome', '-a', 'test']
    args = parse_args()
    assert args.add == 'test'

def test_args_return_type():
    sys.argv = ['todome']
    args = parse_args()
    assert isinstance(args, argparse.Namespace)

@pytest.fixture
def mock_venv_false(monkeypatch):
    monkeypatch.setattr(sys, 'prefix', '/home/oli/.pyenv/versions/3.9.6')

@pytest.fixture
def mock_venv_true(monkeypatch):
    monkeypatch.setattr(sys, 'prefix', '/home/oli/projects/todome/venv')

def test_virtualenv_false(mock_venv_false):
    env = virtualenv_check()
    assert env is False

def test_virtualenv_true(mock_venv_true):
    env = virtualenv_check()
    assert env is True

@pytest.mark.parametrize(
    'entry, add_mark, expected', [
        # True = Add a mark
        # False = Remove a mark
        ('[ ]', True, '[x]'),
        ('[x]', False, '[ ]'),
        ('[x]', True, '[x]'),
        ('[ ]', False, '[ ]'),
    ]
)
def test_mark_pass(entry, add_mark, expected):
    assert mark(entry, add_mark) == expected

@pytest.mark.parametrize(
    'entry, add_mark, expected', [
        # True = Add a mark
        # False = Remove a mark
        ('[ ]', True, '[ ]'),
        ('[x]', True, '[ ]'),
        ('[ ]', True, '[]'),
        ('[x]', False, '[x]'),
        ('[ ]', False, '[x]'),
        ('[x]', False, '[]'),
    ]
)
def test_mark_fail(entry, add_mark, expected):
    assert mark(entry, add_mark) != expected


def test_create_markdown_file(tmpdir):
    # Should not FileExistsError with tmp file
    try:
        create_markdown_file(tmpdir)
    except FileExistsError:
        pytest.fail('Did not create (FileExistsError)')

def test_create_markdown_file_write(tmpdir):
    file = tmpdir.join('TODO.md')
    create_markdown_file(tmpdir)
    assert file.read() == '### Todo\n### In Progress\n### Completed\n'

def test_create_markdown_file_exists(tmpdir):
    with pytest.raises(SystemExit):
        create_markdown_file(tmpdir)
        create_markdown_file(tmpdir)

@pytest.mark.parametrize(
    'lines, expected', [
        (
            ['test\n', 'test\n', 'test\n'],
            ['test\n', 'test\n', 'test\n'],
        )
    ]
)
def test_write_lines(lines, expected, tmpdir):
    file = tmpdir.join('TODO.md')
    write_lines(tmpdir, lines)
    assert file.readlines() == expected

def test_add_FileNotFound_SystemExit(tmpdir):
    with pytest.raises(SystemExit):
        add(tmpdir, 'test')

def test_add_lines_formatting(tmpdir):
    with mock.patch('todome.main.datetime') as mock_dt:
        mock_dt.now.return_value = datetime(2021, 1, 1)

        file = tmpdir.join('TODO.md')
        create_markdown_file(tmpdir)
        add(tmpdir, 'test')
        assert file.read() == (f'### Todo\n'
                              f'- [ ] (_Fri 01/01/21, 00:00:00_ ) - test\n'
                              f'### In Progress\n'
                              f'### Completed\n')

# 
# def test_add_lines_missing_categories(tmpdir):
#     with pytest.raises(ValueError):
#         with mock.patch('todome.open') as mock_open:
#             mock_open.readlines.return_value = None
#             file = tmpdir.join('TODO.md')
#             create_markdown_file(tmpdir)
#             add(tmpdir, 'test')
