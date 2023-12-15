# THELPER

#### The Helper that helps doing the boring stuff.

#### Installation

##### OS

Recommended: Ensure a suitable environment manager for python envs (e.g.  [Anaconda](https://www.anaconda.com/products/individual)).

Installation with Anaconda:

*Windows*: execute `install.bat`

*Linux*: `./install_local.sh -i`

##### Pip

To install via pip:

```
pip install git+https://github.com/tna76874/thelper.git
```

You might add the templates in the corresponding folder `~/.config/thelper` manually.

##### Docker

```bash
./build.sh

./run.sh
```

#### Podman

Installing:

```
curl -sL https://raw.githubusercontent.com/tna76874/thelper/main/install_podman.sh | bash
```

Running: `thelper`

#### Usage

```bash
usage: thelper [-h] [--confdir CONFDIR] [-t T] [-d D] [-r]

optional arguments:
  -h, --help         show this help message and exit
  --confdir CONFDIR  path to config dir
  -t T               template category e.g. default
  -d D               default template category e.g. default
  -r                 render latex templates
```

Render all template files from config directory.
First it will be tried to render from the selected template category.

Example:
├── config.ini
└── templates
├── blank
│   ├── content.tex.j2
│   └── meta.tex.j2
└── default
├── content.tex.j2
├── document.tex.j2
├── main.py.j2
├── meta.tex.j2
└── thelper.sty.j2

If selected 'blank' as template category it will render 'content.tex.j2'
and 'meta.tex.j2'. For the other templates it will fallback to the
template category 'default'.
