import unittest
import string
from SwiftFormat.Parser import *
from SwiftFormat.Scanner import *


class ParserCombinatorTest(unittest.TestCase):
    def testA(self):
        parser = a("a")
        assert parser.parse('a')
        assert parser.parse('b') is None

    def testAnd(self):
        parser = a("a") & a("b")
        assert parser.parse('ab')
        assert parser.parse('ba') is None

    def testOr(self):
        parser = a('a') | a('b')
        assert parser.parse('a')
        assert parser.parse('b')
        assert parser.parse('c') is None

    def testRShift(self):
        parser = a('a') >> (lambda x: string.upper(x) if x is not None else x)
        assert parser.parse("a")[0] == u"A"
        assert parser.parse('b') is None

    def testSetType(self):
        parser = (a('a') | a('b')) >> (set_type(SwiftTypes.LITERAL_INTEGER_BINARY))
        assert parser.parse('a')[0].meta.type == SwiftTypes.LITERAL_INTEGER_BINARY

    def testBetween(self):
        parser = between('a', 'c')
        assert parser.parse('a')
        assert parser.parse('b')
        assert parser.parse('c')
        assert parser.parse('d') is None

    def testMaybe(self):
        parser = maybe(a('a'))
        assert parser.parse('a')
        assert parser.parse('b')[0] == u""

    def testAtLeastOne(self):
        parser = at_least_one(a("a"))
        assert parser.parse('a')
        assert parser.parse('aaaa')[0] == u"aaaa"
        assert parser.parse('b') is None

    def testMany(self):
        parser = many(a("a"))
        assert parser.parse('b')[0] == u""
        assert parser.parse('a')
        assert parser.parse('aaaa')[0] == u"aaaa"


    def testOneOf(self):
        parser = one_of(a(" "), a("\t"), a("\n"))
        assert parser.parse(' ')
        assert parser.parse('\t')
        assert parser.parse('\n')
        assert parser.parse('a') is None

    def testOneOfNoOptions(self):
        parser = one_of()
        assert parser is None

    def testEveryNoOptions(self):
        parser = every()
        assert parser is None

    def testSkip(self):
        parser = skip(one_of(a(" "), a("\t"), a("\n"))) & a("a")
        assert parser.parse("   a")[0] == u'a'

    def testRepeat(self):
        parser = repeat(a("a"), a("a") & a("b"))
        assert parser.parse("aaaaab")
        assert parser.parse("aaaaa") is None

    def testMatch(self):
        parser = match("let") | match("latitude")
        assert parser.parse("let")
        assert parser.parse("latitude")
        assert parser.parse("lat") is None

    def testForwardDecl(self):
        parser = forward_decl()
        try:
            parser.parse('')
            self.fail()
        except:
            pass

    def testDefine(self):
        parser = forward_decl()
        try:
            parser.define(a('a'))
            assert parser.parse('a')
        except:
            self.fail()

    def testAnything(self):
        parser = anything()
        assert parser.parse("a")
        assert parser.parse("0")
        assert parser.parse("\n")
        assert parser.parse(" ")
        assert parser.parse("") is None

    def testAnythingBut(self):
        parser = anything("1", "2", "3")
        assert parser.parse("a")
        assert parser.parse("0")
        assert parser.parse("\n")
        assert parser.parse(" ")

        assert parser.parse("1") is None
        assert parser.parse("2") is None
        assert parser.parse("3") is None
        assert parser.parse("") is None

    def testEOF(self):
        parser = eof()
        assert parser.parse("")
        assert parser.parse("ads") is None

    def testMax(self):
        parser = longest(a("a"), many(a("a")))
        assert parser.parse("aaaaa")[0] == u"aaaaa"

    def testUpTo(self):
        parser = up_to(a("a"), 1)
        assert parser.parse("a")
        assert parser.parse("aa")[0].__len__() == 1

        parser = up_to(a("a"), 3)
        assert parser.parse("a")
        assert parser.parse("aa")
        assert parser.parse("aaa")
        assert parser.parse("aaaa")[0].__len__() == 3
