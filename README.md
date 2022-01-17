
## NOS Teletekst on the Linux console

Small Python app using `curses` to display Dutch NOS Teletekst on the Linux
console. The original Teletekst font includes 2x6 raster graphics glyphs which
have no representation in unicode; as a workaround the braille set is abused to
approximate the graphics.

![Demo](/tt.png)

Pages are retrieved from NOS over HTTP (in JSON format).


### Installation

```
sudo python ./setup.py install
```

or simply run the script straight from the checked out git source:

```
./src/tt
```

### Usage

Termtekst takes an optional start page number as single argument, or defaults to page 100 if not specified:

```
tt [page]
```

Choos the page to view using number keys, browse using arrow keys or vim-style navigation (h,j,k,l), or click
on page numbers with the mouse.

### Key mappings

````
left  / h / [ : prev
right / l / ] : next
up    / j / , : prev sub page
down  / k / . : next sub page
[0-9]         : enter page number
q             : quit
d             : toggle double width
````

### Fonts

The teletext character set can (at this time) not be properly rendered as there is no valid representation for
some of the graphical characters in the unicode set. As a workaround, termtekst tries to approximate some
of these symbols by replacing them with characters from the braille unicode table. For better results,
install the 
[NOS teletekst font](https://cdn.nos.nl/assets/nos-symfony/bcea4a1/bundles/nossite/fonts/teletekst/Android_VeraMono.woff)
on your machine and set the `charset` option to `nos` in your `~/.ttrc`.


### Configuration

Termtekst allows for some basic configuration of bookmarks and rendering options through
a config file in `~/.ttrc`. Refer to the `example-ttrc` for a list of available options and settings.

