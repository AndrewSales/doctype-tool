import xml.sax, xml.sax.handler, xml.sax.saxutils, sys, getopt

# *tested with Python 3.8*
# report DOCTYPE: root, system, public -- as XML doc!
# amend DOCTYPE:
# - supply system, public
# - specify internal subset (via external text file)
# option to report DOCTYPE for malformed docs


class Doctype():
    """
    Class to model an XML document type declaration.
    """
    def __init__(self, root, publicID, systemID):
        self.root = root
        self.publicID = publicID
        self.systemID = systemID

    def asDeclaration(self):
        """
        Return the DOCTYPE as a string, suitable for inclusion
        in a serialized XML document.
        """
        ids = ''
        if self.publicID:
            ids = ' PUBLIC "%s" "%s"' % (self.publicID,self.systemID)
        elif self.systemID:
            ids = ' SYSTEM "%s"' % self.systemID            
        return '<!DOCTYPE %s%s>' % (self.root, ids)

    def asXML(self, uri):
        """
        Return the DOCTYPE as a serialized XML document of the format:
        
        <doctype uri='...' root='...' systemID='...' publicID='...'/>

        where:
        @uri is the URI of the document whose DOCTYPE is requested
        @root is the declared root element name
        @systemID is the SYSTEM identifier
        @publicID is the PUBLIC identifier.
        """
        s = "<doctype uri='%s' root='%s'" % (uri,self.root)
        if self.publicID:
            s += " systemID='%s' publicID='%s'" % (self.systemID, self.publicID)
        elif self.systemID:
            s += " systemID='%s'" % self.systemID
        s += '/>'    
        return s

class DoctypeReporter(xml.sax.handler.ErrorHandler):
    """
    LexicalHandler instance: writes the DOCTYPE declaration and comment and
    CDATA events to the XMLGenerator instance passed to the constructor.
    """
    def __init__(self, writer, systemID, publicID):
        self.writer = writer
        self.doctype = None
        self.hasFatalErrors = False
        self.publicID = publicID
        self.systemID = systemID

    def comment(self, comment):
        self.writer._write('<!--%s-->' % comment)

    def startDTD(self, name, publicID, systemID):
        if self.systemID:
            systemID = self.systemID
        if self.publicID:
            publicID = self.publicID
        self.doctype = Doctype(name, publicID, systemID)

    def endDTD(self):
        if self.doctype:
            self.writer._write(self.doctype.asDeclaration())

    def startCDATA(self):
        self.writer._write('<![CDATA[')

    def endCDATA(self):
        self.writer._write(']]>')

    def reportDoctype(self, uri):
        if self.doctype:
            sys.stderr.write(self.doctype.asXML(uri))

    def fatalError(self, e):
        sys.stderr.write('[FATAL]:%s:%d:%d:%s' % \
            (e.getSystemId(),e.getLineNumber(),e.getColumnNumber(),e.getMessage()))
        self.hasFatalErrors = True
        raise e

    def error(self, e):
        sys.stderr.write('[ERROR]:%s:%d:%d:%s' % \
            (e.getSystemId(),e.getLineNumber(),e.getColumnNumber(),e.getMessage()))            

    def warning(self, e):
        sys.stderr.write('[WARNING]:%s:%d:%d:%s' % \
            (e.getSystemId(),e.getLineNumber(),e.getColumnNumber(),e.getMessage()))                        

def usage():
    print("""<!DoctypeTool> - a tool to report and amend XML 1.0 DOCTYPE declarations

Syntax: DoctypeTool <options> file
where options are:
    -h print this message to the console
    -P omit public identifier
    -p <value> specify public identifier with <value>
    -r <value> specify root element named <value>
    -S omit system and public identifiers
    -s <value> specify system identifier with <value>""")

def fatal():
    usage()
    sys.exit(-1)

if len(sys.argv) < 2:
    fatal()

system = None
public = None
omitPublic = False
omitSystem = False
root = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'hPp:Ss:')
except getopt.GetoptError as err:
    print(err)
    fatal()

for o, a in opts:
    if o == '-h':
        usage()
        sys.exit()
    elif o == '-s':
        system = a
    elif o == '-p':
        public = a        
    elif o == '-P':
        omitPublic = True
    elif o == '-r':
        root = a
    elif o == '-S':
        omitSystem = True        

if len(args) != 1:
   print("exactly one file expected: %s" % args)
   fatal()

if public and omitPublic:
    print('only one of -p or -P allowed')
    fatal()
if omitSystem and (system or public):
    print('-S not allowed with -s or -p')
    fatal()

writer = xml.sax.saxutils.XMLGenerator(encoding='utf-8')
dr = DoctypeReporter(writer, system, public)
parser = xml.sax.make_parser()
parser.setProperty(xml.sax.handler.property_lexical_handler, dr)
parser.setContentHandler(writer)
parser.setErrorHandler(dr)

fn = args[0]
try:
    parser.parse(fn)
except Exception as err:
    print(err)  
    dr.reportDoctype(fn)  #option to report even after fatal error  
    sys.exit(-1)