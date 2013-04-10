import os
import json

class Config(object):
    def __init__(self, base_dir):
        self._base_dir = base_dir
        self._config(base_dir, {})

    def _config(self, base_dir, config_dict):
        self._base_dir = base_dir
        self._input_dir = os.path.join(base_dir, os.path.expanduser(config_dict.get('input_dir', "content/")))
        self._output_dir = os.path.join(base_dir, os.path.expanduser(config_dict.get('output_dir', "site/")))
        self._theme_dir = os.path.join(base_dir, os.path.expanduser(config_dict.get('theme_dir', "theme/")))
        self._static_dir = os.path.join(base_dir, os.path.expanduser(config_dict.get('static_dir', "static/")))
        self._site_name = config_dict.get('site_name', "Vortex Site")
        self._pygments_style = config_dict.get('pygments_style', "solarized")
        self._site_url = config_dict.get('site_url', "localhost")

    def config_from_file(self, f):
        config_dict = json.load(f)
        self._config(config_dict.get('base_dir', self._base_dir), config_dict)

    def config_from_string(self, s):
        config_dict = json.loads(s)
        self._config(config_dict.get('base_dir', self._base_dir), config_dict)

    def config_from_dict(self, config_dict):
        self._config(config_dict.get('base_dir', self._base_dir), config_dict)

    @property
    def sidebar_file(self):
        return os.path.join(self.input_dir, "sidebar.md")

    @property
    def colophon_file(self):
        return os.path.join(self.input_dir, "colophon.md")

    @property
    def colophon_output_dir(self):
        return os.path.join(self.output_dir, "colophon/")

    @property
    def colophon_output_file(self):
        return os.path.join(self.colophon_output_dir, "index.html")

    @property
    def css_filename(self):
        return "pygments-style.css"

    @property
    def css_output_path(self):
        return os.path.join(self.output_dir, self.css_filename)

    @property
    def css_web_path(self):
        return os.path.join("/", self.css_filename)

    @property
    def images_output_dir(self):
        return os.path.join(self.output_dir, "images")

    @property
    def articles_input_dir(self):
        return os.path.join(self.input_dir, "articles")

    def article_output_dir(self, slug, is_draft=False):
        if is_draft:
            dirname = "drafts"
        else:
            dirname = "articles"
        return os.path.join(self.output_dir, os.path.join(dirname, slug))

    def article_file(self, slug, is_draft=False):
        return os.path.join(self.article_output_dir(slug, is_draft), "index.html")

    def article_web_path(self, slug):
        return os.path.join("/articles", slug)

    def index_output_dir(self, index_num):
        if index_num == 1:
            return self.output_dir
        else:
            return os.path.join(self.output_dir, "%d/" % index_num)

    def index_file(self, index_num):
        return os.path.join(self.index_output_dir(index_num), "index.html")

    @property
    def rss_file(self):
        return os.path.join(self.output_dir, "rss.xml")

    @property
    def input_dir(self):
        return self._input_dir

    @property
    def output_dir(self):
        return self._output_dir

    @property
    def template_dir(self):
        return os.path.join(self._theme_dir, "templates/")

    @property
    def theme_static_dir(self):
        return os.path.join(self._theme_dir, "static/")

    @property
    def static_dir(self):
        return self._static_dir

    @property
    def site_name(self):
        return self._site_name

    @property
    def site_url(self):
        return self._site_url

    @property
    def pygments_style(self):
        return self._pygments_style
