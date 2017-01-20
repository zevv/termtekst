
= NOS teletekst on the linux console

Small python app using curses to display dutch NOS teletekst on the linux
console. The original teletext font includes 2x6 raster graphics glyphs which
have no representation in unicode; as a workaround the braille set is abused to
approximate the graphics.

Usage: tt.py [page]

Key mappings:

````
left / j / [  : prev
right / l / ] : next
up / j / ,    : prev sub page
down / k / .  : next sub page
[0-9]         : enter page number
q             : quit
````

![Demo](/tt.png)

