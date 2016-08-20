Less Annoying LaTeX
=========
Quick and easy LaTeX typesetting for the lazy. When having a nicely-formatted document isn't a priority. (e.g. taking notes, doing assignments, making crib sheets)

For example, using LaL, you can compile a .tex file that looks like this:
```
Hello, world!
$x = 3$
```
(note the absence of nonsense like `\begin{document}` etc.)

How to use
---------
There is only one file, **lal.py**.

To compile a .tex file "myfile.tex", run `python lal.py myfile.tex`.

This will generate a file `myfile.pdf`.

Requirements
---------
* Python 3
* pdflatex (added to path)

Arguments
---------
#### `python lal.py <OPTIONS> myfile.tex`
* Layouts
 - `-narr`: Narrow
 - `-wide`: Wide
 - `-2col`: 2 Columns
 - `-3col`: 3 Columns
 - `-2colw`: 2 Columns, wide

* Options
 - `-noopen`: Don't open the file after compilation
 - `-out <filename.pdf>`: Specify an output filename

#### `python lal.py -clean`
 - Cleans up the temporary files that come with compiling the .tex

Other Syntax
---------
* Images: `[img=test.png,350]`
 - Uses image "test.png" in same folder, height = 350
 
* Start and End Tags:
 - Use to render only a part of a document.
 - Start: `===START===`
 - End: `===END===`
 - Case insensitive. Any number of "=" characters 3 or more can be used on either side.
 - Start tag denotes start of document. Anything preceding the start tag will not be rendered.
 - End tag denotes end of document. Anything after the end tag will not be rendered.
 - Unspecified behaviour if multiple start / end tags exist.

Development
--------
Most of the logic is still pretty hacky. But it works, for most cases, as of now.
