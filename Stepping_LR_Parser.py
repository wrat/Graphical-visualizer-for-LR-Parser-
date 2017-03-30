from __future__ import print_function, unicode_literals

from nltk.grammar import Nonterminal
from nltk.tree import Tree
from nltk.compat import unicode_repr

from nltk.parse.api import ParserI
from LR_Parser import LeftReduceParser
from CFG import LR_Parsing_table
from nltk.grammar import Nonterminal, Production,CFG

class SteppingLRParser(LeftReduceParser):

    def __init__(self, grammar, trace=0):
        self._grammar = grammar
        self._trace = trace
        self._stack = None
        self.LR_stack = None
        self._remaining_text = None
        self._history = []
        self.lr_history = []
        self.reducible_production = []
        self.state = None
        self._Parsing_table,self._cononical_state,self._relation_state = LR_Parsing_table(grammar)

    def parse(self, tokens):
        tokens = list(tokens)
        self.initialize(tokens)
        while self.step():
            pass
        return self.parses()

    def stack(self):

        return self._stack

    def remaining_text(self):

        return self._remaining_text

    def initialize(self, tokens):

        self._stack = []
        self.LR_stack = [0]
        self._remaining_text = tokens
        self._history = []

    def step(self):

        return self.lr_shift()


    def lr_shift(self):

          if len(self._remaining_text) == 0: return False
          self._history.append( (self._stack[:], self._remaining_text[:]) )
          self.state = self._shift_lr(self.LR_stack,self._stack, self._remaining_text)
          self.lr_history.append((self.LR_stack[:], self._remaining_text[:]))
          if(self.state):
              return self.state
          #return True  

    def shift(self):

        if len(self._remaining_text) == 0: return False
        self._history.append( (self._stack[:], self._remaining_text[:]) )
        self._shift(self._stack, self._remaining_text)
        return True

    def reduce(self, production=None):


        self._history.append( (self._stack[:], self._remaining_text[:]) )
        return_val = self._reduce(self.LR_stack,self._stack, self._remaining_text,self.state)

        if not return_val: self._history.pop()
        return return_val

    def undo(self):

        if len(self._history) == 0 or len(self.lr_history) == 0: return False
        (self._stack, self._remaining_text) = self._history.pop()
        (self.LR_stack, self._remaining_text) = self.lr_history.pop()
        return True

    def reducible_productions(self):
        
        productions = self._reducible_production()
        
        return productions

    def cononical_state(self):

         self._Parsing_table,self._cononical_state,self._relation_state = LR_Parsing_table(self._grammar)
         return self._cononical_state , self._relation_state

 
    def parses(self):

        if (len(self._remaining_text) == 0 and
            len(self._stack) == 1 and 
            self._stack[0].label() == self._grammar.start().symbol()
            ):
            yield self._stack[0]

# copied from nltk.parser
    def set_grammar(self, grammar):

        self._grammar = grammar
        self.lr_set_grammar(self._grammar)
        self._Parsing_table = LR_Parsing_table(self._grammar)

