from textnode import TextNode, TextType


def main():
    test_node = TextNode("This is some anchor text", TextType.LINK, "http://www.boot.dev")
    print(test_node)


main()
