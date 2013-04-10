import datetime
import os
import re

import typogrify.filters
import Image

import config

def image_filter(html):
    imgRE = re.compile("<img (.+?)/>")
    srcRE = re.compile("src=\"(.+?)\"")

    wrappedImgRE = re.compile("<p>((<a.+?>)?<img (.+?)/>(</a>)?)</p>")
    titleRE = re.compile("title=\"(.+?)\"")

    # right now we don't need this, since images are fluid
    # leave it in though, in case it needs to be an option
    #def size_add(mo):
    #    contents = mo.group(1)
    #    srcMO = srcRE.search(contents)
    #    if not srcMO:
    #        return mo.group(0)
    #    src = srcMO.group(1)
    #    im = Image.open(os.path.join(cfg.output_dir, src[1:]))
    #    return "<img %s width=\"%d\" height=\"%d\">" % (mo.group(1), im.size[0], im.size[1])

    #ret = imgRE.sub(size_add, html)
    ret = html

    def title_add(mo):
        #filters = [ typogrify.filters.amp, typogrify.filters.smartypants, typogrify.filters.caps ]
        contents = mo.group(3)
        titleMO = titleRE.search(contents)
        if not titleMO:
            return mo.group(0)
        title = titleMO.group(1)
        #title = reduce(lambda h, f: f(h), filters, title)
        return "<div class=\"image\">%s<br/><p class=\"caption\">%s</p></div>" % (mo.group(1), title)

    return wrappedImgRE.sub(title_add, ret)

class MarkdownDocument(object):
    filters = [ image_filter, typogrify.filters.amp, typogrify.filters.smartypants, typogrify.filters.caps ]

    def __init__(self, markdown_file, parser):
        self._filename = markdown_file
        with open(markdown_file) as f:
            text = f.read()
        html = parser.convert(text)
        self._html = reduce(lambda h, f: f(h), self.filters, html)
        self._metadata = self._filter_metadata(parser.Meta)
        parser.reset()

    def _filter_metadata(self, metadata_orig):
        return { k.lower(): str(v[0]) for k, v in metadata_orig.iteritems() }

    @property
    def html(self):
        return self._html

    @property
    def metadata(self):
        return self._metadata

class Sidebar(MarkdownDocument):
    def __init__(self, markdown_file, parser):
        super(Sidebar, self).__init__(markdown_file, parser)

    def generate_sidebar_html(self, template, articles, cfg):
        return template.generate(sidebar=self, articles=articles, config=cfg)

class Colophon(MarkdownDocument):
    def __init__(self, markdown_file, parser):
        super(Colophon, self).__init__(markdown_file, parser)

    def generate_html_file(self, template, cfg, sidebar_html):
        generated_html = template.generate(content=self.html, sidebar_html=sidebar_html, pygments_cssfilename=cfg.css_web_path, config=cfg)

        # process html to put captions on images
        #generated_html = image_filter(generated_html, cfg)

        output_dir = cfg.colophon_output_dir
        try:
            os.makedirs(output_dir)
        except OSError:
            # already exists, ignore
            pass
        with open(cfg.colophon_output_file, 'w') as f:
            f.write(generated_html)
            f.flush()

class Article(MarkdownDocument):
    # TODO: make author and slug optional; have a site default author, and do lower->space-to-hypen transform on the title for slug
    required_metadata = [ "title", "timestamp", "author", "slug", "status" ]

    def __init__(self, markdown_file, parser):
        super(Article, self).__init__(markdown_file, parser)
        self._check_required_metadata(self.metadata)

        self._title = self.metadata['title']
        self._author = self.metadata['author']
        self._slug = self.metadata['slug']
        self._article = self.metadata['status'].lower() == 'article'
        self._timestamp = datetime.datetime.strptime(self.metadata['timestamp'], "%d-%m-%Y %H:%M")

        # make a summary: take the first paragraph; knock any h1's down to h2's so they don't conflict with the title
        self._summary_html = self.html[0:self.html.find("</p>") + len("</p>")]
        self._summary_html = self._summary_html.replace("h1>", "h2>")

    def _check_required_metadata(self, metadata):
        for field in self.required_metadata:
            if field not in metadata:
                raise KeyError("Article in file '%s' missing metadata field '%s'" % (self._filename, field.title()))

    def generate_html_file(self, template, cfg, sidebar_html):
        generated_html = template.generate(article=self, sidebar_html=sidebar_html, pygments_cssfilename=cfg.css_web_path)

        # process html to put captions on images
        #generated_html = image_filter(generated_html, cfg)

        output_dir = cfg.article_output_dir(self.slug, not self.is_article)
        try:
            os.makedirs(output_dir)
        except OSError:
            # already exists, ignore
            pass
        with open(cfg.article_file(self.slug, not self.is_article), 'w') as f:
            f.write(generated_html)
            f.flush()

    @property
    def summary_html(self):
        return self._summary_html

    @property
    def title(self):
        return self._title

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def timestamp_str(self):
        return self._timestamp.strftime("%H:%M %B %d, %Y")

    @property
    def author(self):
        return self._author

    @property
    def slug(self):
        return self._slug

    @property
    def is_article(self):
        return self._article

def articles_from_directory(markdown_directory, parser):
    return [ Article(os.path.join(markdown_directory, f), parser) for f in os.listdir(markdown_directory) if f.endswith(".md") ]
