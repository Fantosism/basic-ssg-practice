import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode("div", "Hello world", None, {"class": "foo"})
        self.assertEqual(node.props_to_html(), ' class="foo"')

    def test_values(self):
        node = HTMLNode("div", "Hello world")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello world")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_repr(self):
        node = HTMLNode("div", "Hello world", None, {"class": "foo"})
        self.assertEqual(repr(node), "HTMLNode(div, Hello world, None, {'class': 'foo'})")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello world")
        self.assertEqual(node.to_html(), "<p>Hello world</p>")

    def test_leaf_to_html_anchor(self):
        node = LeafNode("a", "Hello world", {"href": "https://www.foo.bar"})
        self.assertEqual(node.to_html(), '<a href="https://www.foo.bar">Hello world</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><span>child2</span></div>")

    def test_to_html_with_multiple_children_and_grandchildren(self):
        grandchild_node = LeafNode("i", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><i>grandchild</i></span><span>child2</span></div>",
        )

    def test_to_html_with_nested_parents(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        child_node2 = LeafNode("span", "child2")
        parent_node2 = ParentNode("section", [parent_node, child_node2])
        self.assertEqual(
            parent_node2.to_html(),
            "<section><div><span>child</span></div><span>child2</span></section>",
        )


if __name__ == '__main__':
    unittest.main()