from Tkinter import Tk, Button, Label, Entry, OptionMenu, StringVar
from Tkinter import Radiobutton
import Tkinter as tk


class Error():

    '''
    Instance of this class is created and used by prog_tf.py only whenever
    there is an error in the netlist entered by the user.
    '''
    def __init__(self, msg):
        self.err_msg = msg
        print(self.err_msg)
        self.root = Tk()
        self.decision = ''
        self.root.title("Re-enter Netlist?")
        self.options()
        self.root.mainloop()

    def options(self):

        '''
        This function creates radiobuttons which asks the user if s/he wants
        to continue or not. Depending on the decision of the user prog_tf.py
        takes appropriate actions.
        If Yes- Input_screen will be called again and the user is asked to
                enter a new netlist again
        If No- Program terminates.
        '''
        self.v = StringVar()
        Label(self.root, text=self.err_msg).grid(row=0, column=0, sticky='news')
        Radiobutton(self.root, text="Yes", variable=self.v, value="Yes",
                    command=self.close).grid(row=1, column=0, sticky=tk.W,
                                             pady=4)
        Radiobutton(self.root, text="No", variable=self.v, value="No",
                    command=self.close).grid(row=2, column=0, sticky=tk.W,
                                             pady=4)

    def close(self):

        '''
        Closes the Re-enter window after displaying appropriate message to the
        terminal.
        '''
        self.decision = str(self.v.get())
        if self.decision == "Yes":
            print("You chose to re-enter")
        else:
            print("You chose to quit")
        self.root.destroy()


class Input_screen():
    def __init__(self):
        self.origin_node_list = []
        self.destination_node_list = []
        self.element_type_list = []
        self.element_value_list = []
        self.origin_list = []
        self.destination_list = []
        self.ele_type = []
        self.val_list = []
        self.error_msg = ""
        self.error_flag = 0
        self.root = Tk()
        self.root.title("Enter the netlist")
        self.accept_number_of_elements()
        # self.check_netlist_error()
        self.root.mainloop()

    def accept_number_of_elements(self):

        """
        Asks the user for the number of elements in the circuit. Updates the
        GUI window accordingly in the function self.show_rows()
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
        Depending on the number of elements entered by the user, this function
        creates appropriate number of rows in the window for entering the
        information about the elements present in the circuit.
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
        Depending on the input of the user via the GUI, this function creates
        lists of the data entered. The lists created are as follows:-
        origin_list - Stores all the origin nodes f netlist
        destination_list - Stores all the destination nodes of netlist
        val_list- Stores the values of the different elements of circuit
        ele_type- Stores the types of passive elements in circuit
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
        self.check_netlist_error()

    def check_netlist_error(self):

        '''
        Handles exceptions that may arise due to errors in netlist input by
        user.
        List of exceptions handled are:-
            -Negative value of nodes
            -No voltage sources in netlist
            -Negative/Zero value of R,L,C
            -Zero value of V
        If negative value of the voltage source is given the origin and
        destination nodes of the source are reversed for computational
        simplicity

        Whenever an error is encountered in the netlist error_flag is set 1
        An error_msg is also created appropriately. Both of these are handled
        by the program prog_tf.py
        '''
        if len(self.ele_type) < len(self.val_list):
            self.error_flag = 1
            self.error_msg = "You have not entered all identifiers."
            self.root.destroy()
            return
        check_source = len([1 for x in self.ele_type if 'V' in x])
        if check_source == 0:
            self.error_flag = 1
            self.error_msg = "You have forgotten to enter sources"
            self.root.destroy()
            return
        check_negative_origin = any(n < 0 for n in self.origin_list)
        check_negative_dest = any(n < 0 for n in self.destination_list)
        if check_negative_dest == True or check_negative_origin == True:
            self.error_msg = "Negative value of node."
            self.error_flag = 1
            self.root.destroy()
            return
        for ind in range(len(self.val_list)):
            if self.val_list[ind] <= 0 and 'V' not in self.ele_type[ind]:
                self.error_msg = "Non-positive value of R/L/C"
                self.error_flag = 1
                self.root.destroy()
                return
            if self.val_list[ind] == 0:
                self.error_msg = "Zero value"
                self.error_flag = 1
                self.root.destroy()
                return
            if self.val_list[ind] < 0 and 'V' in self.ele_type[ind]:
                # print("Reversing polarity of voltage source")
                self.val_list[ind] = abs(self.val_list[ind])
                o, d = self.origin_list[ind], self.destination_list[ind]
                self.origin_list[ind], self.destination_list[ind] = d, o
        self.root.destroy()

if __name__ == '__main__':
    new = Input_screen()
