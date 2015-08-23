Syntax
=========
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