import unittest

from blockparser import BlockType, block_to_block_type, markdown_to_blocks

class TestBlockParser(unittest.TestCase):
    # Block splitting tests

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

    # Block type tests

    def test_headings(self):
        heading1 = "# This is heading 1"
        heading2 = "## This is heading 2"
        heading3 = "### This is heading 3"
        heading4 = "#### This is heading 4"
        heading5 = "##### This is heading 5"
        heading6 = "###### This is heading 6"
        block_type1 = block_to_block_type(heading1)
        block_type2 = block_to_block_type(heading2)
        block_type3 = block_to_block_type(heading3)
        block_type4 = block_to_block_type(heading4)
        block_type5 = block_to_block_type(heading5)
        block_type6 = block_to_block_type(heading6)
        self.assertEqual(BlockType.HEADING, block_type1)
        self.assertEqual(BlockType.HEADING, block_type2)
        self.assertEqual(BlockType.HEADING, block_type3)
        self.assertEqual(BlockType.HEADING, block_type4)
        self.assertEqual(BlockType.HEADING, block_type5)
        self.assertEqual(BlockType.HEADING, block_type6)

    def test_invalid_headings(self):
        bad_heading1 = "#This heading should fail"
        bad_heading2 = "####### This heading has too many #"
        block_type1 = block_to_block_type(bad_heading1)
        block_type2 = block_to_block_type(bad_heading2)
        self.assertNotEqual(BlockType.HEADING, block_type1)
        self.assertNotEqual(BlockType.HEADING, block_type2)

    def test_code_blocks(self):
        codeblock1 = "```This is a code block in one line\n```"
        codeblock2 = "```This is a code block\nthat uses 2 lines\n```"
        block_type1 = block_to_block_type(codeblock1)
        block_type2 = block_to_block_type(codeblock2)
        self.assertEqual(BlockType.CODE, block_type1)
        self.assertEqual(BlockType.CODE, block_type2)

    def test_bad_code_blocks(self):
        bad_codeblock1 = "```This code block is not closed"
        bad_codeblock2 = "This code block is not opened"
        bad_codeblock3 = "`This code block uses single ticks`"
        bad_codeblock4 = "```This code block doesn't use a newline```"
        block_type1 = block_to_block_type(bad_codeblock1)
        block_type2 = block_to_block_type(bad_codeblock2)
        block_type3 = block_to_block_type(bad_codeblock3)
        block_type4 = block_to_block_type(bad_codeblock4)
        self.assertNotEqual(BlockType.CODE, block_type1)
        self.assertNotEqual(BlockType.CODE, block_type2)
        self.assertNotEqual(BlockType.CODE, block_type3)
        self.assertNotEqual(BlockType.CODE, block_type4)

    def test_quotes(self):
        quote1 = ">This is a quote"
        quote2 = "> This is also a quote"
        quote3 = ">This is a quote\n>On multiple lines"
        quote4 = "> This quote also\n> Uses multiple lines"
        block_type1 = block_to_block_type(quote1)
        block_type2 = block_to_block_type(quote2)
        block_type3 = block_to_block_type(quote3)
        block_type4 = block_to_block_type(quote4)
        self.assertEqual(BlockType.QUOTE, block_type1)
        self.assertEqual(BlockType.QUOTE, block_type2)
        self.assertEqual(BlockType.QUOTE, block_type3)
        self.assertEqual(BlockType.QUOTE, block_type4)

    def test_bad_quotes(self):
        bad_quote1 = "This is not a quote"
        bad_quote2 = ">This is a quote\nWithout a >"
        bad_quote3 = "This quote is also\n>Missing the >"
        block_type1 = block_to_block_type(bad_quote1)
        block_type2 = block_to_block_type(bad_quote2)
        block_type3 = block_to_block_type(bad_quote3)
        self.assertNotEqual(BlockType.QUOTE, block_type1)
        self.assertNotEqual(BlockType.QUOTE, block_type2)
        self.assertNotEqual(BlockType.QUOTE, block_type3)

    def test_u_list(self):
        ulist1 = "- This is a ulist"
        ulist2 = "- This is a ulist\n- With 2 lines"
        block_type1 = block_to_block_type(ulist1)
        block_type2 = block_to_block_type(ulist2)
        self.assertEqual(BlockType.ULIST, block_type1)
        self.assertEqual(BlockType.ULIST, block_type2)

    def test_bad_u_list(self):
        bad_ulist1 = "-This list is missing a space"
        bad_ulist2 = "- This list is\nMissing a - in the second line"
        bad_ulist3 = "This list is\n- Missing a - in the first line"
        bad_ulist4 = "- This list is\n-Missing the space on line 2"
        block_type1 = block_to_block_type(bad_ulist1)
        block_type2 = block_to_block_type(bad_ulist2)
        block_type3 = block_to_block_type(bad_ulist3)
        block_type4 = block_to_block_type(bad_ulist4)
        self.assertNotEqual(BlockType.ULIST, block_type1)
        self.assertNotEqual(BlockType.ULIST, block_type2)
        self.assertNotEqual(BlockType.ULIST, block_type3)
        self.assertNotEqual(BlockType.ULIST, block_type4)

    def test_o_list(self):
        olist1 = "1. This is an o list"
        olist2 = "1. This is an o list\n2. With multiple lines"
        block_type1 = block_to_block_type(olist1)
        block_type2 = block_to_block_type(olist2)
        self.assertEqual(BlockType.OLIST, block_type1)
        self.assertEqual(BlockType.OLIST, block_type2)

    def test_bad_o_list(self):
        bad_olist1 = "2. This o list doesn't start at 1"
        bad_olist2 = "1. This o list\nIs missing the second number"
        bad_olist3 = "This o list\n 2. Is missing the first number"
        bad_olist4 = "1.This o list is missing a space"
        block_type1 = block_to_block_type(bad_olist1)
        block_type2 = block_to_block_type(bad_olist2)
        block_type3 = block_to_block_type(bad_olist3)
        block_type4 = block_to_block_type(bad_olist4)
        self.assertNotEqual(BlockType.OLIST, block_type1)
        self.assertNotEqual(BlockType.OLIST, block_type2)
        self.assertNotEqual(BlockType.OLIST, block_type3)
        self.assertNotEqual(BlockType.OLIST, block_type4)

    def test_paragraph(self):
        paragraph1 = "This is a paragraph"
        paragraph2 = "This is a pragraph\nWith 2 lines"
        block_type1 = block_to_block_type(paragraph1)
        block_type2 = block_to_block_type(paragraph2)
        self.assertEqual(BlockType.PARAGRAPH, block_type1)
        self.assertEqual(BlockType.PARAGRAPH, block_type2)
