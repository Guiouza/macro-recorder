from os import getcwd
from pathlib import Path
from src.models import Macros


def test_macros_model():
    folder = Path(getcwd()) / '.macros/'
    folder.mkdir(exist_ok=True, parents=True)
    macros = Macros(folder.as_posix())

    try:
        assert macros.get_all() == []
        assert macros.search_by_name('teste') is None
        assert macros.delete('teste') is False
        assert macros.create('teste') is not None

        assert macros.get_all() == ['teste']
        assert macros.search_by_name('teste') is not None
        assert macros.create('teste') is None
        assert macros.delete('teste') is True
    finally:
        for file in folder.glob('*'):
            file.unlink()
        folder.rmdir()
