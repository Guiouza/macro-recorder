from pathlib import Path


class Macros():
    def __init__(self, folder: str):
        self.folder: Path = Path(folder)
        self.folder.mkdir(exist_ok=True, parents=True)
        self.macros: list[str] = list()
        # load macro files 
        for file in self.folder.glob('*.macro'):
            self.macros.append(file.stem)

    def get_all(self) -> list[str]:
        return self.macros

    def search_by_name(self, macro_name: str) -> Path | None:
        if macro_name not in self.macros:
            return None
        return self.folder / f'{macro_name}.macro'

    def create(self, macro_name: str) -> Path | None:
        if macro_name in self.macros:
            return None
        macro = self.folder / f'{macro_name}.macro'
        macro.touch()
        self.macros.append(macro_name)
        return macro

    def delete(self, macro_name: str) -> bool:
        macro = self.search_by_name(macro_name)
        if macro is None:
            return False
        macro.unlink()
        self.macros.remove(macro_name)
        return True
