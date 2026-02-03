import unittest

from htmlnode import LeafNode, ParentNode
from markdown import (
    markdown_to_html_node,
    text_to_children,
    paragraph_to_html_node,
    heading_to_html_node,
    code_to_html_node,
    quote_to_html_node,
    unordered_list_to_html_node,
    ordered_list_to_html_node,
)

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraph(self):
        node = markdown_to_html_node("This is a paragraph")
        self.assertEqual(node, ParentNode("div", [
            ParentNode("p", [LeafNode(None, "This is a paragraph")])
        ]))

    def test_paragraph_with_link(self):
        node = markdown_to_html_node("Check [this](https://example.com) out")
        self.assertEqual(node, ParentNode("div", [
            ParentNode("p", [
                LeafNode(None, "Check "),
                LeafNode("a", "this", {"href": "https://example.com"}),
                LeafNode(None, " out"),
            ])
        ]))

    def test_paragraph_with_image(self):
        node = markdown_to_html_node("An image ![alt](https://img.com)")
        self.assertEqual(node, ParentNode("div", [
            ParentNode("p", [
                LeafNode(None, "An image "),
                LeafNode("img", "alt", {"src": "https://img.com", "alt": "alt"}),
            ])
        ]))

    def test_multiple_paragraphs(self):
        node = markdown_to_html_node("First paragraph\n\nSecond paragraph")
        self.assertEqual(node, ParentNode("div", [
            ParentNode("p", [LeafNode(None, "First paragraph")]),
            ParentNode("p", [LeafNode(None, "Second paragraph")]),
        ]))

    def test_heading_with_link(self):
        node = markdown_to_html_node("## Check [this](https://example.com)")
        self.assertEqual(node, ParentNode("div", [
            ParentNode("h2", [
                LeafNode(None, "Check "),
                LeafNode("a", "this", {"href": "https://example.com"}),
            ])
        ]))

    def test_heading(self):
        node = markdown_to_html_node("# Heading")
        self.assertEqual(node, ParentNode("div", [
            ParentNode("h1", [LeafNode(None, "Heading")])
        ]))

    def test_multiple_blocks(self):
        node = markdown_to_html_node("# Heading\n\nParagraph text")
        self.assertEqual(node, ParentNode("div", [
            ParentNode("h1", [LeafNode(None, "Heading")]),
            ParentNode("p", [LeafNode(None, "Paragraph text")]),
        ]))

    def test_empty_markdown(self):
        node = markdown_to_html_node("")
        self.assertEqual(node, ParentNode("div", []))

    def test_all_block_types(self):
        md = """
# Heading

Paragraph

```
code
```

>quote

- item

1. ordered
"""
        node = markdown_to_html_node(md)
        self.assertEqual(node, ParentNode("div", [
            ParentNode("h1", [LeafNode(None, "Heading")]),
            ParentNode("p", [LeafNode(None, "Paragraph")]),
            ParentNode("pre", [ParentNode("code", [LeafNode(None, "\ncode\n")])]),
            ParentNode("blockquote", [LeafNode(None, "quote")]),
            ParentNode("ul", [ParentNode("li", [LeafNode(None, "item")])]),
            ParentNode("ol", [ParentNode("li", [LeafNode(None, "ordered")])]),
        ]))

class TestTextToChildren(unittest.TestCase):
    def test_plain_text(self):
        children = text_to_children("plain text")
        self.assertEqual(children, [LeafNode(None, "plain text")])

    def test_bold(self):
        children = text_to_children("**bold**")
        self.assertEqual(children, [LeafNode("b", "bold")])

    def test_italic(self):
        children = text_to_children("_italic_")
        self.assertEqual(children, [LeafNode("i", "italic")])

    def test_code(self):
        children = text_to_children("`code`")
        self.assertEqual(children, [LeafNode("code", "code")])

    def test_mixed_inline(self):
        children = text_to_children("text **bold** and _italic_")
        self.assertEqual(children, [
            LeafNode(None, "text "),
            LeafNode("b", "bold"),
            LeafNode(None, " and "),
            LeafNode("i", "italic"),
        ])

    def test_empty_string(self):
        children = text_to_children("")
        self.assertEqual(children, [])

    def test_link(self):
        children = text_to_children("[link](https://example.com)")
        self.assertEqual(children, [LeafNode("a", "link", {"href": "https://example.com"})])

    def test_image(self):
        children = text_to_children("![alt](https://example.com/img.png)")
        self.assertEqual(children, [LeafNode("img", "alt", {"src": "https://example.com/img.png", "alt": "alt"})])

    def test_multiple_links(self):
        children = text_to_children("[one](https://one.com) and [two](https://two.com)")
        self.assertEqual(children, [
            LeafNode("a", "one", {"href": "https://one.com"}),
            LeafNode(None, " and "),
            LeafNode("a", "two", {"href": "https://two.com"}),
        ])

    def test_all_inline_types(self):
        children = text_to_children("**bold** _italic_ `code` [link](https://x.com)")
        self.assertEqual(children, [
            LeafNode("b", "bold"),
            LeafNode(None, " "),
            LeafNode("i", "italic"),
            LeafNode(None, " "),
            LeafNode("code", "code"),
            LeafNode(None, " "),
            LeafNode("a", "link", {"href": "https://x.com"}),
        ])


class TestParagraphToHtmlNode(unittest.TestCase):
    def test_simple(self):
        node = paragraph_to_html_node("Hello world")
        self.assertEqual(node, ParentNode("p", [LeafNode(None, "Hello world")]))

    def test_with_bold(self):
        node = paragraph_to_html_node("This is **bold**")
        self.assertEqual(node, ParentNode("p", [
            LeafNode(None, "This is "),
            LeafNode("b", "bold"),
        ]))

    def test_with_multiple_inline(self):
        node = paragraph_to_html_node("**bold** and _italic_")
        self.assertEqual(node, ParentNode("p", [
            LeafNode("b", "bold"),
            LeafNode(None, " and "),
            LeafNode("i", "italic"),
        ]))


class TestHeadingToHtmlNode(unittest.TestCase):
    def test_h1(self):
        node = heading_to_html_node("# Heading")
        self.assertEqual(node, ParentNode("h1", [LeafNode(None, "Heading")]))

    def test_h2(self):
        node = heading_to_html_node("## Heading")
        self.assertEqual(node, ParentNode("h2", [LeafNode(None, "Heading")]))

    def test_h3(self):
        node = heading_to_html_node("### Heading")
        self.assertEqual(node, ParentNode("h3", [LeafNode(None, "Heading")]))

    def test_h6(self):
        node = heading_to_html_node("###### Heading")
        self.assertEqual(node, ParentNode("h6", [LeafNode(None, "Heading")]))

    def test_with_inline(self):
        node = heading_to_html_node("## **Bold** heading")
        self.assertEqual(node, ParentNode("h2", [
            LeafNode("b", "Bold"),
            LeafNode(None, " heading"),
        ]))


class TestCodeToHtmlNode(unittest.TestCase):
    def test_simple(self):
        node = code_to_html_node("```\ncode\n```")
        self.assertEqual(node, ParentNode("pre", [
            ParentNode("code", [LeafNode(None, "\ncode\n")])
        ]))

    def test_no_inline_processing(self):
        node = code_to_html_node("```\n**not bold**\n```")
        self.assertEqual(node, ParentNode("pre", [
            ParentNode("code", [LeafNode(None, "\n**not bold**\n")])
        ]))

    def test_multiline(self):
        node = code_to_html_node("```\nline1\nline2\n```")
        self.assertEqual(node, ParentNode("pre", [
            ParentNode("code", [LeafNode(None, "\nline1\nline2\n")])
        ]))

    def test_code_with_special_chars(self):
        node = code_to_html_node("```\n<div>html</div>\n```")
        self.assertEqual(node, ParentNode("pre", [
            ParentNode("code", [LeafNode(None, "\n<div>html</div>\n")])
        ]))


class TestQuoteToHtmlNode(unittest.TestCase):
    def test_single_line_no_space(self):
        node = quote_to_html_node(">quote")
        self.assertEqual(node, ParentNode("blockquote", [LeafNode(None, "quote")]))

    def test_single_line_with_space(self):
        node = quote_to_html_node("> quote")
        self.assertEqual(node, ParentNode("blockquote", [LeafNode(None, "quote")]))

    def test_multiline(self):
        node = quote_to_html_node(">line one\n>line two")
        self.assertEqual(node, ParentNode("blockquote", [LeafNode(None, "line one\nline two")]))

    def test_multiline_with_space(self):
        node = quote_to_html_node("> line one\n> line two")
        self.assertEqual(node, ParentNode("blockquote", [LeafNode(None, "line one\nline two")]))

    def test_with_inline(self):
        node = quote_to_html_node(">**bold** quote")
        self.assertEqual(node, ParentNode("blockquote", [
            LeafNode("b", "bold"),
            LeafNode(None, " quote"),
        ]))


class TestUnorderedListToHtmlNode(unittest.TestCase):
    def test_single_item(self):
        node = unordered_list_to_html_node("- item")
        self.assertEqual(node, ParentNode("ul", [
            ParentNode("li", [LeafNode(None, "item")])
        ]))

    def test_multiple_items(self):
        node = unordered_list_to_html_node("- one\n- two\n- three")
        self.assertEqual(node, ParentNode("ul", [
            ParentNode("li", [LeafNode(None, "one")]),
            ParentNode("li", [LeafNode(None, "two")]),
            ParentNode("li", [LeafNode(None, "three")]),
        ]))

    def test_with_inline(self):
        node = unordered_list_to_html_node("- **bold** item")
        self.assertEqual(node, ParentNode("ul", [
            ParentNode("li", [
                LeafNode("b", "bold"),
                LeafNode(None, " item"),
            ])
        ]))

    def test_item_with_link(self):
        node = unordered_list_to_html_node("- Check [link](https://example.com)")
        self.assertEqual(node, ParentNode("ul", [
            ParentNode("li", [
                LeafNode(None, "Check "),
                LeafNode("a", "link", {"href": "https://example.com"}),
            ])
        ]))

class TestOrderedListToHtmlNode(unittest.TestCase):
    def test_single_item(self):
        node = ordered_list_to_html_node("1. item")
        self.assertEqual(node, ParentNode("ol", [
            ParentNode("li", [LeafNode(None, "item")])
        ]))

    def test_multiple_items(self):
        node = ordered_list_to_html_node("1. one\n2. two\n3. three")
        self.assertEqual(node, ParentNode("ol", [
            ParentNode("li", [LeafNode(None, "one")]),
            ParentNode("li", [LeafNode(None, "two")]),
            ParentNode("li", [LeafNode(None, "three")]),
        ]))

    def test_double_digits(self):
        node = ordered_list_to_html_node("10. ten\n11. eleven")
        self.assertEqual(node, ParentNode("ol", [
            ParentNode("li", [LeafNode(None, "ten")]),
            ParentNode("li", [LeafNode(None, "eleven")]),
        ]))

    def test_with_inline(self):
        node = ordered_list_to_html_node("1. **bold** item")
        self.assertEqual(node, ParentNode("ol", [
            ParentNode("li", [
                LeafNode("b", "bold"),
                LeafNode(None, " item"),
            ])
        ]))

    def test_item_with_link(self):
        node = ordered_list_to_html_node("1. Check [link](https://example.com)")
        self.assertEqual(node, ParentNode("ol", [
            ParentNode("li", [
                LeafNode(None, "Check "),
                LeafNode("a", "link", {"href": "https://example.com"}),
            ])
        ]))


if __name__ == '__main__':
    unittest.main()
