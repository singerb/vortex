import functools
import operator
import argparse
import os
import shutil
import SimpleHTTPServer
import SocketServer
import datetime

import markdown
import pygments.formatters
import tornado.template
import Image
import PyRSS2Gen

import article
import config

class Vortex(object):
    def __init__(self, config):
        self._config = config

    def generate_site(self):
        # load the markdown parser and pygments formatter
        parser = markdown.Markdown(['extra', 'meta', 'codehilite(css_class=highlight, force_linenos=False, guess_lang=False)'])
        formatter = pygments.formatters.HtmlFormatter(cssclass='highlight', style=self._config.pygments_style, linenos='table')

        # load all the templates we need from the template dir
        loader = tornado.template.Loader(self._config.template_dir, autoescape=None)
        article_template = loader.load('article.html')
        sidebar_template = loader.load('sidebar.html')
        colophon_template = loader.load('colophon.html')
        index_template = loader.load('index.html')

        # get lists of article and drafts objects from their markdown files
        content_unsorted = article.articles_from_directory(self._config.articles_input_dir, parser)
        articles_unsorted = [ a for a in content_unsorted if a.is_article ]
        drafts = [ a for a in content_unsorted if not a.is_article ]

        # sort articles by timestamp, most recent first
        articles = sorted(articles_unsorted, key=operator.attrgetter('timestamp'), reverse=True)

        # build the html for the sidebar using the most recent 5 articles
        sidebar = article.Sidebar(self._config.sidebar_file, parser)
        sidebar_html = sidebar.generate_sidebar_html(sidebar_template, articles[0:min(5, len(articles))], self._config)

        # build the colophon page
        colophon = article.Colophon(self._config.colophon_file, parser)
        colophon.generate_html_file(template=colophon_template, cfg=self._config, sidebar_html=sidebar_html)

        # generate the pygments css file
        css = formatter.get_style_defs('.highlight')
        with open(self._config.css_output_path, 'w') as cssfile:
            cssfile.write(css)

        # now copy over static assets, from the theme and the site
        for f in os.listdir(self._config.theme_static_dir):
            shutil.copy(os.path.join(self._config.theme_static_dir, f), os.path.join(self._config.output_dir, f))
        for f in os.listdir(self._config.static_dir):
            shutil.copy(os.path.join(self._config.static_dir, f), os.path.join(self._config.output_dir, f))

        # now copy all .jpg, .png files found in articles dir to the images directory
        # additionally, copy foo.jpg -> foo@2x.jpg, and use PIL to generate foo.jpg from it
        # this assumes all images over 2000px in one dimension are retina ready
        try:
            os.makedirs(self._config.images_output_dir)
        except OSError:
            # already exists, ignore
            pass
        for f in os.listdir(self._config.articles_input_dir):
            r, e = os.path.splitext(f)
            if e in [".jpg", ".png"]:
                src = os.path.join(self._config.articles_input_dir, f)
                dest = os.path.join(self._config.images_output_dir, "%s@2x%s" % (r, e))
                small_dest = os.path.join(self._config.images_output_dir, f)

                im = Image.open(dest)

                if im.size[0] > 2000 or im.size[1] > 2000:
                    shutil.copy(src, dest)
                    new_size = (im.size[0] / 2, im.size[1] / 2)
                    im = im.resize(new_size, Image.ANTIALIAS)
                    im.save(small_dest, quality=90)
                else:
                    shutil.copy(src, small_dest)

        # tell all the articles to generate themselves
        # TODO links to next prev?
        gen_func = functools.partial(article.Article.generate_html_file, template=article_template, cfg=self._config, sidebar_html=sidebar_html)
        map(gen_func, articles)

        # tell all the drafts to generate themselves
        map(gen_func, drafts)

        # now build the index pages, 5 articles at a time
        max_index_num = (len(articles) / 5) + 1
        for i in range(0, len(articles), 5):
            articles_slice = articles[i:min(i + 5, len(articles))]
            index_num = ((i + 1) / 5) + 1

            index_html = index_template.generate(config=self._config, articles=articles_slice, sidebar_html=sidebar_html, pygments_cssfilename=self._config.css_web_path, index_num=index_num, max_index_num=max_index_num)
            index_html = article.image_filter(index_html)

            output_dir = self._config.index_output_dir(index_num)
            try:
                os.makedirs(output_dir)
            except OSError:
                # already exists, ignore
                pass
            with open(self._config.index_file(index_num), 'w') as f:
                f.write(index_html)
                f.flush()

        # now build the RSS feed
        base_url = "http://%s" % (self._config.site_url)
        rss_items = [ PyRSS2Gen.RSSItem(title=a.title, link="%s%s" % (base_url, self._config.article_web_path(a.slug)), guid=self._config.article_web_path(a.slug), description=a.html, pubDate=a.timestamp) for a in articles ]
        rss = PyRSS2Gen.RSS2(title=self._config.site_name, link=base_url, description="RSS feed for %s" % (self._config.site_name), lastBuildDate=datetime.datetime.now(), items=rss_items)

        with open(self._config.rss_file, 'w') as f:
            rss.write_xml(f)

class MyServer(SocketServer.TCPServer):
    """Basic server that allows address reuse, for ease of development."""

    allow_reuse_address = True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="The config file to use; default '%(default)s'", default="default-config.json")
    parser.add_argument("-d", "--dev-server", help="Run a simple webserver after generating the site, for development testing; default '%(default)s'", action='store_true')

    args = parser.parse_args()

    # find the config file directory; relative paths in the config file should be resolved relative to that
    config_dir = os.path.dirname(os.path.abspath(args.config))

    cfg = config.Config(config_dir)
    cfg.config_from_file(open(args.config))

    generator = Vortex(cfg)
    generator.generate_site()
    print "Generated the '%s' site" % (cfg.site_name)

    if args.dev_server:
        os.chdir(cfg.output_dir)
        Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

        httpd = MyServer(("", 8000), Handler)
        httpd.allow_reuse_address = True

        print "Serving at port %d" % (8000,)
        httpd.serve_forever()
