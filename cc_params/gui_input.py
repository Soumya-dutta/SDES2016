"""
Create GUI interface for the user to enter the netlist.

Also gives the option re-entering netlist if entered netlist is erroneous.
"""
from Tkinter import Tk, Button, Label, Entry, OptionMenu, StringVar
from Tkinter import Radiobutton
import Tkinter as tk


class Error():
    """
    Handles if error is present in the circuit/netlist.

    Gives the option of re-entering.

    ``Parameters``

    - msg: error message to inform the user of the error in the circuit

    """

    def __init__(self, msg):
        """
        Initialize an Instance of the class Error.

        Creates a GUI window with title Re-enter Netlist?
        """
        self.err_msg = msg
        print(self.err_msg)
        self.root = Tk()
        self.decision = ''
        self.root.title("Re-enter Netlist?")
        self.options()
        self.root.mainloop()

    def options(self):
        """
        Create radio buttons for accepting user input.

        Radiobutton Yes is created for user to re-enter netlist
        Radiobutton No is created for user to quit.
        """
        self.v = StringVar()
        Label(self.root, text=self.err_msg).grid(row=0, column=0, sticky='news')
        Radiobutton(self.root, text="Yes", variable=self.v, value="Yes",
                    command=self.close).grid(row=1, column=0, sticky=tk.W,
                                             pady=4)
        Radiobutton(self.root, text="No", variable=self.v, value="No",
                    command=self.close).grid(row=2, column=0, sticky=tk.W,
                                             pady=4)

    def close(self):
        """
        Close window after dispalying appropriate information.

        If user chooses to continue the decision variable is set to Yes and
        the user has to re-enter netlist, else the program quits.
        """
        self.decision = str(self.v.get())
        if self.decision == "Yes":
            print("You chose to re-enter")
        else:
            print("You chose to quit")
        self.root.destroy()


class Input_screen():
    """
    Create an input interface for the user to enter netlist.

    Asks user for number of elements in the circuit. Creates a table sort of
    input interface for the user for entering the netlist. Errors are also
    checked.

    ``Variables``

    - origin_node_list[]: list of originating nodes as Tkinter objects

    - destination_node_list[]: list of terminating nodes as Tkinter objects

    - element_type_list[]: list of types of element as Tkinter objects

    - element_value_list[]: list of values of element as Tkinter objects

    - origin_list[]: list of originating nodes in circuit

    - destination_list[]: list of terminating nodes in circuit

    - ele_type[]: list of element types in circuit

    - val_list[]: list of element values in circuit

    - error_msg: stores the error message in case there is an error

    - error_flag: set to 1 if there is an error else 0

    """

    def __init__(self):
        """
        Initialize Instance of class Input_screen.

        Create GUI window with title Enter the netlist
        """
        self.origin_node_list = []
        self.destination_node_list = []
        self.element_type_list = []
        self.element_value_list = []
        self.origin_list = []
        self.destination_list = []
        self.ele_type = []
        self.val_list = []
        self.root = Tk()
        self.root.title("Enter the netlist")
        self.accept_number_of_elements()
        self.root.mainloop()

    def accept_number_of_elements(self):
        """
        Accept number of elements in the circuit from user.

        the number entered by user is stored in the variable num_el_field.
        function show_rows() is called subsequently.
        """
        Label(self.root, text="Enter number of Elements:").grid(row=0,
                                                                column=0,
                                                                sticky='news')
        self.num_el_field = Entry(self.root, width=4)
        self.num_el_field.grid(row=0, column=1, sticky='news')
        Button(self.root, text='Show', command=self.show_rows).grid(row=0,
                                                                    column=2,
                                                                    sticky=tk.W,
                                                                    pady=4)

    def show_rows(self):
        """
        User enters netlist in rows provided based on number of elements.

        The user has to enter the netlist under the following heads

        - From: Origin node of elements

        - To: Destination node of elements

        - Type of element to be selected from drop-down menu

        - Value: Value of the element entered.

        Once netlist is entered user has to click on Save to load the netlist.
        """
        num_el = int(self.num_el_field.get())
        Label(self.root, text="From").grid(row=1, column=0, sticky='news')
        Label(self.root, text="To").grid(row=1, column=1, sticky='news')
        Label(self.root, text="Value").grid(row=1, column=3, sticky='news')
        for i in range(1, num_el+1):
            origin = Entry(self.root, width=33)
            origin.grid(row=i+1, column=0, sticky='news')
            self.origin_node_list.append(origin)
            Label(self.root, text='---').grid(row=i+1, column=1, sticky='news')
            dest = Entry(self.root, width=33)
            dest.grid(row=i+1, column=1, sticky='news')
            self.destination_node_list.append(dest)
            self.element_type_list.append(StringVar(self.root))
            OptionMenu(self.root, self.element_type_list[i-1],
                       "Voltage Source in Volts", "Resistance in Ohm",
                       "Inductance in Henry",
                       "Capacitance in Farad").grid(row=i+1, column=2,
                                                    sticky='news')
            value = Entry(self.root, width=33)
            value.grid(row=i+1, column=3, sticky='news')
            self.element_value_list.append(value)
        Button(self.root, text='Save',
               command=self.store_entry_fields).grid(row=num_el+2, column=2,
                                                     sticky=tk.W, pady=4)

    def store_entry_fields(self):
        """
        Store the netlist data in the form of lists.

        The lists created are as follows:-

        - origin_list : Stores all the origin nodes of netlist

        - destination_list : Stores all the destination nodes of netlist

        - val_list : Stores the values of the different elements of circuit

        - ele_type : Stores the types of passive elements in circuit

        """
        volt, res, ind, cap = 0, 0, 0, 0
        for i in self.origin_node_list:
            self.origin_list.append(int(i.get()))
        for i in self.destination_node_list:
            self.destination_list.append(int(i.get()))
        for i in self.element_value_list:
            self.val_list.append(float(i.get()))
        for i in self.element_type_list:
            if i.get() == "Voltage Source in Volts":
                volt += 1
                self.ele_type.append('V' + str(volt))
            elif i.get() == "Resistance in Ohm":
                res += 1
                self.ele_type.append('R' + str(res))
            elif i.get() == "Inductance in Henry":
                ind += 1
                self.ele_type.append('L' + str(ind))
            elif i.get() == "Capacitance in Farad":
                cap += 1
                self.ele_type.append('C' + str(cap))
        self.root.destroy()


if __name__ == '__main__':
    new = Input_screen()
