# <!DoctypeTool> 
Cross-platform tool for reporting and manipulating XML 1.0 document type declarations

# Pre-requisites
Tested under Python 3.8

# Installation
Simply place `src/doctype.py` somewhere on your system and invoke it in the usual way, e.g.

```
python path/to/doctype.py
```

The synopsis below should appear.

## Windows executables
On Windows, executables are also provided, built using [pyinstaller](https://pyinstaller.org/): see `dist/doctype/` and `dist/standalone`.

You can use these without needing to install python.

To use the former, you must copy the entire contents of the directory. The standalone version can be used on its own, but will be [slower to start](https://pyinstaller.org/en/stable/operating-mode.html#how-the-one-file-program-works).

In either case, invoke `doctype.exe` and the synopsis should appear.

# Synopsis
```
<!DoctypeTool> - a tool to report and amend XML 1.0 DOCTYPE declarations

Syntax: doctype.py <options> file
where options are:
    -h print this message to the console and exit
    -P omit public identifier
    -p <value> specify public identifier with <value>
    -q do not emit the document passed in
    -r <value> specify root element named <value>
    -S omit system and public identifiers
    -s <value> specify system identifier with <value>
```

# Usage
See [the wiki](https://github.com/AndrewSales/doctype-tool/wiki/Getting-started) for details.
