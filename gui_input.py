from Tkinter import *

def store_entry_fields():
    
    '''This function takes each Tkinter entry and creates 4 lists which describes the netlist
    from_list-contains a list of all the from nodes
    to_list-contains a list of all the to nodes
    ele_type-contains a list of the identifiers of all the passive elements
    val_list-contains a list of all the values
    '''
    volt,res,ind,cap = 0,0,0,0
    global from_list
    global to_list
    global ele_type
    global val_list
    from_list,to_list,ele_type,val_list=[],[],[],[]
    for i in from_node:
        from_list.append(int(i.get()))

    for i in to_node:
        to_list.append(int(i.get()))

    for i in val:
        val_list.append(float(i.get()))

    for i in type_el:
        if i.get() == "Voltage Source":
            volt += 1
            ele_type.append('V' + str(volt))
        elif i.get() == "Resistance":
            res += 1
            ele_type.append('R' + str(res))
        elif i.get() == "Inductance":
            ind += 1
            ele_type.append('L' + str(ind))
        elif i.get() == "Capacitance":
            cap += 1
            ele_type.append('C' + str(cap))
    top.destroy()
    
def show_fields():

    '''First the user has to give the number of elements in his/her circuit. 
    Depending on the number of elements the number of rows in the netlist
    is decided. This function gets this value from the user and creates three
    fields for From node, To node and value. Type of the element is provided 
    as an option
    '''
    global from_node
    global to_node
    global type_el
    global val
    from_node,to_node,type_el,val=[],[],[],[]
    num_el = int(num_el_field.get())
    Label(top,text="From").grid(row=1, column=0, sticky='news')
    Label(top,text="To").grid(row=1, column=1, sticky='news')
    Label(top,text="Value").grid(row=1, column=3, sticky='news')
  
    for i in range(1,num_el+1):

        f = Entry(top,width=33)
        f.grid(row=i+1, column=0, sticky='news')
        from_node.append(f)
  
        Label(top,text='---').grid(row=i+1, column=1, sticky='news')
        t = Entry(top,width=33)
        t.grid(row=i+1, column=1, sticky='news')
        to_node.append(t)
  
        type_el.append(StringVar(top))
        OptionMenu(top,type_el[i-1], "Voltage Source","Resistance", 
                        "Inductance", "Capacitance").grid(row=i+1, column=2, sticky='news')

        v = Entry(top,width=33)
        v.grid(row=i+1, column=3, sticky='news')
        val.append(v)
    Button(top,text='Save', command=store_entry_fields).grid(row=num_el+2, column=2, sticky=W, pady=4)

def enter_number_of_elements():

    ''' 
    The field for entering the number of circuit elemnents is created 
    in this function
    '''
    Label(top,text="Enter the number of Elements:").grid(row=0,column=0,sticky='news')
    global num_el_field
    num_el_field = Entry(top, width=4)
    num_el_field.grid(row=0, column=1, sticky='news') 
    Button(top, text='Show', command=show_fields).grid(row=0, column=2, sticky=W, pady=4)

def main():

    '''List containing all the origin nodes: from_list
    List containing all the destination nodes:to_list
    List containing all the values:val_list
    List containing all the identifiers:ele_type
    '''
    global top
    top = Tk()
    top.title("Enter The parameters")
    enter_number_of_elements()
    top.mainloop()

if __name__ == '__main__':
    main()
