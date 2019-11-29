#!/usr/bin/env python3

import click

from pathlib import Path
from .file_handler import FileHandler


@click.command()
@click.argument('file_path', type=click.Path(exists=True))
def brs_beautify(file_path: str) -> None:
    file_path = Path(file_path)

    if file_path.suffix != '.brs':
        click.echo(f'Invalid file type | {file_path.suffix}')
        return

    current_file = FileHandler(file_path)
    current_file.beautify_lines()


if __name__ == '__main__':
    brs_beautify()
