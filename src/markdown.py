from block_markdown import BlockType, markdown_to_blocks, block_to_block_type
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html_node(block))
        elif block_type == BlockType.HEADING:
            children.append(heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            children.append(code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(unordered_list_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(ordered_list_to_html_node(block))

    return ParentNode("div", children)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children

def paragraph_to_html_node(block):
    children = text_to_children(block)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    text = block[3:-3]
    code_node = ParentNode("code", [LeafNode(None, text)])
    return ParentNode("pre", [code_node])

def quote_to_html_node(block):
    lines = block.split("\n")
    stripped = []
    for line in lines:
        stripped.append(line[1:].lstrip())
    text = "\n".join(stripped)
    children = text_to_children(text)
    return ParentNode("blockquote", children)

def unordered_list_to_html_node(block):
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        li_nodes.append(ParentNode("li", children))
    return ParentNode("ul", li_nodes)

def ordered_list_to_html_node(block):
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        text = line.split(". ", 1)[1]
        children = text_to_children(text)
        li_nodes.append(ParentNode("li", children))
    return ParentNode("ol", li_nodes)


def extract_title(markdown):
    h1_headers = [line[2:].strip() for line in markdown.splitlines() if line.startswith("# ")]

    if not h1_headers:
        raise ValueError("No title (h1 header) found")
    if len(h1_headers) > 1:
        raise ValueError("Only one title allowed per document")

    return h1_headers[0]