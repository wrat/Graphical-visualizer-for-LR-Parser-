from nltk.grammar import Nonterminal, Production,CFG
import re
import copy
from collections import OrderedDict

done = False
def lhs(production):
     """
     Return the left-hand side of this ``Production``.
     :rtype: Nonterminal
     """
     return production.lhs()


def rhs(production):
     """
     Return the right-hand side of this ``Production``.
     :rtype: sequence(Nonterminal and terminal)
     """
     return production.rhs()


def is_nonterminal(item):
    """
    :return: True if the item is a ``Nonterminal``.
    :rtype: bool
    """
    return isinstance(item, Nonterminal)


def is_terminal(item):
    """
    Return True if the item is a terminal, which currently is
    if it is hashable and not a ``Nonterminal``.

    :rtype: bool
    """
    return hasattr(item, '__hash__') and not isinstance(item, Nonterminal)


""" Get All Production Whose left side is this item"""
def get_production(Productions , lhs_item ):
    related_production = []
    for each_production in Productions:
        if(str(lhs(each_production)) == lhs_item ):
            related_production.append(each_production)
    
    return related_production


"""Get Terminals and Non_terminals from Production"""
def get_all_items(Productions):
    item = []
    for production in Productions:
         if(lhs(production) not in item):
         	item.append(lhs(production))
         if(production.is_nonlexical()):
         	pass
         if(production.is_lexical()):
         	production_rhs = rhs(production)
                for each_item in production_rhs:
                    if(each_item not in item):
                    	item.append(each_item) 
    return list(item)         



def first_of(item , first_of_item , Productions):
        
    if(is_nonterminal(item)):
       """ 
         If item is non-terminal then 
         first-of that item is set of all it's production's first
       """
       #If it has Null Production
       if(has_null_production(item,Productions)):
          first_of_item[item] = set(["NULL"])
       related_production = get_production(Productions,str(item))
       for production in related_production:
           if(production.is_lexical()):
               production_rhs = rhs(production)[0]
               first_of_item[item].add(production_rhs)
           else:
              production_rhs = rhs(production)[0]
              first = first_of_item[production_rhs]
              if(len(first) > 0):
                   first_of_item[item] = first
              else:
                  return first_of_item 
       
    #If Item is terminal
    if(is_terminal(item)):
         first_of_item[item].add(str(item))

    if(item == "NULL"):
        first_of_item[item].add(str(item))      

    
    return first_of_item

def has_null_production(item,Productions):
    
    for each_production in Productions:
        if(lhs(each_production) == item):
            if(str(rhs(each_production)[0]) == "NULL"):
                return True
     



def Closure(I , Original_Productions,final_item):
    
   
    done = False
    flag = 0
    while(1):
            
            temp_len = len(I)
             
	    for (_Production_) in copy.copy(I):                   
		 production_rhs    = rhs(_Production_)
                 production_string = _Production_.__repr__()
                 production_string = "".join(production_string.split())
                 production_string = production_string.replace("'","")         
		 match_char = re.search('([.])(\w)',production_string)
                 match_operator = re.search('([.])(\W)',production_string)            
                 for (i,count) in zip(production_string,range(len(production_string))):
                 	if(i == '.'):
                            break
                  
                 if(count == len(production_string)-1):
                      final_production = _Production_
                      flag = 1
                      continue
                 
		 if(match_char):
		    
                    B = match_char.group(2)

                 if(match_operator):
                    B = match_operator.group(2)
                 
                 #if(len(production_string) > count+2):
                      #beta = production_rhs[count-2]
                      #b = first[beta]
                 
                 #else:
		      #b = symbol

                 count = count - 3
		 related_productions = get_production(Original_Productions,B)
		 for each_production in related_productions:
		     #for each_terminal in b:
                          
                          if(str(rhs(each_production)[0]) == "NULL"):
                               ele = (each_production,'NULL')                                 
                               if(ele not in I):
                                    I.append(ele)
                          else: 
				  production_rhs = list(rhs(each_production)) 
				  N1 = Nonterminal('.'+str(production_rhs[0]))
				  production_rhs[0] = N1
				  
				  new_production = Production(lhs(each_production) , production_rhs) 
				  ele = (new_production)
				  if(ele not in I):
		   		          I.append(ele)
            if(temp_len == len(I)):
               break      

    if(flag):
       if(I not in final_item):
            final_item.append((I,final_production))

    return I,final_item                    
         

def get_J_items(I,X):
    
    J = []
    for(_Production_) in I:
           
           flag = 0
           production_string = _Production_.__repr__()
           production_string = "".join(production_string.split())
           production_string = production_string.replace("'","") 
           production_rhs = list(rhs(_Production_))
           
           for (i,count) in zip(production_string,range(len(production_string))):
                if(i == '.'):
                    break

           if(count == len(production_string)-1):
                    '''
                    final_item_production = set()
                    final_item_production.add(_Production_)
                    if(final_item_production not in final_item):        
                            final_item.append((final_item_production))
                    '''   
                    continue 
                   

           if(len(production_string) > count+2):
                
                dot_item = production_string[count+2]

           else:             
              
              dot_item = production_string[count+1]
              flag = 1
              
           count  = count - 3
           match_char  = re.search('[.](\w)' , production_string)
           match_operator = re.search('[.](\W)',production_string)
  
           if(match_char):

               match_item = match_char.group(1)
               if(match_item == str(X)):
                    
                    if(flag):
                    	N1 = Nonterminal(dot_item + '.')
                        if(len(production_rhs) == 1):  
                        	production_rhs[0] = N1
                        else:
                                production_rhs[count] = N1

                        new_production = Production(lhs(_Production_),production_rhs)
                        if((new_production) not in J):
                        	J.append((new_production))
                                   
                    else:
                        
                        N1 = Nonterminal('.' + dot_item)
                        production_rhs[count] = Nonterminal(match_item)
                        production_rhs[count+1] = N1
                    
                    new_production = Production(lhs(_Production_),production_rhs)
                    if((new_production) not in J ):
                    	J.append((new_production))

  
           if(match_operator):

               match_item = match_operator.group(1)
               if(match_item == str(X)):
                    
                    if(flag):
                    	N1 = Nonterminal(dot_item + '.')
                        if(len(production_rhs) == 1):  
                        	production_rhs[0] = N1
                        else:
                                production_rhs[count] = N1

                        new_production = Production(lhs(_Production_),production_rhs)
                        if((new_production) not in J):
                        	J.append((new_production))

                             
                    else:
                        
                        N1 = Nonterminal('.' + dot_item)
                        production_rhs[count] = Nonterminal(match_item)
                        production_rhs[count+1] = N1
                    
                    new_production = Production(lhs(_Production_),production_rhs)
                    if((new_production) not in J ):
                    	J.append((new_production))

    return J           


def Go_To(I,X,Productions,final_item):
     
     J = get_J_items(I,X)
     return Closure(J,Productions,final_item)
    
    
def is_empty(item):
    if(len(item) == 0):
         return True

    return False



def Cononical_Collections_items(Start_symbol , Productions):
     
 
 
     #List of All states After Performing Action
     Cononical_Collections_items = []
     first_of_item  = {}
     Original_Productions = Productions
     (S_ , S) = [Nonterminal('S_'),Nonterminal('.' + str(Start_symbol))] 
     Starting_production = Production(S_, [S])
     Productions = [Starting_production] + Productions
     Grammar_Symbol = get_all_items(Original_Productions)
     

     """Find All items First()"""
     for item in Grammar_Symbol:
          first_of_item[item] = set()
     
     for item in Grammar_Symbol:
           first_of_item = first_of(item , first_of_item,Original_Productions)
  
     
     C = []
     I = []
     I.append((Productions[0]))
     final_item_list = []
     initial_state,final_item_list = Closure(I,Original_Productions,final_item_list) 
     #Go_To()
     count = 0
     C.append(initial_state)
     state_list = []
     states = OrderedDict()
     states['I'+str(count)] = C[0] 
     counter = 0
     Relation_state = OrderedDict() 
     relation = set()
     while(1):
           
           temp_len = len(C)
           for I in copy.copy(C):                
                temp = counter 
                for X in Grammar_Symbol:     
                     result , final_item_list = Go_To(I,X,Original_Productions,final_item_list)
                     if( (not is_empty(result)) and (result not in C)):                          
                          count = count + 1
                          states['I'+str(count)] = result
                          state_list.append((I,'I'+str(count),X))
                          C.append(result)
                          #Relation_state[str(X)] = ('I'+str(temp) , 'I' +str(count))
                     elif(result in C): 
                               for state in states:
                                    if(states[state] == result):
                                           res_state = state  
                                           tup  = (I,res_state,X)
                                           if(tup not in state_list):
                                                 state_list.append(tup)

                     """    
                     elif(is_empty(result)):
                          if(X is not Start_symbol):
                                  for state in states:
                                      if(states[state] == I):
                                              final_item.add(state)
                     """
                                                               
           if(temp_len == len(C)):
           	break
     new_state_list = []
     final_item = OrderedDict()
     for each_tup in state_list:         
            state = each_tup[1]
            X = each_tup[2]
            for item in states:
                    if(states[item] == each_tup[0]):
                            var = item 
                            new_state_list.append((var, state,X))
      
       
     for each_state in states:
         for item in final_item_list:
              if(states[each_state] == item[0]):
                  #if((each_state,item[1] not in final_item):
                  final_item[each_state] = item[1] 
                  break

     return states , Grammar_Symbol,new_state_list,final_item



grammar1 = CFG.fromstring("""
         E -> E "+" E
         E -> E "*" E
         E -> "(" E ")"
         E -> "i"
""")

Productions  = grammar1.productions()
Start_symbol = grammar1.start()
Cononical_Collections_items(Start_symbol,Productions)

