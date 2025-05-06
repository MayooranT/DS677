from tree_sitter import Language, Parser
import ast

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

RETURN_QUERY = LANGUAGE.query("""
(return_statement) @return
""")

global_parser = Parser()
global_parser.set_language(LANGUAGE)

def does_have_return(entry: dict, parser=global_parser, return_query=RETURN_QUERY) -> bool:
    try:
        content_dict = ast.literal_eval(entry)
        #content_dict = entry
        code = content_dict.get("code", "")
        if not code.strip():
            return False

        tree = parser.parse(bytes(code, "utf8"))
        root = tree.root_node
        captures = return_query.captures(root)

        for node, _ in captures:
            if len(node.children) >= 1:  # return with a value
                return True
    except Exception as e:
        print(f"Failed to process: {e}")
    return False



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

# def does_have_return(src, parser=global_parser):
#     tree = parser.parse(bytes(src, "utf8"))
#     root = tree.root_node
#     captures = RETURN_QUERY.captures(root)
#     for node, _ in captures:
#         # if it doesn't have an argument, it's not a return with a value
#         if len(node.children) <= 1:  # includes "return" itself
#             continue
#         else:
#             return True

#     return False


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
