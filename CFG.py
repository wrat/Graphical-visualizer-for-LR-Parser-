import re
import nltk
from nltk.grammar import Nonterminal, Production,CFG
from Cononical_LR_item import Cononical_Collections_items,is_nonterminal,get_all_items
from collections import OrderedDict

def get_entry(state,symbol,relation):
      for each_relation in relation:
           
          if((each_relation[0] == state) and (symbol is each_relation[2])):
             return each_relation[1]  

def Analyze_rhs(rhs,Productions):
    Grammar_symbol = get_all_items(Productions)
    new_rhs = [] 
    for ele in rhs: 
         if(str(ele) in Grammar_symbol):
               new_rhs.append(str(ele))
         else:
	 	new_rhs.append(ele)
    return new_rhs
    

def get_production(Productions,state):
    
    string_repr = state.__repr__()
    lhs = str(state.lhs())
    rhs_str = list(state.rhs())
    rhs_list = []
    for i in rhs_str:
       rhs_list.append(str(i))
     
    string_repr = "".join(rhs_list)
    string_repr = string_repr.replace(".","")
    rhs = []
    for item in string_repr:
          rhs.append(Nonterminal(item))
    
    rhs = Analyze_rhs(rhs,Productions)
    
    new_production = Production(state.lhs(),rhs) 
    for (_production_,count) in zip(Productions,range(len(Productions))):
          
          if(_production_ == new_production):
               return count+1


def LR_Parsing_table(grammar):

        
	Productions  = grammar.productions()
	Start_symbol = grammar.start()
	Cononical_symbol , Grammar_symbol , relation_list ,final_item = Cononical_Collections_items(Start_symbol,Productions)
	Parsing_table = OrderedDict()
	Action = OrderedDict()
	Go_to = OrderedDict()
	final_item_state_list = []
	Lookup_parsing_table = OrderedDict()
	go_to_list = []
	action_list = []
        

	for symbol in Grammar_symbol:
	      if(is_nonterminal(symbol)):
		  Go_to[symbol] = []
		  go_to_list.append(symbol)
	      else:
		 Action[symbol] = []
		 action_list.append(symbol)

	action_list.append('$')
	Parsing_table['Column'] = ('Action','Go_To')
	Parsing_table['Element'] = (action_list,go_to_list)


	for state in Cononical_symbol:
	       Parsing_table[state] = []		                                  

	for symbol in Grammar_symbol:
	      if(is_nonterminal(symbol)):
		  Go_to[symbol] = []
	      else:
		 Action[symbol] = []

	Action['$'] = []


	for state in Parsing_table:

	      all_items = OrderedDict()
	      if(state == 'Column' or state == 'Element'):
		    continue
               
	      #if state is Final state
	      if(state in final_item.keys()):                   
		   action_entry = []
		   go_to_entry  = []
		   if(1):
		      for action in Action:
                          if(state == 'I1'):
                              if(action == '$'):
                              	action_entry.append('accept')
                              	all_items['$'] = 'accept'
                                continue

                              entry = get_entry(state,action,relation_list)
                              if(entry):
                                if(len(entry) > 2):
                                    var = entry[1] + entry[2]
                                else:
                                    var = entry[1]

		              	action_entry.append('S' + var) 
		              	all_items[action] = 'S' + var                            
                              continue

		          entry = get_production(Productions,final_item[state])                                          
		          action_entry.append('r'+str(entry)) 
		          all_items[action] = 'r'+str(entry)  

		      for go_to in Go_to:
                            entry = get_entry(state,go_to,relation_list)
                            if(entry):
                                if(len(entry) > 2):
                                    var = int(entry[1] + entry[2])
                                else:
                                    var = int(entry[1])
		          	go_to_entry.append(var)      
		          	all_items[go_to] = var
                            else:
		            	go_to_entry.append('None')
		            	all_items[go_to] = 'None'
  
		   Parsing_table[state].append((action_entry,go_to_entry))
                   if(len(state) > 2):                       
                       var = state[1] + state[2]
                       Lookup_parsing_table[int(var)] = all_items
                       continue

                   Lookup_parsing_table[int(state[1])] = all_items
		   continue 


	      #Fill Action Operation
	      action_entry = []
	      for action in Action:
		    
		    entry = get_entry(state,action,relation_list)
		    if(entry):

                        if(len(entry) > 2):
                               var = entry[1] + entry[2]
                        else:
                               var = entry[1]

		        action_entry.append('S' + var)
		        all_items[action] =  'S' + var
 
		    if(action is '$'):
		            action_entry.append('None')
		            all_items['$'] = 'None'      

	      #for go_to entry:
	      go_to_entry = []
	      for go_to in Go_to:
		   entry = get_entry(state,go_to,relation_list)
		   if(entry):
                        if(len(entry) > 2):
                              var = int(entry[1] + entry[2])
                        else:
                              var = int(entry[1])

		        go_to_entry.append(var)      
		        all_items[go_to] = var
		   else:  
		          go_to_entry.append('None')
		          all_items[go_to] = 'None' 
	      Parsing_table[state].append((action_entry,go_to_entry))
              if(len(state) > 2):
                  var = state[1] + state[2]
                  Lookup_parsing_table[int(var)] = all_items
                  continue

	      Lookup_parsing_table[int(state[1])] = all_items
        

        return Lookup_parsing_table,Cononical_symbol,relation_list


'''
grammar1 = CFG.fromstring("""
         R -> R "+" R
         R -> R R
         R -> R "^"
         R -> "(" R ")"
         R -> "a"
         R -> "b" 
""")

print(LR_Parsing_table(grammar1))
'''



