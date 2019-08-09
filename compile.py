import sys
import ast
from pprint import pprint

import click
import astunparse

import lexer
import parser
import py_parser


@click.command()
@click.argument('source_file')
@click.option('--strip_comments', default=0, help="Remove comments from tokens")
@click.option('--tokens', default=0, help="Show tokens generated by lexer")
@click.option('--ast', default=0, help="Show the internal AST (later transformed to Python AST")
@click.option('--py_ast', default=0, help="Show Python AST")
@click.option('--py_code', default=0, help="Show generated Python code")
def run(source_file, **kwargs):
    file_handler = open(source_file, 'r')
    source = file_handler.read()

    tokens = lexer.lexer(source)

    if kwargs["strip_comments"]:
        tokens = list(filter(lambda x: x["type"] != "COMMENT", tokens))
        tokens = list(filter(lambda x: x["type"] != "MULTILINE-COMMENT", tokens))

    if kwargs["tokens"]:
        pprint(tokens)
        return

    ast_ = parser.parse(tokens)

    if kwargs["ast"]:
        pprint(ast_)
        return

    py_ast = py_parser.ast_to_py_ast(ast_)

    if kwargs["py_ast"]:
        pprint(ast.dump(py_ast))
        return

    if kwargs["py_code"]:
        print(astunparse.unparse(py_ast))
        return

    exec(compile(py_ast, filename="<ast>", mode="exec"))


if __name__ == '__main__':
    run()