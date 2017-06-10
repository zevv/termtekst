
## NOS Teletekst on the Linux console

Small Python app using `curses` to display Dutch NOS Teletekst on the Linux
console. The original Teletekst font includes 2x6 raster graphics glyphs which
have no representation in unicode; as a workaround the braille set is abused to
approximate the graphics.

Pages are retrieved from NOS over HTTP (in JSON format).

Installation:

```
sudo python ./setup.py install
```

Usage:

```
tt [page]
```
Key mappings:

````
left  / h / [ : prev
right / l / ] : next
up    / j / , : prev sub page
down  / k / . : next sub page
[0-9]         : enter page number
q             : quit
````

![Demo](/tt.png)

