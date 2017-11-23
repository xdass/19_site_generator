import jinja2
import markdown


def open_markdown_file(markdown_file):
    pass


def load_json_config(json_file):
    pass


with open('articles/0_tutorial/8_cli.md', 'r', encoding='utf-8') as f:
    text = f.read()
html = markdown.markdown(text)
print(html)

with open('test.html', 'w') as fp:
    fp.write(html)