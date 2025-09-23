import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_all_values(self):
        node = HTMLNode(tag="h1", value="This is a heading", children=["h2", "p"], props={"href": "https://www.boot.dev"})
        self.assertEqual("HTMLNode(h1, This is a heading, ['h2', 'p'], {'href': 'https://www.boot.dev'})", repr(node))

    def test_no_tag(self):
        node = HTMLNode(value="This is a heading", children=["h2", "p"], props={"href": "https://www.boot.dev"})
        self.assertEqual("HTMLNode(None, This is a heading, ['h2', 'p'], {'href': 'https://www.boot.dev'})", repr(node)) 

    def test_no_value(self):
        node = HTMLNode(tag="div", children=["h2", "p"], props={"href": "https://www.boot.dev"})
        self.assertEqual("HTMLNode(div, None, ['h2', 'p'], {'href': 'https://www.boot.dev'})", repr(node)) 

    def test_no_children(self):
        node = HTMLNode(tag="h1", value="This is a heading", props={"href": "https://www.boot.dev"})
        self.assertEqual("HTMLNode(h1, This is a heading, None, {'href': 'https://www.boot.dev'})", repr(node)) 

    def test_no_props(self):
        node = HTMLNode(tag="h1", value="This is a heading", children=["h2", "p"])
        self.assertEqual("HTMLNode(h1, This is a heading, ['h2', 'p'], None)", repr(node)) 
    
    def test_props_to_html1(self):
        node = HTMLNode(props={"href": "https://www.boot.dev", "target": "_blank"})
        self.assertEqual(' href="https://www.boot.dev" target="_blank"', node.props_to_html())

    def test_props_to_html2(self):
        node = HTMLNode(tag="h1", value="This is a heading")
        self.assertEqual("", node.props_to_html())

if __name__ == "__main__":
    unittest.main()
