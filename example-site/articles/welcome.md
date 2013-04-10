Title: Welcome To Vortex
Author: Benedict Singer
Slug: welcome-to-vortex
Timestamp: 26-2-2013 17:30
Status: article

# Introduction

This article is intended both as an introduction to the default Vortex style, and to the features of Vortex that enable that style. Examples of all the elements that Vortex and its style were designed for are present, which also makes this a useful development test. The basic building blocks of Vortex are [Markdown][] via [Python Markdown][] and [tornado][]'s templating system. Articles, drafts, the sidebar, and the about page are all written in Markdown format; they are then processed into HTML which is inserted into templates to build article pages and index pages. Theming is purely the responsibility of the templates and the CSS.

A site is composed of four elements, appropriately represented by the four templates in the theme: index pages, article pages (and draft pages), a sidebar, and a colophon page. All pages contain the sidebar, which is generated using the 5 most recent articles, the sidebar Markdown file, and the sidebar template. While it's called a sidebar, all that vortex expects is that each page needs a copy of it; it is up to theme via the templates & CSS how it is layed out and positioned. The vortex theme uses it as a right sidebar, but it could be done as a header, footer, left sidebar, or anything else you can think of. Article pages are generated from article Markdown files, and get a copy of the sidebar HTML to place in their template. Drafts are generated in the same way as articles, but are not included in the index or the five articles in the sidebar. Index pages are then generated from the articles, using an automatic summary (up to the end of the first paragraph in the article, with any `h1` elements demoted to `h2`). The colophon page is generated like the article pages, from its Markdown file and template, but is not included on index pages. Static files from the theme are also placed in the generated site, and image files in the articles directory are copied to an images directory in the generated site, and processed as discussed below. An RSS 2.0 XML file is also generated and placed in `rss.xml` in the site root; the feed contains the full article HTML as it appears on the page.

All locations are controlled by the configuration file, which is written in JSON format. Available variables are:

* `input_dir`: the location for all input Markdown documents. Vortex will look for `sidebar.md` and `colophon.md` in this directory, and articles, drafts, and images in an `articles/` sub-directory of this directory.
* `output_dir`: the web root for the output site.
* `theme_dir`: the location for all theme files. Vortex will look for two subdirectories here, `templates/` and `static/`; Vortex will look for `index.html`, `article.html`, `sidebar.html`, and `colophon.html` in the `templates/` directory, and theme static files in the `static/` directory (CSS, JS, fonts, etc). The content in the static directory will be copied to the `output_dir`.
* `static_dir`: the location for all site-specific static content. Vortex will copy all of this content to the `output_dir`; place site-specific static files like favicons, and `robots.txt` here, for example.
* `site_name`: Vortex will use this on index and colophon pages in the vortex theme.
* `pygments_style`: The name of the pygments style to use for code highlighting; it must be accessible to the pygments installtion.

# Style Examples

## Paragraphs

Paragraphs have no initial indent, while following paragraphs are indented and leave no blank line between themselves and the preceeding paragraph.

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## Lists

Lists have customized bullets via CSS, but are otherwise normal.

* Here's a list item
* And another list item

## Code

Code is highlighted via the [pygments][] module, using the style specified in the config file. The Vortex theme uses a [Solarized Light][] style to match the other page elements. Markdown is responsible for invoking pygments via the code-hilite extension; language guessing is turned off, so the language must be specified: `:::python` for example. For smaller viewports, the code blocks will line wrap, so line numbers are turned off.

    :::python
    def readStdin():
        """Read a line off stdin, and return it stripped. Raise EOFError on EOF."""
        line = stdin.readline()
        if line == "":
            raise EOFError
        return line.strip()

## Other Typographic Elements

Several [typogrify][] filters are run on the output: caps, amp, and smartypants. Example abbreviations that benefit from this: HTML, CSS (only one of them is defined, to show the style difference).

*[HTML]: Hyper Text Markup Language

Links have the usual treatment applied: underline on hover only, set in a contrasting color. Line heights and margins are set based on The Elements of Typographic Style, via the [web adaptation][typographic-style]. Heading sizes are also styled and controlled. For example:

### Sub-sub head

Nothing to see here.

#### Sub-sub-sub head

Nothing to see here.

## Images

Images are assumed by Vortex to be retina-ready, that is, the provided image is the 2x version; a 1x version is generated during site generation using [PIL][]. However, since images are presented in a fluid fashion in the default theme (`max-width: 100%`), the width and height do not get specified. Theoretically, the high resolution version could be served to all clients, but in the interests of bandwidth, they are not. [Retina.js][] is included in the templates to swap the high resolution images in for clients that will benefit. In addition to the standard Markdown treatment, the HTML is post-processed to take the `title` attribute from the image and create a caption below the image, as seen in the following image of a different kind of tornado. Note that this works even with a link around the image.

[![tornado](/images/tornado.jpg "Tornado, by TruckinTim on Flickr, CC BY-NC-ND")][tornado-flickr]

# Conclusion

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

[pygments]: http://pygments.org
[solarized light]: http://ethanschoonover.com/solarized
[typogrify]: https://github.com/mintchaos/typogrify
[typographic-style]: http://www.webtypography.net
[tornado-flickr]: http://www.flickr.com/photos/truckintim/3171794580/
[markdown]: http://daringfireball.net/projects/markdown/
[python markdown]: http://packages.python.org/Markdown/
[tornado]: http://www.tornadoweb.org/
[pil]: http://www.pythonware.com/products/pil/index.htm
[retina.js]: http://retinajs.com
