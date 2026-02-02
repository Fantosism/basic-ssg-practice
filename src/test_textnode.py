import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node3", TextType.TEXT)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ANCHOR, "https://www.foo.bar")
        node2 = TextNode("This is a text node", TextType.ANCHOR, "https://www.foo.bar")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a bold node", TextType.BOLD, "https://www.foo.bar")
        self.assertEqual("TextNode(This is a bold node, ('bold',), https://www.foo.bar)", repr(node))

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_anchor(self):
        node = TextNode("This is a text node", TextType.ANCHOR, "https://www.foo.bar")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "https://www.foo.bar"})

    def test_img(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://www.qax.qux")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"alt": "This is a text node", "src": "https://www.qax.qux"})



if __name__ == '__main__':
    unittest.main()