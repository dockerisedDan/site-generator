import unittest

from blockparser import markdown_to_blocks

class TestBlockParser(unittest.TestCase):
    def test_block_splitting(self):
        markdown = "# This is a heading\n\n"
        markdown += "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.\n\n"
        markdown += "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        blocks = markdown_to_blocks(markdown)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
        ]
        self.assertListEqual(expected, blocks)

    def test_whitespace(self):
        markdown = """
        # This is a heading

        This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

        - This is the first list item in a list block
        - This is a list item
        - This is another list item
        """
        blocks = markdown_to_blocks(markdown)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n        - This is a list item\n        - This is another list item",
        ]
        self.assertListEqual(expected, blocks)

    def test_extra_lines(self):
        markdown = "# This is a heading\n\n"
        markdown += "\n\n"
        markdown += "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.\n\n"
        markdown += "\n\n"
        markdown += "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        blocks = markdown_to_blocks(markdown)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
        ]
        self.assertListEqual(expected, blocks)

    def test_uneven_newlines(self):
        markdown = "# This is a heading\n\n"
        markdown += "\n\n\n"
        markdown += "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.\n\n"
        markdown += "\n\n\n\n\n\n\n\n\n\n"
        markdown += "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        blocks = markdown_to_blocks(markdown)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
        ]
        self.assertListEqual(expected, blocks)

        
