import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_text_node(self):
        node = TextNode('Hello world', TextType.TEXT)
        self.assertEqual(node, TextNode('Hello world', TextType.TEXT))

    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_bold_delimiter(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ])

    def test_italic_delimiter(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ])

    def test_no_delimiters(self):
        node = TextNode("plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("plain text", TextType.TEXT)])

    def test_unmatched_delimiter_raises(self):
        node = TextNode("unmatched `code block", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_multiple_nodes_input(self):
        nodes = [
            TextNode("text with `code`", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("more `code` here", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("already bold", TextType.BOLD),
            TextNode("more ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ])

    def test_delimiter_at_start(self):
        node = TextNode("`code` after", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("code", TextType.CODE),
            TextNode(" after", TextType.TEXT),
        ])

    def test_delimiter_at_end(self):
        node = TextNode("before `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("before ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ])

    def test_delimiter_at_both_ends(self):
        node = TextNode("`code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("code", TextType.CODE),
        ])

class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        text = "This is an image ![foo](https://www.foo.bar)"
        self.assertEqual(extract_markdown_images(text), [("foo", "https://www.foo.bar")])

    def test_multiple_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_nested_brackets_in_alt_text(self):
        text = "This is an image ![alt [nested] text](https://www.foo.bar)"
        self.assertEqual(extract_markdown_images(text), [])

    def test_nested_parentheses_in_url(self):
        text = "This is an image ![foo](https://en.wikipedia.org/wiki/Python_(language))"
        self.assertEqual(extract_markdown_images(text), [])

    def test_valid_image_alongside_nested(self):
        text = "![valid](https://valid.com) and ![invalid [nested]](https://foo.bar)"
        self.assertEqual(extract_markdown_images(text), [("valid", "https://valid.com")])

    def test_no_images(self):
        text = "This is plain text with no images"
        self.assertEqual(extract_markdown_images(text), [])

    def test_empty_alt_text(self):
        text = "Image with no alt ![](https://www.foo.bar)"
        self.assertEqual(extract_markdown_images(text), [("", "https://www.foo.bar")])

    def test_link_not_image(self):
        text = "This is a link [foo](https://www.foo.bar)"
        self.assertEqual(extract_markdown_images(text), [])

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        text = "This is a link [foo](https://www.foo.bar)"
        self.assertEqual(extract_markdown_links(text), [("foo", "https://www.foo.bar")])

    def test_multiple_links(self):
        text = "This is a link [foo](https://www.foo.bar) and [youtube](https://www.youtube.com)"
        self.assertEqual(extract_markdown_links(text), [("foo", "https://www.foo.bar"), ("youtube", "https://www.youtube.com")])

    def test_image_not_link(self):
        text = "This is an image link ![foo](https://www.foo.bar)"
        self.assertEqual(extract_markdown_links(text), [])

    def test_nested_brackets(self):
        text = "This is [invalid [markdown]](https://www.foo.bar)"
        self.assertEqual(extract_markdown_links(text), [])

    def test_nested_parentheses(self):
        text = "This is [invalid markdown](https://www.foo.bar?q=(foo))"
        self.assertEqual(extract_markdown_links(text), [])

    def test_no_links(self):
        text = "This is plain text with no links"
        self.assertEqual(extract_markdown_links(text), [])

    def test_empty_anchor_text(self):
        text = "Link with no text [](https://www.foo.bar)"
        self.assertEqual(extract_markdown_links(text), [("", "https://www.foo.bar")])

    def test_links_and_images_mixed(self):
        text = "A [link](https://link.com) and ![image](https://image.com) together"
        self.assertEqual(extract_markdown_links(text), [("link", "https://link.com")])

class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        node = TextNode("This is ![alt](https://example.com/img.png) text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" text", TextType.TEXT),
        ])

    def test_multiple_images(self):
        node = TextNode("![one](https://one.com) and ![two](https://two.com)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("one", TextType.IMAGE, "https://one.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.IMAGE, "https://two.com"),
        ])

    def test_image_at_start(self):
        node = TextNode("![img](https://example.com) after", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("img", TextType.IMAGE, "https://example.com"),
            TextNode(" after", TextType.TEXT),
        ])

    def test_image_at_end(self):
        node = TextNode("before ![img](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("before ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "https://example.com"),
        ])

    def test_only_image(self):
        node = TextNode("![img](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("img", TextType.IMAGE, "https://example.com"),
        ])

    def test_no_images(self):
        node = TextNode("plain text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("plain text with no images", TextType.TEXT),
        ])

    def test_non_text_node_unchanged(self):
        node = TextNode("bold text", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [node])

    def test_multiple_nodes_input(self):
        nodes = [
            TextNode("![img](https://example.com)", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("text ![img2](https://two.com) here", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(new_nodes, [
            TextNode("img", TextType.IMAGE, "https://example.com"),
            TextNode("already bold", TextType.BOLD),
            TextNode("text ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "https://two.com"),
            TextNode(" here", TextType.TEXT),
        ])

    def test_link_not_image(self):
        node = TextNode("This is [link](https://example.com) not image", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("This is [link](https://example.com) not image", TextType.TEXT),
        ])

class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        node = TextNode("This is [anchor](https://example.com) text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("anchor", TextType.ANCHOR, "https://example.com"),
            TextNode(" text", TextType.TEXT),
        ])

    def test_multiple_links(self):
        node = TextNode("[one](https://one.com) and [two](https://two.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode("one", TextType.ANCHOR, "https://one.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.ANCHOR, "https://two.com"),
        ])

    def test_link_at_start(self):
        node = TextNode("[link](https://example.com) after", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode("link", TextType.ANCHOR, "https://example.com"),
            TextNode(" after", TextType.TEXT),
        ])

    def test_link_at_end(self):
        node = TextNode("before [link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode("before ", TextType.TEXT),
            TextNode("link", TextType.ANCHOR, "https://example.com"),
        ])

    def test_only_link(self):
        node = TextNode("[link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode("link", TextType.ANCHOR, "https://example.com"),
        ])

    def test_no_links(self):
        node = TextNode("plain text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode("plain text with no links", TextType.TEXT),
        ])

    def test_non_text_node_unchanged(self):
        node = TextNode("bold text", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])

    def test_multiple_nodes_input(self):
        nodes = [
            TextNode("[link](https://example.com)", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("text [link2](https://two.com) here", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(new_nodes, [
            TextNode("link", TextType.ANCHOR, "https://example.com"),
            TextNode("already bold", TextType.BOLD),
            TextNode("text ", TextType.TEXT),
            TextNode("link2", TextType.ANCHOR, "https://two.com"),
            TextNode(" here", TextType.TEXT),
        ])

    def test_image_not_link(self):
        node = TextNode("This is ![img](https://example.com) not link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode("This is ![img](https://example.com) not link", TextType.TEXT),
        ])

    def test_mixed_links_and_images(self):
        node = TextNode("A [link](https://link.com) and ![img](https://img.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode("A ", TextType.TEXT),
            TextNode("link", TextType.ANCHOR, "https://link.com"),
            TextNode(" and ![img](https://img.com)", TextType.TEXT),
        ])


if __name__ == '__main__':
    unittest.main()