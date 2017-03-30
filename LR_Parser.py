from __future__ import print_function, unicode_literals
from nltk.grammar import Nonterminal
from nltk.tree import Tree
from nltk.compat import unicode_repr
from nltk.parse.api import ParserI
from CFG import LR_Parsing_table


class LeftReduceParser(ParserI):

    def __init__(self, grammar, trace=0):
        self._grammar = grammar
        self._trace = trace
        self._check_grammar()
        self._Parsing_table,self._cononical_state,self._relation_state = LR_Parsing_table(grammar)
        self.reducible_production = []

    def grammar(self):
        return self._grammar

    def parse(self, tokens):
        tokens = list(tokens)
        self._grammar.check_coverage(tokens)
        # initialize the stack.
        LR_stack = [0]
        stack = []  
        remaining_text = tokens
        remaining_text.append('$')
        # Trace output.
        if self._trace:
            print('Parsing %r' % " ".join(tokens))
            self._trace_stack(stack, remaining_text)

        # iterate through the text, pushing the token onto
        # the stack, then reducing the stack.

        while len(remaining_text) > 0: 
            state = self._shift_lr(LR_stack,stack,remaining_text)
            if(state):
		    if(state[0] == 'S'):
		           self._shift(stack,remaining_text)
		    if(state[0] == 'r'):
		           self._reduce(LR_stack,stack, remaining_text,state)  
            #while self._reduce(stack, remaining_text): pass

        # Did we reduce everything?
        if len(stack) == 1: 
            # Did we end up with the right category?
            if stack[0].label() == self._grammar.start().symbol():
                yield stack[0]


    def _shift_lr(self,LR_stack,stack,remaining_text):

         top_lr = LR_stack[(len(LR_stack)-1)]
         state  =   (self._Parsing_table[top_lr])[remaining_text[0]]     
         if(state == 'accept'):
              remaining_text.remove(remaining_text[0])
       
         if(state[0] == 'S'):
                if(len(state) > 2):
                    var = state[1] + state[2]
                    var = int(var)
                else:
                   var = int(state[1])

         	LR_stack.append(remaining_text[0])
         	LR_stack.append(var)
                remaining_text.remove(remaining_text[0])
               
         return state
    
      

    def _shift(self, stack, remaining_text):
        stack.append(remaining_text[0])
        #remaining_text.remove(remaining_text[0])
        if self._trace: self._trace_shift(stack, remaining_text)

    def _reduce(self,LR_stack,stack, remaining_text,state):


        productions = self._grammar.productions()
        production  = productions[int(state[1])-1]
        self.reducible_production.append(production)
        rhslen = len(production.rhs())
        lhs = production.lhs()

        tree = Tree(production.lhs().symbol(), stack[-rhslen:])
        stack[-rhslen:] = [tree]

        #Remove 2*rhslen element from LR_stak
        for count in range(2*rhslen):  
               LR_stack.pop()
        
        top_lr1 =  LR_stack[(len(LR_stack)-1)]
        
        #Append lhs of production
        LR_stack.append(lhs)

        top_lr2 =  LR_stack[(len(LR_stack)-1)]
        new_state = (self._Parsing_table[top_lr1])[top_lr2]
        LR_stack.append(new_state)
    
        #print('After Reduction',LR_stack)
        #We reduced something

        if self._trace:
           self._trace_reduce(stack, production, remaining_text)
        return production


        # We didn't reduce anything
        return None


    def _reducible_production(self):
        production_list = self.reducible_production
        return production_list



    def trace(self, trace=2):
        # 1: just show shifts.
        # 2: show shifts & reduces
        # 3: display which tokens & productions are shifed/reduced
        self._trace = trace


    def _trace_stack(self, stack, remaining_text, marker=' '):
        s = '  '+marker+' [ '
        for elt in stack:
            if isinstance(elt, Tree):
                s += unicode_repr(Nonterminal(elt.label())) + ' '
            else:
                s += unicode_repr(elt) + ' '
        s += '* ' + ' '.join(remaining_text) + ']'
        print(s)


    def _trace_shift(self, stack, remaining_text):

        if self._trace > 2: print('Shift %r:' % stack[-1])
        if self._trace == 2: self._trace_stack(stack, remaining_text, 'S')
        elif self._trace > 0: self._trace_stack(stack, remaining_text)


    def _trace_reduce(self, stack, production, remaining_text):

        if self._trace > 2:
            rhs = " ".join(str(production.rhs()))
            print('Reduce %r <- %s' % (production.lhs(), rhs))
        if self._trace == 2: self._trace_stack(stack, remaining_text, 'R')
        elif self._trace > 1: self._trace_stack(stack, remaining_text)


    def _check_grammar(self):

        productions = self._grammar.productions()

        # Any production whose RHS is an extension of another production's RHS
        # will never be used.
        for i in range(len(productions)):
            for j in range(i+1, len(productions)):
                rhs1 = productions[i].rhs()
                rhs2 = productions[j].rhs()
                if rhs1[:len(rhs2)] == rhs2:
                    print('Warning: %r will never be used' % productions[i])

# copied from nltk.parser

    def lr_set_grammar(self, grammar):
         
        self._grammar = grammar
        self._Parsing_table = LR_Parsing_table(grammar)      

def demo():
    
    """
    A demonstration of the shift-reduce parser.
    """

    from nltk import parse, CFG

    grammar2 = CFG.fromstring("""
    S -> A A
    A -> "a" A | "b"
    """)

    grammar1 = CFG.fromstring("""
         E -> E "+" E
         E -> E "*" E
         E -> "(" E ")"
         E -> "i"
    """)
 
    grammar3 = CFG.fromstring("""
           S -> "w" "(" "e" ")" S | "{" L "}" | "s"
           L ->  L ";" S | S
    """)

   
    #print(LR_Parsing_table(grammar1))
               
    
    sent = 'i + i + i'.split()
    parser = LeftReduceParser(grammar1, trace=2)
    for p in parser.parse(sent):
        print(p)
   

if __name__ == '__main__':
    demo()
