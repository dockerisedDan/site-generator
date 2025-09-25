import unittest
from textnode import TextNode, TextType
from textparser import split_nodes_delimiter


class TestTextParser(unittest.TestCase):
    def test_delim_bold(self):
        node =  TextNode("This is text with a **bolded** word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_delim_bold_double(self):
        node = TextNode("This is text with a **bolded** word and **another**", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word and ", TextType.PLAIN),
            TextNode("another", TextType.BOLD),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_delim_bold_multiword(self):
        node = TextNode("This is text with a **bolded word** and **another**", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("bolded word", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("another", TextType.BOLD),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_delim_italic(self):
        node = TextNode("This is text with an __italic__ word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "__", TextType.ITALIC)
        expected = [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_delim_bold_and_italic(self):
        node = TextNode("**Bold** and __italic__", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "__", TextType.ITALIC)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertListEqual(new_nodes, expected)
