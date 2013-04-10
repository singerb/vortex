# vortex

Python static site generator with a solarized-inspired theme.

A list of required packages (use virtualenv) is included, as is an example site that uses the included theme.

## Usage

```
usage: vortex.py [-h] [-c CONFIG] [-d]

optional arguments:
    -h, --help            show this help message and exit
    -c CONFIG, --config CONFIG
                          The config file to use; default 'default-config.json'
    -d, --dev-server      Run a simple webserver after generating the site, for
                          development testing; default 'False'
```

For development usage, run it with `-d` to run a basic webserver on the generated site; for production usage, just run it with the config. Everything else is controlled by the config; see the example-config.json or config.py files for the elements involved.

## Further info

The example site included has an article that demonstrates all of the layout and design decisions made in the theme.
