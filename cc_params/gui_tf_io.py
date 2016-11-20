"""
Create GUI interface for user to select input and output for transfer function.

Displays options to the user to select the input and output from the circuit
to be considered for transfer function computation.
"""
from Tkinter import Tk, Button, IntVar, StringVar, Label, Radiobutton
import Tkinter as tk


class Input_selection():
    """Class for creating GUI for input selection by user."""

    def __init__(self, identifiers, values, number_of_options):
        """
        Initialize Instance of class Input_selection.

        **Parameters**

        - identifiers: list of types of elements in the circuit
        - values: list of element values in the circuit
        - number_of_options: number of voltage sources in circuit.

        A GUI with title Select your input for transfer function is created.
        """
        self.root = Tk()
        self.passive_element_list = identifiers
        self.element_values = values
        self.num_volt_sources = number_of_options
        self.root.title("Select your input for transfer function")
        self.options_input()
        self.root.mainloop()

    def options_input(self):
        """
        Input is selected by the user from options provided via radiobuttons.

        If there are *n* voltage sources in the circuit, *n* radiobuttons are
        given as optons to the user. The user can select any one and then
        clicks on Confirm selection of input.
        """
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
        """Value of the voltage source selected by user is stored in inpval."""
        ind = self.passive_element_list.index("V"+str(self.v.get()))
        self.inpval = self.element_values[ind]
        self.root.destroy()


class Output_selection():
    """Class for creating GUI for output selection by user."""

    def __init__(self, identifiers):
        """
        Initialize Instance of class Output_selection.

        **Parameters**

        - identifiers: list of types of elements in the circuit.

        A GUI with title Select your output for transfer function is created.
        """
        self.root = Tk()
        self.element_list = identifiers
        self.root.title("Select your output for transfer function")
        self.options_output()
        self.root.mainloop()

    def options_output(self):
        """
        Output is selected by the user from options provided via radiobuttons.

        Options are provided for selecting current through any element or
        voltage across any element.
        """
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
        """
        Store the output selected by user.

        Both the element and the type of output is stored.
        For eg: if **current** through resistance **R1** is demanded then
        self.ele_identifier is set to **R1**
        self.output_type is set to **I**
        """
        l = str(self.v.get()).split(':')
        self.ele_identifier = l[1]
        self.output_type = l[0]
        self.root.destroy()
