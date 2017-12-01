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


def load_json_config(file_path):
    try:
        with open(file_path, encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return None


def create_articles_catalog(articles, path):
    topics_info = defaultdict(list)
    for article in articles:
        html_file_path = generate_path_to_html(path['html_articles'], article['source'])
        md_file_path = generate_path_to_md(path['md_articles'], article['source'])
        html = convert_markdown_to_html(md_file_path)
        topics_info[article['topic']].append([article['title'], html_file_path])
        create_html_page(html, article['title'], html_file_path)
    return topics_info


def generate_path_to_md(md_articles_dir, md_article_path):
    path_to_md_file = os.path.join(
        md_articles_dir,
        md_article_path
    )
    return path_to_md_file


def generate_path_to_html(html_articles_dir, html_article_path):
    path_to_html_file = os.path.join(
        html_articles_dir,
        html_article_path.replace('.md', '.html')
    )
    return path_to_html_file


def create_site_structure(articles):
    try:
        for article in articles:
            dirs_path = os.path.split(article['source'])[0]
            os.makedirs(os.path.join('topics', dirs_path), exist_ok=True)
    except FileExistsError:
        pass


def create_html_page(html, title, html_file_path):
    page_template = env.get_template('template.html')
    html_page = page_template.render({'html': html, 'title': title})
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(html_page)


def create_index_page(articles_info, topics):
    index_template = env.get_template('index-template.html')
    html = index_template.render({'title': 'Энциклопедия', 'articles': articles_info, 'topics': topics})
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(html)


def make_site():
    site_config = load_json_config('config.json')
    articles = site_config['articles']
    topics = site_config['topics']
    paths = site_config['paths']
    create_site_structure(articles)
    articles_info = create_articles_catalog(articles, paths)
    create_index_page(articles_info, topics)

if __name__ == '__main__':
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('templates')
    )
    make_site()
    server = Server()
    server.watch('articles/**/*.md', make_site)
    server.serve(root='')
