import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        segments = node.text.split(delimiter)
        if len(segments) % 2 == 0:
            raise Exception(f"No matching {delimiter} found, invalid syntax")
        for i in range(len(segments)):
            if segments[i] == '':
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(segments[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(segments[i], text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    raise NotImplementedError

def split_nodes_link(old_nodes):
    raise NotImplementedError

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)