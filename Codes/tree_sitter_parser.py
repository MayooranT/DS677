from tree_sitter import Language, Parser

Language.build_library(
    'build/lang.so',
    [
        './tree-sitter-cpp'
    ]
)
LANGUAGE = Language('build/lang.so', 'cpp')


QUERY = LANGUAGE.query("""
(function_definition
  declarator: (function_declarator
    declarator: (identifier) @fn-name
  )
)
""")


global_parser = Parser()
global_parser.set_language(LANGUAGE)


def get_fn_name(code, parser=global_parser):
    src = bytes(code, "utf8")
    tree = parser.parse(src)
    node = tree.root_node
    for cap, typ in QUERY.captures(node):
        if typ == "fn-name":
            return node_to_string(src, cap)
    return None


def node_to_string(src: bytes, node):
    return src[node.start_byte:node.end_byte].decode("utf8")


def make_parser():
    _parser = Parser()
    _parser.set_language(LANGUAGE)
    return _parser


RETURN_QUERY = LANGUAGE.query("""
(return_statement) @return
""")


def does_have_return(src, parser=global_parser):
    tree = parser.parse(bytes(src, "utf8"))
    root = tree.root_node
    captures = RETURN_QUERY.captures(root)
    for node, _ in captures:
        # if it doesn't have an argument, it's not a return with a value
        if len(node.children) <= 1:  # includes "return" itself
            continue
        else:
            return True

    return False


if __name__ == "__main__":
    code ="""
int add(int a, int b) {
    return a + b;
}

void greet() {
    std::cout << "Hello, World!" << std::endl;
}
"""
    print(global_parser.parse(bytes(code, "utf8")).root_node.sexp())
