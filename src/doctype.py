import xml.sax, xml.sax.handler, xml.sax.saxutils, sys, getopt

# *tested with Python 3.8*
# TODO create DOCTYPE where none present
# TODO report discrepancy between declared and actual root
# TODO specify internal subset (via external text file)
# TODO report DOCTYPE for malformed docs


class Doctype():
    """
    Class to model an XML document type declaration.
    """
    def __init__(self, root, publicID=None, systemID=None):
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

    def asXML(self):
        """
        Return the DOCTYPE as a serialized XML document of the format:
        
        <doctype root='...' systemID='...' publicID='...'/>

        where:
        @root is the declared root element name
        @systemID is the SYSTEM identifier
        @publicID is the PUBLIC identifier.
        """
        s = "<doctype root='%s'" % (self.root)
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
    def __init__(self, writer):
        self.writer = writer
        self.doctype = None
        self.publicID = None
        self.systemID = None
        self.omitPublic = False
        self.omitSystem = False
        self.root = None
        self.errors = []

    def setSystemID(self, systemID):
        self.systemID = systemID

    def setPublicID(self, publicID):
        self.publicID = publicID  

    def setRoot(self, root):
        self.root = root

    def omitSystemID(self):
        self.omitSystem = True

    def omitPublicID(self):
        self.omitPublic = True        

    def comment(self, comment):
        if self.writer:
            self.writer._write('<!--%s-->' % comment)

    def startDTD(self, name, publicID, systemID):
        #configure overrides
        if self.systemID:
            systemID = self.systemID
        if self.publicID:
            publicID = self.publicID
        if self.root:
            name = self.root
        
        if self.omitSystem:
            self.doctype = Doctype(name)
        elif self.omitPublic:
            self.doctype = Doctype(name, None, systemID)
        else:
            self.doctype = Doctype(name, publicID, systemID)

    def endDTD(self):
        if self.doctype and self.writer:
            self.writer._write(self.doctype.asDeclaration())

    def startCDATA(self):
        if self.writer:
            self.writer._write('<![CDATA[')

    def endCDATA(self):
        if self.writer:
            self.writer._write(']]>')

    def report(self, uri):
        s = "<report uri='%s'>" % uri
        for err in self.errors:
            s += '<error>%s</error>' % format(err)
        if self.doctype:
            s += self.doctype.asXML()
        s += '</report>'
        return s

    def fatalError(self, e):
        self.errors.append(e)

    def error(self, e):
        self.errors.append(e)

    def warning(self, e):
        self.errors.append(e)

class DoctypeTool():

    OPTION_HELP = '-h'
    OPTION_SET_SYSTEM_ID = '-s'
    OPTION_SET_PUBLIC_ID = '-p'
    OPTION_DROP_SYSTEM_ID = '-S'
    OPTION_DROP_PUBLIC_ID = '-P'
    OPTION_QUIET = '-q'
    OPTION_SET_ROOT = '-r'
    OPTIONS = 'hPp:qr:Ss:'

    def __init__(self, args=sys.argv):
        sys.stdout.reconfigure(encoding='utf-8')    #else redirecting to file results in encoding error
        self.system = None
        self.public = None
        self.omitPublic = False
        self.omitSystem = False
        self.root = None
        self.quiet = False
        self.file = None
        self.parseCommandLine(args)

        writer = None
        if not self.quiet:
            writer = xml.sax.saxutils.XMLGenerator(encoding='utf-8')
        dr = DoctypeReporter(writer)
        dr.setPublicID(self.public)
        dr.setSystemID(self.system)
        if self.omitPublic:
            dr.omitPublicID()
        if self.omitSystem:
            dr.omitSystemID()
        if self.root:
            dr.setRoot(self.root)
        parser = xml.sax.make_parser()
        parser.setProperty(xml.sax.handler.property_lexical_handler, dr)
        if not self.quiet:
            parser.setContentHandler(writer)
        parser.setErrorHandler(dr)
        
        try:
            parser.parse(self.file)
            sys.stderr.write(dr.report(self.file))
        # except xml.sax.SAXParseException as err:
        #     sys.stderr.write(format(err))  #option to report even after fatal error  
        #     sys.exit(-1)
        except Exception as err:
            sys.stderr.write('[FATAL]:' + format(err))
            sys.exit(-1)

    def usage(self):
        print("""<!DoctypeTool> - a tool to report and amend XML 1.0 DOCTYPE declarations

Syntax: doctype.py <options> file
where options are:
    -h print this message to the console and exit
    -P omit public identifier
    -p <value> specify public identifier with <value>
    -q do not emit the document passed in
    -r <value> specify root element named <value>
    -S omit system and public identifiers
    -s <value> specify system identifier with <value>""")

    def fatal(self, msg=''):
        sys.stderr.write('[FATAL]:' + msg)
        self.usage()
        sys.exit(-1)

    def parseCommandLine(self, args):
        if len(args) < 2:
            self.fatal('too few arguments')

        try:
            opts, args = getopt.getopt(args[1:], self.OPTIONS)
        except getopt.GetoptError as err:
            self.fatal(format(err))

        for o, a in opts:
            if o == self.OPTION_HELP:
                self.usage()
                sys.exit()
            elif o == self.OPTION_SET_SYSTEM_ID:
                self.system = a
            elif o == self.OPTION_SET_PUBLIC_ID:
                self.public = a        
            elif o == self.OPTION_DROP_PUBLIC_ID:
                self.omitPublic = True
            elif o == self.OPTION_SET_ROOT:
                self.root = a
            elif o == self.OPTION_DROP_SYSTEM_ID:
                self.omitSystem = True
            elif o == self.OPTION_QUIET:
                self.quiet = True

        if self.public and self.omitPublic:
            self.fatal('only one of -p or -P allowed')
        if self.omitSystem and (self.system or self.public):
            self.fatal('-S not allowed with -s or -p')

        if len(args) < 1:
            self.fatal("file must be specified")
        else:
            self.file = args[0] #subsequent file args ignored

if __name__ == '__main__':
    DoctypeTool()