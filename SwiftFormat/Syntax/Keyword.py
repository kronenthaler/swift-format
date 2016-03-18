from SwiftFormat.Parser import *
from SwiftFormat.Scanner import *


# Keywords used in declarations:
#   class, deinit, enum, extension, func, import, init, inout, internal, let, operator, private, protocol, public,
#   static, struct, subscript, typealias, and var.
# Keywords used in statements:
#   break, case, continue, default, defer, do, else, fallthrough, for, guard, if, in, repeat, return, switch, where,
#   and while.
# Keywords used in expressions and types:
#   as, catch, dynamicType, false, is, nil, rethrows, super, self, Self, throw, throws, true, try, __COLUMN__, __FILE__,
#    __FUNCTION__, and __LINE__.
# Keywords used in patterns: _.
# Keywords reserved in particular contexts:
#   associativity, convenience, dynamic, didSet, final, get, infix, indirect, lazy, left, mutating, none, nonmutating,
#   optional, override, postfix, precedence, prefix, Protocol, required, right, set, Type, unowned, weak, and willSet.


def keyword():
    return _declaration_keyword() | \
           _statement_keyword() | \
           _expression_keyword() | \
           _pattern_keyword() | \
           _context_keywords()


def _declaration_keyword():
    return one_of(match(u"class"), match(u"deinit"), match(u"enum"),
                  match(u"extension"), match(u"func"), match(u"import"),
                  match(u"init"), match(u"inout"), match(u"internal"),
                  match(u"let"), match(u"operator"), match(u"private"),
                  match(u"protocol"), match(u"public"), match(u"static"),
                  match(u"struct"), match(u"subscript"), match(u"typealias"),
                  match(u"var")) >> set_type(SwiftTypes.KEYWORD_DECLARATION)


def _statement_keyword():
    return one_of(match(u"break"), match(u"case"), match(u"continue"),
                  match(u"default"), match(u"defer"), match(u"do"),
                  match(u"else"), match(u"fallthrough"), match(u"for"),
                  match(u"guard"), match(u"if"), match(u"in"),
                  match(u"repeat"), match(u"return"), match(u"switch"),
                  match(u"where"), match(u"while")) >> set_type(SwiftTypes.KEYWORD_STATEMENT)


def _expression_keyword():
    return one_of(match(u"as"), match(u"catch"), match(u"dynamicType"),
                  match(u"false"), match(u"is"), match(u"nil"),
                  match(u"rethrows"), match(u"super"), match(u"self"),
                  match(u"Self"), match(u"throw"), match(u"throws"),
                  match(u"true"), match(u"try"), match(u"__COLUMN__"),
                  match(u"__FILE__"), match(u"__FUNCTION__"), match(u"__LINE__")
                  ) >> set_type(SwiftTypes.KEYWORD_EXPRESSION_TYPES)


def _pattern_keyword():
    return a(u"_") >> set_type(SwiftTypes.KEYWORD_PATTERNS)


def _context_keywords():
    return one_of(match(u"associativity"), match(u"convenience"), match(u"dynamic"),
                  match(u"didSet"), match(u"final"), match(u"get"),
                  match(u"infix"), match(u"indirect"), match(u"lazy"),
                  match(u"left"), match(u"mutating"), match(u"none"),
                  match(u"nonmutating"), match(u"optional"), match(u"override"),
                  match(u"postfix"), match(u"precedence"), match(u"prefix"),
                  match(u"Protocol"), match(u"required"), match(u"right"),
                  match(u"set"), match(u"Type"), match(u"unowned"),
                  match(u"weak"), match(u"willSet")) >> set_type(SwiftTypes.KEYWORD_RESERVED | SwiftTypes.IDENTIFIER)
