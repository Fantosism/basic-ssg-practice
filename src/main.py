from textnode import TextNode, TextType

def main():
    print(TextNode("This is some anchor text", TextType.ANCHOR_TEXT, 'https://www.boot.dev'))

if __name__ == "__main__":
    main()
