import unittest
from gencontent import extract_heading

class TestExtractTitle(unittest.TestCase):
    def test_extract_heading_only(self):
        md = "# This is a heading"
        heading = extract_heading(md)
        expected = "This is a heading"
        self.assertEqual(expected, heading)
        
    def test_extract_heading_from_blocks(self):
        md = "# This is the heading\n"
        md += "\n"
        md += "```\nThis is a code block\nover a few lines\n```\n"
        md += "\n"
        md += "This is some text"
        heading = extract_heading(md)
        expected = "This is the heading"
        self.assertEqual(expected, heading)

    def test_extract_heading_with_subheadings(self):
        md = "# This is the main heading\n"
        md += "\n"
        md += "This is a paragraph\n"
        md += "\n"
        md += "## This is the subheading\n"
        md += "\n"
        md += "This is the subheading paragraph\n"
        heading = extract_heading(md)
        expected = "This is the main heading"
        self.assertEqual(expected, heading)

    def test_extract_heading_under_subheading(self):
        md = "## This is a subheading\n"
        md += "\n"
        md += "# This is a heading\n"
        heading = extract_heading(md)
        expected = "This is a heading"
        self.assertEqual(expected, heading)
