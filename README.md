# <!DoctypeTool> 
Cross-platform tool for reporting and manipulating XML 1.0 document type declarations

# Pre-requisites
Tested under Python 3.8

# Synopsis
```
<!DoctypeTool> - a tool to report and amend XML 1.0 DOCTYPE declarations

Syntax: doctype.py <options> file
where options are:
    -h print this message to the console
    -P omit public identifier
    -p <value> specify public identifier with <value>
    -q do not emit the document passed in
    -r <value> specify root element named <value>
    -S omit system and public identifiers
    -s <value> specify system identifier with <value>
```    

# Behaviour
## Reporting the `DOCTYPE`
By default, and with no options specified, the tool emits the document passed in verbatim to standard output. This can be turned off by specifying option `-q`.

An XML report of any errors encountered by the (non-validating) parser, together with details of any `DOCTYPE` declaration, is emitted to standard error.

The report takes this format:

```
<report uri='my-file.xml'>
<doctype root='foo' systemID='bar' publicID='blort'/>
</report>
```

The `<doctype>` attributes occur only if the corresponding information is present in the `DOCTYPE` declaration.
If there is no `DOCTYPE` declaration, `<doctype>` is omitted from the report.

Any errors appear, for example, as:

```
<report uri='my-file.xml'>
<error>my-file.xml:1:0: no element found</error>
</report>
```

Note that if a parseable `DOCTYPE` declaration is encountered and the overall document is not well-formed, the declaration will still be reported, along with the well-formedness error.

## Amending the `DOCTYPE`
Other options amend the `DOCTYPE` declaration in the emitted document as follows. Options may be combined (except for combinations which would both specify and omit `SYSTEM` and `PUBLIC` identifiers).

### Omit `PUBLIC` identifier
Specifying option `-P` changes e.g. this:

```
<!DOCTYPE foo PUBLIC "somePublicID" "my.dtd">... 
```

to this:

```
<!DOCTYPE foo SYSTEM "my.dtd">... 
```

### Change `PUBLIC` identifier
Specifying option `-p<value>` changes e.g. this:

```
<!DOCTYPE foo PUBLIC "somePublicID" "my.dtd">... 
```

to this:

```
<!DOCTYPE foo PUBLIC "otherPublicID" "my.dtd">... 
```

### Change root element name
Specifying option `-r<value>` changes e.g. this:

```
<!DOCTYPE foo ...>
```

to this:

```
<!DOCTYPE bar ...>
```

### Omit `SYSTEM` and `PUBLIC` identifiers
Specifying option `-S` changes e.g. this:

```
<!DOCTYPE foo PUBLIC "somePublicID" "my.dtd">... 
```

to this:

```
<!DOCTYPE foo>... 
```

### Change `SYSTEM` identifier
Specifying option `-s<value>` changes e.g. this:

```
<!DOCTYPE foo SYSTEM "my.dtd">... 
```

to this:

```
<!DOCTYPE foo SYSTEM "your.dtd">... 
```

Arguments containing spaces must be escaped in the usual way at the command line.

N.B. If the `DOCTYPE` declaration is amended by the options specified, then the resulting report features the _updated_ values, rather than those found in the original document.

## IMPORTANT 
*The application makes no attempt to check whether values passed in would result in well-formed output.*
