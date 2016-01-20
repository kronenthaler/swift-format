from SwiftFormat.SwiftNodeTypes import *


class CommentScanner:
    END_OF_LINE = u"\x0A\x0D"
    SINGLE_LINE_HEAD = u"//"
    MULTI_LINE_HEAD = u"/*"
    MULTI_LINE_TAIL = u"*/"

    def comment(self, tokenizer):
        comment = self.single_line_comment(tokenizer)
        if comment:
            return comment
        return self.multi_line_comment(tokenizer)

    def single_line_comment(self, tokenizer):
        head = tokenizer.search_for(CommentScanner.SINGLE_LINE_HEAD)
        if not head:
            return None

        comment = tokenizer._next_token(delimiters=CommentScanner.END_OF_LINE, allowEOF=True)
        if not comment:
            return tokenizer.push_back()

        return SingleLineComment(comment)

    def multi_line_comment(self, tokenizer):
        head = tokenizer.search_for(CommentScanner.MULTI_LINE_HEAD)
        if not head:
            return None

        comment_node = None

        while True:
            # it could happen multiple times
            comment = tokenizer.advance([CommentScanner.MULTI_LINE_HEAD, CommentScanner.MULTI_LINE_TAIL])
            if not comment:
                tokenizer.push_back()
                break

            if comment_node is None:
                comment_node = MultiLineComment(comment)
            else:
                comment_node.append(comment)

            if tokenizer.current_token().token == CommentScanner.MULTI_LINE_HEAD:
                tokenizer.push_back()
                sub_comment_node = self.multi_line_comment(tokenizer)
                comment_node.append(sub_comment_node)
            elif tokenizer.current_token().token == CommentScanner.MULTI_LINE_TAIL:
                return comment_node

        return comment_node