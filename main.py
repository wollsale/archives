import os
import shutil
import sass
from markdown2 import markdown
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('_templates'))
tag_template = env.get_template('tag.html')
post_template = env.get_template('post.html')
feed_template = env.get_template('core-feed.html')

def removeDir(dirPath):
  if os.path.isdir(dirPath):
    try:
      shutil.rmtree(dirPath)
    except OSError as e:
      print ("Error: %s - %s." % (e.filename, e.strerror))

def copyDirectory(src, dest):
    try:
        shutil.copytree(src, dest)
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    except OSError as e:
        print('Directory not copied. Error: %s' % e)

# Remove dist/
removeDir('./dist/')

# Prepare posts and tags
distDir = './dist/'
publicDir = './'
publicPostDir = publicDir + 'posts/'
POSTS = []
TAGS = set()

# Loop through content
for md_post in os.listdir('_content/posts'):
    file_path = os.path.join('_content/posts', md_post)
    with open(file_path, 'r') as file:
        raw_post = markdown(
            file.read(),
            extras=['metadata', 'code-friendly']
        )
        post_data = {
          'title' : raw_post.metadata['title'],
          'tags' : [tag.strip() for tag in raw_post.metadata['tags'].split(",")],
          'slug' : publicPostDir + raw_post.metadata['slug'],
          'poster' : publicDir + raw_post.metadata['poster'],
          'content' : raw_post
        }
        POSTS.append(post_data)
        for tag in post_data['tags']:
            TAGS.add(tag.strip())

# Loop through tags
for tag in TAGS:
    posts = []
    for post in POSTS:
        if tag in post['tags']:
            posts.append(post)
    tag_html = tag_template.render(tag=tag, posts=posts)
    tag_file_path = 'dist/tag-{tag}.html'.format(tag=tag.lower())
    os.makedirs(os.path.dirname(tag_file_path), exist_ok=True)

    with open(tag_file_path, 'w') as file:
        file.write(tag_html)

# Build posts
for post in POSTS:
    post_html = post_template.render(post=post)
    post_file_path = 'dist/{slug}.html'.format(slug=post['slug'])
    os.makedirs(os.path.dirname(post_file_path), exist_ok=True)

    with open(post_file_path, 'w') as file:
        file.write(post_html)

# Build feed
feed_html = feed_template.render(posts=POSTS)
feed_file_path = 'dist/core-feed.html'
os.makedirs(os.path.dirname(feed_file_path), exist_ok=True)
with open(feed_file_path, 'w') as file:
    file.write(feed_html)

# Copy and move medias folder
# TO-DO : process all medias with compressor
copyDirectory('./_content/medias/', './dist/medias')

# SCSS
# https://sass.github.io/libsass-python/frameworks/flask.html#directory-layout
sass.compile(dirname=('./', './dist/'), output_style='compressed')
