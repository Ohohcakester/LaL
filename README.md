Less Annoying LaTeX
=========
Quick and easy LaTeX typesetting for the lazy. When having a nicely-formatted document isn't a priority. (e.g. taking notes, doing assignments, making crib sheets)

How to use
---------
There is only one file, **lal.py**.

To compile a .tex file "myfile.tex", run `python lal.py myfile.tex`.

This will create a file called `tempfilename.pdf`. (Yes I know it's weird. I'll change it at some point)

Requirements
---------
* Python 3
* pdflatex

Arguments
---------
* `python lal.py -OPTION myfile.tex`
 - `-narr`: Narrow
 - `-wide`: Wide
 - `-2col`: 2 Columns
 - `-3col`: 3 Columns
 - `-2colw`: 2 Columns, wide

* `python lal.py -clean`
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
At the moment, the script is pretty hacky. At some point I'll clean up the code. As of now, it's just there for the utility.
