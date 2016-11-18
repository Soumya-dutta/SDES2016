from Tkinter import Tk, Button, IntVar, StringVar, Label, Radiobutton
import Tkinter as tk


class Input_selection():
    """Class for creating GUI for input selection by user
    Methods in class:
    -----------------
    __init__ - initializes the different class variables as follows:
               root- A Tkinter window where the GUI will be shown
               passive_element_list - A list storing the different circuit
                                      elements in the netlist
               element_values - A list storing all the values of circuit
                                elements
               num_volt_sources - number if voltage sources in the circuit

    options_input - Depending on the number of voltage sources in the circuit
                    the user is given options of selecting any one of them.
                    This choice is given by a Radiobutton. After selection, the
                    user has to confirm his/her selection by clicking on
                    Confirm selection of input.
    compute_val - After user selects an input, the value of the required
                  identifier is read from the list and stored in the variable
                  inpval.
    """
    def __init__(self, identifiers, values, number_of_options):
        self.root = Tk()
        self.passive_element_list = identifiers
        self.element_values = values
        self.num_volt_sources = number_of_options
        self.root.title("Select your input for transfer function")
        self.options_input()
        self.root.mainloop()

    def options_input(self):
        self.v = IntVar()
        Label(self.root, text="Options for input").grid(row=0, column=0,
                                                        sticky='news')
        for ind in range(self.num_volt_sources):
            Radiobutton(self.root, text="V"+str(ind+1), variable=self.v,
                        value=ind+1).grid(row=ind+1, column=0, sticky=tk.W,
                                          pady=4)
        Button(self.root, text="Confirm selection of input",
               command=self.compute_val).grid(row=ind+4, column=0, sticky=tk.W,
                                              pady=4)

    def compute_val(self):
        ind = self.passive_element_list.index("V"+str(self.v.get()))
        self.inpval = self.element_values[ind]
        self.root.destroy()


class Output_selection():
    """Class creates a GUI for providing different output selection options
    to user
    Methods in class:
    -----------------
    __init__ - initializes the different class variables as follows:
               root- A Tkinter window where the GUI will be shown
               element_list - A list storing the different circuit
                              elements in the netlist
    options_output - Provides options to user for selecting output as
                     either voltage/current in any of the elements
    output_selected - creates two variables ele_identifier and output_type.
                      If user wants to have "Current though L1 as output"
                      ele_identifier is set to "L1"
                      output_type is set to "I"
    """
    def __init__(self, identifiers):
        self.root = Tk()
        self.element_list = identifiers
        self.root.title("Select your output for transfer function")
        self.options_output()
        self.root.mainloop()

    def options_output(self):
        self.v = StringVar()
        Label(self.root, text="Options for output").grid(row=0, column=0,
                                                         sticky='news')
        for ind in range(len(self.element_list)):
            Radiobutton(self.root, text="Voltage across " +
                        self.element_list[ind], variable=self.v, value="V:" +
                        self.element_list[ind]).grid(row=ind+1, column=0,
                                                     sticky=tk.W, pady=4)
            Radiobutton(self.root, text="Current through " +
                        self.element_list[ind], variable=self.v, value="I:" +
                        self.element_list[ind]).grid(row=ind+1, column=1,
                                                     sticky=tk.W, pady=4)
        Button(self.root, text="Confirm selection of output",
               command=self.output_selected).grid(row=len(self.element_list)+2,
                                                  column=0, sticky=tk.W,
                                                  pady=4)

    def output_selected(self):
        l = str(self.v.get()).split(':')
        self.ele_identifier = l[1]
        self.output_type = l[0]
        self.root.destroy()
