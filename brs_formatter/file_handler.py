#!/usr/bin/env python3

import click


class FileHandler:
    def __init__(self, file_path: object):
        self.file_path = file_path
        self.name = file_path.name
        self.classified_lines = self.parse_file(self.file_path)
        self.depth = 0

    def parse_file(self, file_path: object) -> list:
        if file_path.suffix == '.brs':
            brs_file = None
            try:
                brs_file = self.file_path.open('r')
                return [self.classify_line(line) for line in enumerate(brs_file.readlines())]
            except IOError:
                click.echo('Error reading files, exiting gracefully')
                return []
            finally:
                if brs_file is not None:
                    brs_file.close()

    @staticmethod
    def standardize_line(line: str) -> str:
        return ' '.join(line.lstrip().rstrip('\n').split())

    @staticmethod
    def classifications(classification_id: int) -> dict:
        classifiers = {
            0: {"name": 'variable_declaration', "before": 0, "after": 0},
            1: {"name": 'conditional_statement_start', "before": 0, "after": 1},
            2: {"name": 'conditional_statement_end', "before": -1, "after": 0},
            3: {"name": 'loop_start', "before": 0, "after": 1},
            4: {"name": 'loop_end', "before": -1, "after": 0},
            5: {"name": 'dictionary_start', "before": 0, "after": 1},
            6: {"name": 'dictionary_end', "before": -1, "after": 0},
            7: {"name": 'list_start', "before": 0, "after": 1},
            8: {"name": 'list_end', "before": -1, "after": 0},
            9: {"name": 'function_start', "before": 0, "after": 1},
            10: {"name": 'function_end', "before": -1, "after": 0},
            11: {"name": 'return', "before": 0, "after": 0},
            12: {"name": 'if_then', "before": 0, "after": 0},
            13: {"name": 'conditional_statement_else', "before": -1, "after": 1},
            13: {"name": 'comment', "before": 0, "after": 0},
        }

        return classifiers.get(classification_id, {"name": 'unknown', "before": 0, "after": 0})

    def classify_line(self, line: tuple) -> object:
        classified_line = {
            'line_number': line[0],
            'original_line': line[1],
            'formatted_line': self.standardize_line(line[1]),
            'classification': None
        }
        line_check = classified_line["formatted_line"].lower()

        if len(line_check) > 0 and line_check[0] == '\'':
            classified_line['classification'] = self.classifications(13)
        elif 'end function' in line_check or 'end sub' in line_check:
            classified_line['classification'] = self.classifications(10)
            classified_line["formatted_line"] = classified_line["formatted_line"] + '\n'
        elif 'end if' in line_check:
            classified_line['classification'] = self.classifications(2)
            classified_line["formatted_line"] = classified_line["formatted_line"] + '\n'
        elif 'end for' in line_check:
            classified_line['classification'] = self.classifications(4)
        elif 'end while' in line_check:
            classified_line['classification'] = self.classifications(4)
        elif 'return' in line_check:
            classified_line['classification'] = self.classifications(11)
        elif 'function' in line_check or 'sub' in line_check:
            classified_line['classification'] = self.classifications(9)
            if 'as void' in line_check:
                classified_line["formatted_line"] = classified_line["formatted_line"].replace('as void', '').rstrip()
        elif 'if' in line_check or 'else' in line_check:
            if 'then' in line_check and line_check.split()[-1] != 'then':
                classified_line['classification'] = self.classifications(12)
            elif 'else' in line_check:
                classified_line['classification'] = self.classifications(13)
            else:
                classified_line['classification'] = self.classifications(1)

            if 'and' in line_check:
                classified_line["formatted_line"] = classified_line["formatted_line"].replace('and', 'AND')
            elif 'or' in line_check:
                classified_line["formatted_line"] = classified_line["formatted_line"].replace('or', 'OR')
            elif 'not' in line_check:
                classified_line["formatted_line"] = classified_line["formatted_line"].replace('not', 'NOT')
        elif 'for each' in line_check or 'for i' in line_check:
            classified_line['classification'] = self.classifications(3)
        elif 'while' in line_check:
            classified_line['classification'] = self.classifications(3)
        elif '{' in line_check and '}' not in line_check:
            classified_line['classification'] = self.classifications(5)
        elif '}' in line_check and '{' not in line_check:
            classified_line['classification'] = self.classifications(6)
        else:
            classified_line['classification'] = self.classifications(-1)

        return classified_line

    def beautify_lines(self):
        temp = []
        for line in self.classified_lines:
            if line["classification"]["before"] > 0:
                self.depth += line["classification"]["before"]
            elif self.depth != 0:
                self.depth += line["classification"]["before"]

            if self.depth > 0:
                tabs = ['\t' for i in range(self.depth)]
                line["formatted_line"] = f'{"".join(tabs)}{line["formatted_line"]}\n'
            else:
                line["formatted_line"] += '\n'

            if line["classification"]["after"] > 0:
                self.depth += line["classification"]["after"]
            elif self.depth != 0:
                self.depth += line["classification"]["after"]

            if line["classification"]["name"] == 'return':
                temp.append('\n')

            temp.append(line["formatted_line"])

        self.file_path.write_text(' '.join(temp))

    def __str__(self):
        return self.name