import os
import json
from collections import defaultdict
import jinja2
import markdown
from livereload import Server


def convert_markdown_to_html(markdown_file):
    with open(markdown_file, 'r', encoding='utf-8') as f:
        text = f.read()
    html = markdown.markdown(text)
    return html


def load_json_config(json_file):
    try:
        with open('config.json', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return None


def create_articles_catalog(site_config):
    topics = defaultdict(list)
    for article in site_config['articles']:
        html_file_path, md_file_path = create_paths(article)
        html = convert_markdown_to_html(md_file_path)
        topics[article['topic']].append([article['title'], html_file_path])
        create_html_page(html, article['title'], html_file_path)
    return topics


def create_paths(article_info):
    path_to_md_file = os.path.join(
        config['paths']['md_articles'],
        article_info['source']
    )
    path_to_html_file = os.path.join(
        config['paths']['html_articles'],
        article_info['source'].replace('.md', '.html'),
    )
    return path_to_html_file, path_to_md_file


def create_site_structure():
    try:
        for article in config['articles']:
            dirs_path = os.path.split(article['source'])[0]
            os.makedirs(os.path.join('topics', dirs_path), exist_ok=True)
    except FileExistsError:
        pass


def create_html_page(html, title, html_file_path):
    page_template = env.get_template('template.html')
    html_page = page_template.render({'html': html, 'title': title})
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(html_page)


def create_index_page(dd, topics_conf):
    index_template = env.get_template('index-template.html')
    html = index_template.render({'title': 'Энциклопедия', 'articles': dd, 'topics': topics_conf})
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(html)


def make_site():
    pass

if __name__ == '__main__':
    # server = Server()
    # server.watch('articles/*.md', make_site)
    # server.serve(root='topics/')  # folder to serve html files from
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('templates')
    )
    env.globals['static'] = os.getcwd()

    site_config = load_json_config('')
    create_site_structure()
    topics_info = create_articles_catalog(site_config)
    create_index_page(topics_info)
