from xmlrpclib import Transport, ServerProxy
import readline
import cmd
import traceback
import pprint
import datetime
from optparse import OptionParser
import sys


class CustomXmlRpcExtensionTransport(Transport):
    """
    This Transport allows for the parser's dispatch object to be modified to cater for additional
    extension tags. In case the client need to be extend to interoperate with other provider,
    such as apache xml-rpc service points.
    see also http://bugs.python.org/issue8792
    """
    def getparser(self):
        parser, unmarshaller = Transport.getparser(self)
        dispatch = unmarshaller.dispatch.copy()
        unmarshaller.dispatch = dispatch
        # Now we can add custom types
        dispatch["ex:nil"] = dispatch["nil"]
        dispatch["ex:i2"]  = dispatch["int"]
        dispatch["ex:i4"]  = dispatch["int"]
        dispatch["ex:i8"]  = dispatch["int"]

        return parser, unmarshaller

class XmlRpcClientConsole(cmd.Cmd):
    """
    Generic xml rpc client console. Allows for seamlessly working with compatible xml-rpc server.
    """
    def __init__(self, url):
        cmd.Cmd.__init__(self)
        self.url = url;
        self.server = ServerProxy(url, transport=CustomXmlRpcExtensionTransport(use_datetime=True)) #verbose=True,)
        self.pp = pprint.PrettyPrinter(indent=2)
        self.updatePrompt()

    def updatePrompt(self):
        self.prompt = "\n[%s] %s\nxmlrpc >> " % (datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S"),self.url)

    def default(self, line):
        try:
            result=None
            exec("result=self.server.%s" % (line))
            self.pp.pprint(result) # default formatter: pretty print the resultant data
        except Exception, ex:
            traceback.print_exc(ex)
        print; self.updatePrompt()

    def do_help(self,line):
        print
        print "-------------------------------------"
        print "GENERIC XML RPC CLIENT CONSOLE - HELP"
        print "-------------------------------------"
        print
        print "Simply type in the function name on the xml-rpc service end, like you would"
        print "on any good ol' python program. For example, if the other side has a method"
        print "called helloWorld(strparam), you can invoke it like so:"
        print
        print "... xmlrpc >> helloWorld('hello zen')"
        print
        print "the client is therefore completely transparent and exposes the full capabilities"
        print "of the server end. have fun." # -zen
        print

def main():
    parser = OptionParser("""Generic XML RPC Client console""")
    parser.add_option("--url", dest="url", help="The XML RPC service URL to connect")
    parser.add_option("--cmd", dest="cmd", help="A one-off command to execute")
    (options, args) = parser.parse_args()

    if options.url == None :
        parser.print_help()
        sys.exit(1)

    console = XmlRpcClientConsole(options.url)
    if options.cmd != None :
        # run the cmd and bomb out
        console.default(options.cmd)
        sys.exit(0)
    else:
        print "for help using the console, type 'help'"
        # enter into cmd loop for interactive session
        console.cmdloop()

if __name__ == "__main__":
    main()
