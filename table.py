import Tkinter as tk
from CFG import LR_Parsing_table
from nltk.grammar import Nonterminal, Production, CFG
from Cononical_LR_item import is_nonterminal,get_all_items

class ExampleApp(tk.Tk):
    def __init__(self,Parsing_table,symbol_list):
        tk.Tk.__init__(self)
        t = SimpleTable(self,Parsing_table,symbol_list)
        t.pack(side="top", fill="x")
        t.set(0,0,"States")


class SimpleTable(tk.Frame):
    def __init__(self,parent,Parsing_table,symbol_list):
        # use black background so it "peeks through" to 
        # form grid lines
        symbol_list.insert(0,"states")
        self.rows = len(Parsing_table)+1
        self.columns = len(symbol_list)

        tk.Frame.__init__(self, parent, background="black")
        self._widgets = []
        self.Parsing_table = Parsing_table
        self.symbol_list = symbol_list

        for row in range(self.rows):
            current_row = []
            for column in range(self.columns):
                if(row == 0):
	                label = tk.Label(self, text="%s" % (symbol_list[column]), 
                                 borderwidth=0, width=10)
	                label.grid(row=row, column = column, sticky="nsew", padx=1, pady=1)
	                current_row.append(label)


                elif(row != 0 and column == 0):
	                label = tk.Label(self, text="%s" % (row-1), 
                                 borderwidth=0, width=10)
	                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
	                current_row.append(label)

                else: 
                        try:
		                val = Parsing_table[row-1]
		                val = val[symbol_list[column]]
			        label = tk.Label(self, text="%s" % (val),borderwidth=0, width=10)
			        label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
			        current_row.append(label)
                        except:
                                 label = tk.Label(self, text="%s" % ('None'), borderwidth=0, width=10)
			         label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
			         current_row.append(label)


            self._widgets.append(current_row)

        for column in range(self.columns):
            self.grid_columnconfigure(column, weight=1)


    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)


def create_table(grammar):

    Parsing_table,Cononical_symbol,relation_list = LR_Parsing_table(grammar)
    Grammar_symbol = get_all_items(grammar.productions())
    action_list = []
    go_to_list  = []

    for symbol in Grammar_symbol:
	 if(is_nonterminal(symbol)):
	       go_to_list.append(symbol)
	 else:
	       action_list.append(symbol)

    symbol_list = action_list+go_to_list
    app = ExampleApp(Parsing_table,symbol_list)
    app.mainloop()
