from SwiftFormat.Parser import *

# comment ::= single_line | multi_line
# single_line ::= //[ascii]* \n
# single_line ::= //[ascii]* \r
# single_line ::= //[ascii]* EOF
# multi_line ::= /* {[ascii]* | multi_line}* */

def comment():
    return _single_line_comment() | _multi_line_comment()


def _single_line_comment():
    return match(u"//") & repeat(anything(), a(u"\r") | a(u"\n") | eof())

def _multi_line_comment():
    multi_line = forward_decl()
    parser = match(u"/*") & many(repeat(anything(), match(u"/*") | match(u"*/")) | multi_line) & match(u"*/")
    return multi_line.define(parser)
