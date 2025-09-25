import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    # HTML node tests

    def test_html_all_values(self):
        node = HTMLNode(tag="h1", value="This is a heading", children=["h2", "p"], props={"href": "https://www.boot.dev"})
        self.assertEqual("HTMLNode(h1, This is a heading, ['h2', 'p'], {'href': 'https://www.boot.dev'})", repr(node))

    def test_html_no_tag(self):
        node = HTMLNode(value="This is a heading", children=["h2", "p"], props={"href": "https://www.boot.dev"})
        self.assertEqual("HTMLNode(None, This is a heading, ['h2', 'p'], {'href': 'https://www.boot.dev'})", repr(node)) 

    def test_html_no_value(self):
        node = HTMLNode(tag="div", children=["h2", "p"], props={"href": "https://www.boot.dev"})
        self.assertEqual("HTMLNode(div, None, ['h2', 'p'], {'href': 'https://www.boot.dev'})", repr(node)) 

    def test_html_no_children(self):
        node = HTMLNode(tag="h1", value="This is a heading", props={"href": "https://www.boot.dev"})
        self.assertEqual("HTMLNode(h1, This is a heading, None, {'href': 'https://www.boot.dev'})", repr(node)) 

    def test_html_no_props(self):
        node = HTMLNode(tag="h1", value="This is a heading", children=["h2", "p"])
        self.assertEqual("HTMLNode(h1, This is a heading, ['h2', 'p'], None)", repr(node)) 
    
    def test_html_props_to_html1(self):
        node = HTMLNode(props={"href": "https://www.boot.dev", "target": "_blank"})
        self.assertEqual(' href="https://www.boot.dev" target="_blank"', node.props_to_html())

    def test_html_props_to_html2(self):
        node = HTMLNode(tag="h1", value="This is a heading")
        self.assertEqual("", node.props_to_html())

    # Leaf node tests

    def test_leaf_to_html_p(self):
        node = LeafNode(tag="p", value="Hello, World!")
        self.assertEqual("<p>Hello, World!</p>", node.to_html())

    def test_leaf_to_html_a(self):
        node = LeafNode(tag="a", value="", props={"href": "https://www.boot.dev", "target": "_blank"})
        self.assertEqual('<a href="https://www.boot.dev" target="_blank"></a>', node.to_html())

    def test_leaf_to_html_button(self):
        node = LeafNode(tag="btn", value="test", props={"href": "https://www.boot.dev"})
        self.assertEqual('<btn href="https://www.boot.dev">test</btn>', node.to_html())

    def test_leaf_no_tag(self):
        node = LeafNode(tag=None, value="test")
        self.assertEqual("test", node.to_html())

    def test_leaf_no_value(self):
        node = LeafNode(tag="b", value=None)
        with self.assertRaises(ValueError):
            node.to_html()

    # Parent node tests

    def test_to_html_with_children(self):
        child_node = LeafNode(tag="span", value="child")
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode(tag="b", value="grandchild")
        child_node = ParentNode(tag="span", children=[grandchild_node])
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_with_many_children(self):
        grandchild_node1 = LeafNode(tag="b", value="Bold text")
        grandchild_node2 = LeafNode(tag=None, value="Normal text")
        grandchild_node3 = LeafNode(tag="i", value="Italic text")
        grandchild_node4 = LeafNode(tag=None, value="Normal text")
        parent_node = ParentNode(tag="p", children=[grandchild_node1, grandchild_node2, grandchild_node3, grandchild_node4])
        self.assertEqual("<p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p>", parent_node.to_html())

    def test_to_html_with_multiple_paths(self):
        grandchild1_node1 = LeafNode(tag="p", value="p")
        grandchild1_node2 = LeafNode(tag="span", value="span")
        child1_node = ParentNode(tag="div", children=[grandchild1_node1, grandchild1_node2])
        grandchild2_node1 = LeafNode("span", value="span")
        grandchild2_node2 = LeafNode("p", value="p")
        child2_node = ParentNode(tag="div", children=[grandchild2_node1, grandchild2_node2])
        parent_node = ParentNode(tag="div", children=[child1_node, child2_node])
        self.assertEqual("<div><div><p>p</p><span>span</span></div><div><span>span</span><p>p</p></div></div>", parent_node.to_html())

    def test_to_html_with_no_children(self):
        parent_node = ParentNode(tag="p", children=None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_no_tag(self):
        child_node = LeafNode(tag="p", value="this should fail")
        parent_node = ParentNode(tag=None, children=[child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

if __name__ == "__main__":
    unittest.main()
