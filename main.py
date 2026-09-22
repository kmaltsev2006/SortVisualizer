import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from random import randint, shuffle
import threading
import time
import perform
import measure
import graph_builder
import time_algs
import global_namespace as gn

unique_items_num = 0
last_num = 0
session_number = 0

def allocator(name):
    match name:
        case 'None':
            return (perform.none_function, measure.none_function, time_algs.none_function)
        case 'Bubble Sort':
            return (perform.perform_bubble_sort, measure.measure_bubble_sort, time_algs.time_bubble_sort)
        case 'Insertion Sort':
            return (perform.perform_insertion_sort, measure.measure_insertion_sort, time_algs.time_insertion_sort)
        case 'Selection Sort':
            return (perform.perform_selection_sort, measure.measure_selection_sort, time_algs.time_selection_sort)
        case 'Quick Sort':
            return (perform.perform_quick_sort, measure.measure_quick_sort, time_algs.time_quick_sort)
        case 'Merge Sort':
            return (perform.perform_merge_sort, measure.measure_merge_sort, time_algs.time_merge_sort)
        case 'Shaker Sort':
            return (perform.perform_shaker_sort, measure.measure_shaker_sort, time_algs.time_shaker_sort)
        case 'Gnome Sort':
            return (perform.perform_gnome_sort, measure.measure_gnome_sort, time_algs.time_gnome_sort)
        case 'Odd-Even Sort':
            return (perform.perform_odd_even_sort, measure.measure_odd_even_sort, time_algs.time_odd_even_sort)
        case 'Comb Sort':
            return (perform.perform_comb_sort, measure.measure_comb_sort, time_algs.time_comb_sort)
        case 'Heap Sort':
            return (perform.perform_heap_sort, measure.measure_heap_sort, time_algs.time_heap_sort)
        case 'Tim Sort':
            return (perform.perform_tim_sort, measure.measure_tim_sort, time_algs.time_tim_sort)
        case 'IntroSort':
            return (perform.perform_introsort, measure.measure_introsort, time_algs.time_introsort)
        case 'Shell Sort':
            return (perform.perform_shell_sort, measure.measure_shell_sort, time_algs.time_shell_sort)
        case 'Count Sort':
            return (perform.perform_count_sort, measure.measure_count_sort, time_algs.time_count_sort)
        case 'Radix Sort':
            return (perform.perform_radix_sort, measure.measure_radix_sort, time_algs.time_radix_sort)

class MyLabelFrame(tk.LabelFrame):
    
    def __init__(self, master, *args, **kwargs):
        super(MyLabelFrame, self).__init__(master, *args, **kwargs)


class DataItem:
    
    def __init__(self, name):
        self.name = name    # Name
        self.Vtime = 0      # Vizual Time (sec)
        self.Stime = 0      # Sort Time (ms)
        self.cmp = 0        # Comparisons
        self.swaps = 0      # Swaps
        self.Mwrites = 0    # Writes to Main Array
        self.Awrites = 0    # Writes to Auxiliary Array


class DataFrame(MyLabelFrame):
    
    def __init__(self, master, *args, **kwargs):
        super(DataFrame, self).__init__(master, bg='#000000', *args, **kwargs)
        
        self.Stime = LabelEntry(self, label_text='Sort Time (ms):', entry_text='?', bg='#000000')
        self.Stime.label.configure(bg='#000000', fg='#FFFFFF')
        self.Stime.entry.configure(bg='#000000', fg='#FFFFFF', disabledbackground='#000000', disabledforeground='#FFFFFF', width='16')
        self.Stime.create_widgets()
        self.Stime.grid(row=0, column=0, sticky='w')
        
        self.cmp = LabelEntry(self, label_text='Comparisons:', entry_text='?', bg='#000000')
        self.cmp.label.configure(bg='#000000', fg='#FFFFFF')
        self.cmp.entry.configure(bg='#000000', fg='#FFFFFF', disabledbackground='#000000', disabledforeground='#FFFFFF', width='16')
        self.cmp.create_widgets()
        self.cmp.grid(row=1, column=0, sticky='w')
        
        self.swaps = LabelEntry(self, label_text='Swaps:', entry_text='?', bg='#000000')
        self.swaps.label.configure(bg='#000000', fg='#FFFFFF')
        self.swaps.entry.configure(bg='#000000', fg='#FFFFFF', disabledbackground='#000000', disabledforeground='#FFFFFF', width='16')
        self.swaps.create_widgets()
        self.swaps.grid(row=2, column=0, sticky='w')

        self.Mwrites = LabelEntry(self, label_text='Writes to Main Array:', entry_text='?', bg='#000000')
        self.Mwrites.label.configure(bg='#000000', fg='#FFFFFF')
        self.Mwrites.entry.configure(bg='#000000', fg='#FFFFFF', disabledbackground='#000000', disabledforeground='#FFFFFF', width='16')
        self.Mwrites.create_widgets()
        self.Mwrites.grid(row=3, column=0, sticky='w')
        
        self.Awrites = LabelEntry(self, label_text='Writes to Auxiliary Array:', entry_text='?', bg='#000000')
        self.Awrites.label.configure(bg='#000000', fg='#FFFFFF')
        self.Awrites.entry.configure(bg='#000000', fg='#FFFFFF', disabledbackground='#000000', disabledforeground='#FFFFFF', width='16')
        self.Awrites.create_widgets()
        self.Awrites.grid(row=4, column=0, sticky='w')


class CellFrame(MyLabelFrame):
    
    def __init__(self, master, array, name, *args, **kwargs):
        super(CellFrame, self).__init__(master, *args, **kwargs)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.array1 = array.copy() # perform
        self.array2 = array.copy() # measure
        self.name = name
        self.perform_function, self.measure_function = allocator(self.name)[0], allocator(self.name)[1]
        if (name != 'None'):
            perform.waiting += 1
            measure.waiting += 1
        self.data_item = DataItem(name)
        self.specials = dict()
        self.last_rendered = 0
        self.create_widgets()
        self.create_thread()
    
    def create_widgets(self):
        self.name_entry = StaticEntry(self, 
                                      text=self.name + ' (Waiting)' if (self.name != 'None') else 'None', justify='center', 
                                      bg='#000000', fg='#FFFFFF', 
                                      disabledbackground='#000000', disabledforeground='#FFFFFF', 
                                      highlightbackground='#FFFFFF', highlightcolor='#FFFFFF', highlightthickness=1)
        self.name_entry.change_text(self.name + ' (Waiting)' if (self.name != 'None') else 'None')
        self.name_entry.grid(row=0, column=0, sticky='nswe')
        self.bottom_canvas = tk.Canvas(self, width=0, height=0, bg='#000000', highlightbackground='#FFFFFF', highlightthickness=1)
        self.bottom_canvas.grid(row=1, column=0, sticky='nswe')
        self.top_canvas = tk.Canvas(self, width=0, height=0, bg='#000000', highlightbackground='#FFFFFF', highlightthickness=1)
        self.top_canvas.grid(row=1, column=0, sticky='nswe')
        self.data_frame = DataFrame(self, bd=0, highlightbackground='#FFFFFF', highlightthickness=1)
        self.data_frame.grid(row=1, column=0, sticky='nswe')
        self.data_frame.grid_remove()
    
    def create_thread(self):
        self.perform_thread = threading.Thread(target=self.perform_function, args=(self, ), daemon=True)


class Graph:
    
    def __init__(self, array_type, percent_unique):
        self.array_type = array_type
        self.percent_unique = percent_unique
        self.items = []
        self.X = []
        self.mn = 1e9


class GraphItem:
    
    def __init__(self, function, name):
        self.function = function
        self.name = name
        self.Y1 = []
        self.Y2 = []


class DisplayFrame(MyLabelFrame):
    
    def __init__(self, master, *args, **kwargs):
        super(DisplayFrame, self).__init__(master, *args, **kwargs)
        self.size = 0
        self.markup = []
        self.arr_type = ''
        self.arr_size = 0
        self.data = []
        self.bind('<Configure>', lambda e, obj=self: perform.draw_multiple_arrays(obj.size, obj.markup))
    
    def create_widgets(self, selected_algs, array):
        q = 0
        for i in range(self.size):
            self.markup.append([])
            self.rowconfigure(i, weight=1)
            for j in range(self.size):
                self.columnconfigure(j, weight=1)
                cell_frame = CellFrame(self, array=array.copy() if (q<len(selected_algs)) else [], 
                                       name=selected_algs[q]['text'] if (q<len(selected_algs)) else 'None', 
                                       bg='#000000', fg='#FFFFFF', bd=1)
                cell_frame.grid(row=i, column=j, sticky='nswe')
                self.markup[i].append(cell_frame)
                q += 1
    
    def create_coordinate_plane(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        coordinate_plane_frame = MyLabelFrame(self, bd=0)
        coordinate_plane_frame.grid(row=0, column=0, sticky='nswe')
        
        fig, ax = plt.subplots()
        plt.xlabel('Array Size')
        plt.ylabel('Time (ms)')
        plt.grid(which='major')
        plt.minorticks_on()
        plt.grid(which='minor', linestyle=':')
        self.canvas = FigureCanvasTkAgg(fig, master=coordinate_plane_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=1)
        
        toolbar_frame = MyLabelFrame(self, bd=0)
        toolbar_frame.grid(row=1, column=0, sticky='nswe')
        
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame, pack_toolbar=False)
        toolbar.update()
        toolbar.pack(side='left', fill='x', expand=1)

        
        self.graph_mode_button = GraphModeButton(toolbar_frame, text='Change Mode', state='disabled')
        self.graph_mode_button.configure(command=lambda obj=self.graph_mode_button: obj.on_click(self.canvas, None))
        self.graph_mode_button.pack(side='right', padx=[0, 10], ipadx=2, ipady=1)
    
    def destroy_widgets(self):
        for i in range(self.size):
            self.rowconfigure(i, weight=0)
            for j in range(self.size):
                self.columnconfigure(j, weight=0)
                self.markup[i][j].destroy()
        self.size = 0
        self.markup = []
        for child in self.winfo_children():
            child.destroy()


class ScrollFrame(MyLabelFrame):
    
    def __init__(self, master, *args, **kwargs):
        super(ScrollFrame, self).__init__(master, *args, **kwargs)
        wrap_canvas = tk.Canvas(self, width=0, height=0, highlightthickness=0)
        wrap_canvas.pack(side='left', fill='both', expand=1)
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=wrap_canvas.yview)
        scrollbar.pack(side='right', fill='y')
        wrap_canvas.configure(yscrollcommand=scrollbar.set)
        wrap_canvas.bind('<Configure>', lambda e, obj=wrap_canvas: obj.configure(scrollregion = obj.bbox('all')))
        self.field = tk.Frame(wrap_canvas)
        wrap_canvas.create_window((0,0), window=self.field, anchor='nw')


class MyLabel(tk.Label):
    
    def __init__(self, master, *args, **kwargs):
        super(MyLabel, self).__init__(master, *args, **kwargs)


class StaticEntry(tk.Entry):
    
    def __init__(self, master, text, *args, **kwargs):
        super(StaticEntry, self).__init__(master, relief='flat', cursor='arrow', state='disabled', *args, **kwargs)
        self.change_text(text)
        
    def change_text(self, text):
        self.configure(state='normal')
        self.delete(0, 'end')
        self.insert(0, text)
        self.configure(state='disabled')


class MyEntry(tk.Entry):
    
    def __init__(self, master, *args, **kwargs):
        super(MyEntry, self).__init__(master, validate='key', *args, **kwargs)
        self.current_value = 0
        vcmd = (self.register(self.validate), '%P')
        self.configure(validatecommand=vcmd)
        self.bind('<FocusIn>', lambda e, obj=self: obj.focus_in())
        self.bind('<FocusOut>', lambda e, obj=self: obj.focus_out())
        self.bind('<Escape>', lambda e, obj=self: obj.focus_out())
    
    def validate(self, new_value):
        return new_value == '' or new_value.isdigit()
        
    def focus_in(self):
        self.current_value = int(self.get())
        self.selection_range(0, 'end')    
    
    def focus_out(self):
        self.master.focus()
        self.delete(0, 'end')
        self.insert(0, self.current_value)

    def display_on_scale(self, scale, reverse):
        self.master.focus()
        val = max(int(scale['from']), min(int(scale['to']), int(self.get()))) if (self.get() != '') else int(scale['from'])
        self.current_value = val
        self.delete(0, 'end')
        self.insert(0, val)
        if (reverse):
            scale.set(int(scale['to']) - val)
        else:
            scale.set(val)


class DelayEntry(MyEntry):

    def __init__(self, master, *args, **kwargs):
        super(DelayEntry, self).__init__(master, *args, **kwargs)
    
    def set_delay(self, scale, reverse):
        self.display_on_scale(scale, reverse)
        perform.delay = self.current_value


class LabelEntry(MyLabelFrame):
    
    def __init__(self, master, label_text, entry_text, *args, **kwargs):
        super(LabelEntry, self).__init__(master, bd=0, *args, **kwargs)
        self.label = MyLabel(self, text=label_text, justify='left')
        self.entry = StaticEntry(self, text=entry_text, justify='left')
    
    def create_widgets(self, padx=[0, 0], pady=[0, 0]):
        self.label.grid(row=0, column=0, padx=[padx[0], 0], pady=pady, sticky='w')
        self.entry.grid(row=0, column=1, padx=[0, padx[1]], pady=pady, sticky='w')


class MyScale(tk.Scale):
    
    def __init__(self, master, *args, **kwargs):
        super(MyScale, self).__init__(master, orient='horizontal', resolution=1, variable=tk.IntVar(), showvalue=0, *args, **kwargs)
    
    def display_in_entry(self, entry, reverse):
        self.master.focus()
        entry.delete(0, 'end')
        if (reverse):
            entry.current_value = int(self['to'])-self.get()
        else:
            entry.current_value = self.get()
        entry.insert(0, entry.current_value)


class SpeedScale(MyScale):
    
    def __init__(self, master, *args, **kwargs):
        super(SpeedScale, self).__init__(master, *args, **kwargs)
    
    def set_delay(self, entry, reverse):
        self.display_in_entry(entry, reverse)
        perform.delay = entry.current_value


class MyButton(ttk.Button):
    
    def __init__(self, master, *args, **kwargs):
        super(MyButton, self).__init__(master, *args, **kwargs)


class GraphModeButton(MyButton):
    
    def __init__(self, master, *args, **kwargs):
        super(GraphModeButton, self).__init__(master, *args, **kwargs)
        self.mode = -1
    
    def on_click(self, canvas, graph):
        self.master.focus()
        if (self.mode == -1):
            return
        self.mode = 1-self.mode
        plt.cla()
        plt.xlabel('Array Size')
        plt.ylabel('Time (ms)')
        plt.grid(which='major')
        plt.minorticks_on()
        plt.grid(which='minor', linestyle=':')
        if (self.mode == 0):
            plt.title('With Fluctuation')
        if (self.mode == 1):
            plt.title('Approximated')
        for i in range(len(graph.items)):
            if (self.mode == 0):
                plt.plot(graph.X[:graph.mn], graph.items[i].Y1[:graph.mn], label=graph.items[i].name)
            if (self.mode == 1):
                plt.plot(graph.X[:graph.mn], graph.items[i].Y2[:graph.mn], label=graph.items[i].name)
        plt.legend()
        canvas.draw()


class AlgButton(MyButton):
    def __init__(self, master, idx, *args, **kwargs):
        super(AlgButton, self).__init__(master, *args, **kwargs)
        self.configure(style='default.TButton')
        self.idx = idx
        self.selected = False
        
    def on_click(self, selected_algs):
        self.master.focus()
        if (not(self.selected)):
            selected_algs.append(self)
            self.configure(style='selectedB.TButton')
            self.selected = True
        else:
            selected_algs.pop(selected_algs.index(self))
            self.configure(style='default.TButton')
            self.selected = False


class ResetButton(MyButton):
    
    def __init__(self, master, *args, **kwargs):
        super(ResetButton, self).__init__(master, *args, **kwargs)
    
    def on_click(self, display_frame, mode, test_number, gc, array_type, array_size, percent_unique, selected_algs, graph, mode_button, run_button, get_info_button, progress_bar):
        global unique_items_num
        self.master.focus()
        
        gn.sessions[-1].interrupted = True
        time.sleep(0.05)
        gn.sessions[-1].reset_time = time.monotonic_ns()
        perform.stopped = False
        mode_button.change_mode()
        mode_button.configure(state='disabled')
        progress_bar.set_value(0)
        perform.waiting = 0
        perform.finished = 0
        measure.waiting = 0
        measure.finished = 0
        display_frame.data.clear()
        get_info_button.configure(state='disabled')
        display_frame.destroy_widgets()
        selected_algs.sort(key=lambda x: x.idx)
        graph.X = []
        graph.items = []
        graph.mn = 1e9
        graph.array_type = array_type
        graph.percent_unique = percent_unique
        gn.mode = mode
        time_algs.tests_number = test_number
        time_algs.gc = gc

        
        if (mode == 'Graph'):
            for i in range(max(1, array_size//100), array_size*2+1, max(1, array_size//100)):
                graph.X.append(i)
            graph.X.append(array_size)
            graph.X = sorted(list(set(graph.X)))
            for i in range(len(selected_algs)):
                graph.items.append(GraphItem(allocator(selected_algs[i]['text'])[2], selected_algs[i]['text']))
            display_frame.create_coordinate_plane()
        else:
            size = 0
            while (size*size < len(selected_algs)):
                size += 1
            display_frame.size = size
            display_frame.arr_type = array_type
            display_frame.arr_size = array_size
            
            array = list(range(5, 5*array_size+1, 5))
            m = max(1, round(percent_unique*array_size))
            if (percent_unique > 0.5):
                shuffle(array)
            for i in range(array_size):
                array[i] = array[i%m]
            unique_items_num = len(set(array))
            
            match array_type:
                case 'Ascending':
                    array.sort()
                case 'Descending':
                    array.sort(reverse=True)
                case 'Random shuffle':
                    shuffle(array)
                case 'Partially ordered':
                    if (randint(0, 1)):
                        array[array_size//3: -array_size//3] = sorted(array[array_size//3: -array_size//3])
                    else:
                        array[:array_size//3] = sorted(array[:array_size//3])
                        array[-array_size//3:] = sorted(array[-array_size//3:])
            
            perform.mx = max(array)
            display_frame.create_widgets(selected_algs=selected_algs.copy(), array=array.copy())
            perform.draw_multiple_arrays(display_frame.size, display_frame.markup)
        
        if (len(selected_algs) > 0):
            run_button.configure(state='normal')
        else:
            run_button.configure(state='disabled')


class RunButton(MyButton):
    
    def __init__(self, master, *args, **kwargs):
        super(RunButton, self).__init__(master, *args, **kwargs)
    
    def on_click(self, graph, size, markup, mode_button, get_info_button, display_frame, progress_bar):
        global session_number
        self.master.focus()
        self.configure(state='disabled')
        if (gn.sessions[-1].reset_time <= gn.sessions[-1].interrupt_time or not(gn.sessions[-1].completed)):
            messagebox.showerror('Sort Visualizer', 'Previous process was interrupted incorrectly. Press "Reset" to restart.')
            gn.sessions[-1].interrupt_time = -1
            gn.sessions[-1].completed = True
            return
        gn.sessions.append(gn.Status())
        session_number = len(gn.sessions)-1
        if (gn.mode != 'Graph' and gn.mode != 'No Visualization'):
            mode_button.configure(state='normal')
        progress_bar.set_value(0)
        perform.finished = 0
        measure.finished = 0
        if (gn.mode == 'Graph'):
            graph_builder.barrier = threading.Barrier(parties=1, action=lambda obj=self: obj.show_graph(graph, display_frame))
            graph_thread = threading.Thread(target=graph_builder.build_graph, args=(graph, progress_bar, session_number, ), daemon=True)
            graph_thread.start()
            
        if (gn.mode == 'No Visualization'):
            self.show_data(markup, display_frame, progress_bar, mode_button, get_info_button)
        else:
            perform.barrier = threading.Barrier(parties=size**2, action=lambda obj=self: obj.show_data(markup, display_frame, progress_bar, mode_button, get_info_button))
            for i in range(size):
                for j in range(size):
                    markup[i][j].perform_thread.start()

    def show_data(self, markup, display_frame, progress_bar, mode_button, get_info_button):
        mode_button.configure(state='disabled')
        progress_bar.set_value(0)
        measure.barrier = threading.Barrier(parties=1, action=lambda obj=self: obj.configure_connected_buttons(get_info_button))
        measure_thread = threading.Thread(target=measure.collect_data, args=(markup, display_frame, progress_bar, session_number, ), daemon=True)
        measure_thread.start()
    
    @staticmethod
    def show_graph(graph, display_frame):
        gn.sessions[-1].completed = True
        if (gn.sessions[-1].interrupted):
            return
        plt.title('With Fluctuation')
        for i in range(len(graph.items)):
            plt.plot(graph.X[:graph.mn], graph.items[i].Y1[:graph.mn], label=graph.items[i].name)
        plt.legend()
        display_frame.canvas.draw()
        display_frame.graph_mode_button.mode = 0 # with fluctuation
        display_frame.graph_mode_button.configure(command=lambda obj=display_frame.graph_mode_button: obj.on_click(display_frame.canvas, graph), state='normal')
    
    @staticmethod
    def configure_connected_buttons(get_info_button):
        gn.sessions[-1].completed = True
        if (gn.sessions[-1].interrupted):
            return
        get_info_button.configure(state='normal')


class ModeButton(MyButton):
    
    def __init__(self, master, *args, **kwargs):
        super(ModeButton, self).__init__(master, *args, **kwargs)
    
    def on_click(self):
        self.master.focus()
        perform.stopped ^= True
        
        self.change_mode()
    
    def change_mode(self):
        if (perform.stopped):
            self.configure(text='Continue')
        else:
            self.configure(text='Stop')


class GetInfoButton(MyButton):
    
    def __init__(self, master, *args, **kwargs):
        super(GetInfoButton, self).__init__(master, *args, **kwargs)

    def on_click(self, arr_type, arr_size, percent_unique, data, progress_bar):
        global last_num
        last_num += 1
        self.master.focus()
        self.configure(state='disabled')
        info_win = InfoWin(last_num, self)
        info_win.create_widgets(arr_type, arr_size, percent_unique, data)


class GCModeButton(MyButton):
    
    def __init__(self, master, *args, **kwargs):
        super(GCModeButton, self).__init__(master, *args, **kwargs)
        self.configure(style='default.TButton')
        self.selected = False
        
    def on_click(self):
        self.master.focus()
        if (not(self.selected)):
            self.configure(style='selectedR.TButton')
            self.selected = True
        else:
            self.configure(style='default.TButton')
            self.selected = False
    
    
class MyCombobox(ttk.Combobox):
    
    def __init__(self, master, cur, *args, **kwargs):
        super(MyCombobox, self).__init__(master, state='readonly', *args, **kwargs)
        if (len(self['values']) >= cur):
            self.current(cur)
        self.bind('<<ComboboxSelected>>', lambda e, obj=self: obj.on_change()) 
    
    def on_change(self):
        self.master.focus()


class VisualizerTypeCombobox(MyCombobox):
    
    def __init__(self, master, *args, **kwargs):
        super(VisualizerTypeCombobox, self).__init__(master, *args, **kwargs)
    
    def on_change(self, arr_size_scale):
        self.master.focus()
        value = self.get()
        match value:
            case 'Classic':
                arr_size_scale.configure(to=100)
            case 'Graph':
                arr_size_scale.configure(to=10000)
            case 'No Visualization':
                arr_size_scale.configure(to=10000)

class MyProgressbar(ttk.Progressbar):
    
    def __init__(self, master, progress_value_entry, *args, **kwargs):
        super(MyProgressbar, self).__init__(master, *args, **kwargs)
        self.progress_value_entry = progress_value_entry
    
    def set_value(self, value):
        self.configure(value=min(max(0.0, round(value, 1)), 100.0))
        self.update()
        self.progress_value_entry.change_text(str(self['value'])+'%')


# mb width for columns?
class MyTreeview(ttk.Treeview):
    
    def __init__(self, master, headers, col_types, *args, **kwargs):
        super(MyTreeview, self).__init__(master, show='headings', *args, **kwargs)
        self.headers = headers.copy()
        self.col_types = col_types.copy()
        self.last_sorted = -1
        self.configure_columns()
    
    def configure_columns(self):
        scrollbar = ttk.Scrollbar(self.master)
        scrollbar.pack(side='right', fill='y')
        scrollbar.configure(command=self.yview)
        self.configure(yscrollcommand=scrollbar.set, selectmode='extended', columns=list(range(len(self.headers))))
        self.tag_configure('oddrow', background='white')
        self.tag_configure('evenrow', background='lightblue')
        for j in range(len(self.headers)):
            self.heading(j, text=self.headers[j], command=lambda obj=self, column=j, column_type=self.col_types[j]: obj.column_sort(column, False, column_type))
            self.column(j, width=0, anchor='center')
        
    def column_sort(self, col, reverse, key):
        
        l = [(self.set(k, col), k) for k in self.get_children('')]
        l.sort(reverse=reverse, key=lambda x: key(x[0]) if x[0] != '' else str(x[0]))
        for idx, (_, k) in enumerate(l):
            self.move(k, '', idx)
            if (idx % 2 == 0):
                self.item(k, tags=('evenrow',))
            else:
                self.item(k, tags=('oddrow',))
        
        if (self.last_sorted != -1):
            self.heading(self.last_sorted, text=self.headers[self.last_sorted], 
                        command=lambda obj=self, column=self.last_sorted, column_type=self.col_types[self.last_sorted]: obj.column_sort(column, False, column_type))
        
        self.heading(col, text=self.headers[col]+' '+chr(8593) if not(reverse) else self.headers[col]+' '+chr(8595),
                     command=lambda obj=self, column=col, column_type=key: obj.column_sort(column, not(reverse), column_type))
        
        self.last_sorted = col
    
    def enter_data(self, data):
        self.remove_all()
        for i in range(len(data)):
            if (i % 2 == 0):
                self.insert('', 'end', values=list(data[i].__dict__.values()).copy(), tags=('evenrow',))
            else:
                self.insert('', 'end', values=list(data[i].__dict__.values()).copy(), tags=('oddrow',))
        self.column_sort(0, False, self.col_types[0])
        
    def remove_all(self):
        children = self.get_children()
        for child in children:
            self.delete(child)


class InfoWin(tk.Toplevel):
    
    def __init__(self, last_num, get_info_button):
        super(InfoWin, self).__init__()
        self.num = last_num
        self.geometry('1050x300')
        self.title('Information')
        self.iconbitmap('images/chart-3331238.ico')
        self.protocol('WM_DELETE_WINDOW', lambda obj=self: obj.on_closing(get_info_button))
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
    
    def on_closing(self, get_info_button):
        self.destroy()
        if (self.num == last_num):
            get_info_button.configure(state='normal')
    
    def create_widgets(self, arr_type, arr_size, percent_unique, data):
        # GENERAL INFO FRAME----------------------------------------------------
        general_info_frame = MyLabelFrame(self, bd=0)
        general_info_frame.grid(row=0, column=0, sticky='nswe')
        
        type_labelentry = LabelEntry(general_info_frame, label_text='Input Type:', entry_text=arr_type)
        type_labelentry.entry.configure(bg='SystemButtonFace', fg='#000000', disabledbackground='SystemButtonFace', disabledforeground='#000000')
        type_labelentry.create_widgets()
        type_labelentry.grid(row=1, column=0, sticky='w')
        arr_size_labelentry = LabelEntry(general_info_frame, label_text='Array Size:', entry_text=arr_size)
        arr_size_labelentry.entry.configure(bg='SystemButtonFace', fg='#000000', disabledbackground='SystemButtonFace', disabledforeground='#000000')
        arr_size_labelentry.create_widgets()
        arr_size_labelentry.grid(row=2, column=0, sticky='w')
        percentage_labelentry = LabelEntry(general_info_frame, label_text='Unique Items:', entry_text=str(unique_items_num)+' ('+chr(8776)+str(percent_unique)+'%)')
        percentage_labelentry.entry.configure(bg='SystemButtonFace', fg='#000000', disabledbackground='SystemButtonFace', disabledforeground='#000000')
        percentage_labelentry.create_widgets()
        percentage_labelentry.grid(row=3, column=0, sticky='w')
        
        # TREE FRAME------------------------------------------------------------
        tree_frame = MyLabelFrame(self, bd=0)
        tree_frame.grid(row=1, column=0, sticky='nswe')
        tree = MyTreeview(tree_frame, 
                          headers=['Name', 
                                   'Vizual Time (sec)', 
                                   'Sort Time (ms)', 
                                   'Comparisons', 
                                   'Swaps', 
                                   'Writes to Main Array', 
                                   'Writes to Auxiliary Array'], 
                          col_types={0: str, 
                                     1: float, 
                                     2: float, 
                                     3: int, 
                                     4: int, 
                                     5: int, 
                                     6: int})
        
        tree.enter_data(data)
        tree.pack(expand=True, fill='both')


class TextBox(tk.Text):
    
    def __init__(self, master, *args, **kwargs):
        super(TextBox, self).__init__(master, *args, **kwargs)


class App(tk.Tk):
    
    def __init__(self):
        super(App, self).__init__()
        ttk.Style().configure('default.TButton')
        ttk.Style().configure('selectedB.TButton', background='#0000FF', foreground='#0000FF')
        ttk.Style().configure('selectedR.TButton', background='#FF0000', foreground='#FF0000')
        self.selected_algs = []
        self.graph = Graph(None, None)
        self.geometry('1280x720')
        self.title('Sorting Visualizer')
        self.iconbitmap('images/chart-3331238.ico')
        self.protocol('WM_DELETE_WINDOW', lambda obj=self: obj.on_closing())
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=6)
    
    def on_closing(self):
        if (messagebox.askokcancel('Sort Visualizer', 'Close program?')):
            plt.close('all')
            self.destroy()
    
    def create_widgets(self):
        
        # VIZUALIZER FRAME------------------------------------------------------
        visualizer_frame = DisplayFrame(self, bg='#000000', bd=3)
        visualizer_frame.grid(row=0, column=0, rowspan=3, sticky='nswe', padx=[2, 2], pady=[2, 2])
        
        
        # CONTROLS FRAME--------------------------------------------------------
        controls_frame = MyLabelFrame(self, text='Animation Controls', bd=3)
        controls_frame.grid(row=0, column=1, sticky='nswe', padx=[2, 2], pady=[2, 2])
        
        
        visualizer_type_label = MyLabel(controls_frame, anchor='w', text='Visualizer Type:')
        visualizer_type_label.grid(row=0, column=0, sticky='w', padx=[4, 0], pady=[4, 0])
        
        
        visualizer_type_combobox = VisualizerTypeCombobox(controls_frame, cur=0, width=17, values=['Classic', 'Graph', 'No Visualization'])
        visualizer_type_combobox.bind('<<ComboboxSelected>>', lambda e, obj=visualizer_type_combobox: obj.on_change(arr_size_scale))
        visualizer_type_combobox.grid(row=0, column=1, sticky='we', padx=[4, 4], pady=[4, 4])
        
        
        button_warp_frame = MyLabelFrame(controls_frame, bd=0)
        button_warp_frame.grid(row=1, column=0, columnspan=2, sticky='nswe')
        
        
        run_button = RunButton(button_warp_frame, state='disabled', width=10, text='Run')
        run_button.configure(command=lambda obj=run_button: obj.on_click(graph=self.graph,
                                                                         size=visualizer_frame.size, 
                                                                         markup=visualizer_frame.markup, 
                                                                         mode_button=mode_button, 
                                                                         get_info_button=get_info_button,
                                                                         display_frame=visualizer_frame,
                                                                         progress_bar=self.progress_bar))
        run_button.grid(row=0, column=0, sticky='we', padx=[34, 6], pady=[4, 4])
        
        
        mode_button = ModeButton(button_warp_frame, state='disabled', width=10, text='Stop')
        mode_button.configure(command=lambda obj=mode_button: obj.on_click())
        mode_button.grid(row=0, column=1, sticky='we', padx=[6, 20], pady=[4, 4])
        
        
        reset_button = ResetButton(button_warp_frame, width=10, text='Reset')
        reset_button.configure(command=lambda obj=reset_button: obj.on_click(display_frame=visualizer_frame, 
                                                                             mode=visualizer_type_combobox.get(), 
                                                                             test_number = int(test_number_combobox.get()), 
                                                                             gc = GC_mode_btn.selected, 
                                                                             array_type=type_combobox.get(), 
                                                                             percent_unique=percentage_entry.current_value/100,
                                                                             array_size=arr_size_entry.current_value, 
                                                                             selected_algs=self.selected_algs.copy(),
                                                                             graph=self.graph, 
                                                                             mode_button=mode_button, 
                                                                             run_button=run_button, 
                                                                             get_info_button=get_info_button,
                                                                             progress_bar=self.progress_bar))
        reset_button.grid(row=1, column=0, sticky='we', padx=[34, 6], pady=[4, 4])
        
        
        get_info_button = GetInfoButton(button_warp_frame, state='disabled', width=10, text='Get Info')
        get_info_button.configure(command=lambda obj=get_info_button: obj.on_click(arr_type=visualizer_frame.arr_type, 
                                                                                   arr_size=visualizer_frame.arr_size, 
                                                                                   percent_unique=percentage_entry.current_value, 
                                                                                   data=visualizer_frame.data,
                                                                                   progress_bar=self.progress_bar))
        get_info_button.grid(row=1, column=1, sticky='we', padx=[6, 20], pady=[4, 4])
        
        
        speed_label = MyLabel(controls_frame, anchor='w', text='Speed:')
        speed_label.grid(row=2, column=0, sticky='w', padx=[4, 4], pady=[4, 4])
        
        
        speed_scale = SpeedScale(controls_frame, from_=0, to=1000, width=8, sliderlength=8)
        speed_scale.configure(command=lambda e, obj=speed_scale: obj.set_delay(entry=delay_entry, reverse=True))
        speed_scale.grid(row=2, column=1, sticky='we', padx=[4, 4], pady=[4, 4])
        
        
        delay_label = MyLabel(controls_frame, anchor='w', text='Delay (ms):')
        delay_label.grid(row=3, column=0, sticky='w', padx=[4, 4], pady=[4, 4])
        
        
        delay_entry = DelayEntry(controls_frame, width=5, justify='right')
        delay_entry.bind('<Return>', lambda e, obj=delay_entry: obj.set_delay(scale=speed_scale, reverse=True))
        delay_entry.insert(0, int(speed_scale['from']))
        delay_entry.display_on_scale(scale=speed_scale, reverse=True)
        delay_entry.grid(row=3, column=1, sticky='w', padx=[4, 4], pady=[4, 4])
        
        
        # ALG FRAME-------------------------------------------------------------
        alg_frame = MyLabelFrame(self, text='Input and perform', bd=3)
        alg_frame.grid(row=1, column=1, sticky='nswe', padx=[2, 2], pady=[2, 2])
        alg_frame.rowconfigure(4, weight=1) # for alg_button_frame
        
        
        type_label = MyLabel(alg_frame, anchor='w', text='Input Type:')
        type_label.grid(row=0, column=0, sticky='w', padx=[4, 0], pady=[4, 0])
        
        
        type_combobox = MyCombobox(alg_frame, cur=0, values=['Ascending', 'Descending', 'Random shuffle', 'Partially ordered'])
        type_combobox.grid(row=0, column=1, columnspan=2, sticky='we', padx=[4, 4], pady=[4, 4])
        
        
        arr_size_label = MyLabel(alg_frame, anchor='w', text='Array Size:')
        arr_size_label.grid(row=1, column=0, sticky='w', padx=[4, 0], pady=[4, 0])
        
        
        arr_size_scale = MyScale(alg_frame, from_=10, to=100, width=8, sliderlength=8)
        arr_size_scale.configure(command=lambda e, obj=arr_size_scale: obj.display_in_entry(entry=arr_size_entry, reverse=False))
        arr_size_scale.grid(row=1, column=1, sticky='we', padx=[4, 0], pady=[4, 0])
        
        
        arr_size_entry = MyEntry(alg_frame, width=5, justify='right')
        arr_size_entry.bind('<Return>', lambda e, obj=arr_size_entry: obj.display_on_scale(scale=arr_size_scale, reverse=False))
        arr_size_entry.insert(0, int(arr_size_scale['from']))
        arr_size_entry.display_on_scale(scale=arr_size_scale, reverse=False)
        arr_size_entry.grid(row=1, column=2, sticky='e', padx=[4, 4], pady=[4, 4])
        
        
        percentage_label = MyLabel(alg_frame, anchor='w', text='% Unique:')
        percentage_label.grid(row=2, column=0, sticky='w', padx=[4, 0], pady=[4, 0])
        
        
        percentage_scale = MyScale(alg_frame, from_=0, to=100, width=8, sliderlength=8)
        percentage_scale.configure(command=lambda e, obj=percentage_scale: obj.display_in_entry(entry=percentage_entry, reverse=False))
        percentage_scale.grid(row=2, column=1, sticky='we', padx=[4, 0], pady=[4, 0])
        
        
        percentage_entry = MyEntry(alg_frame, width=5, justify='right')
        percentage_entry.bind('<Return>', lambda e, obj=percentage_entry: obj.display_on_scale(scale=percentage_scale, reverse=False))
        percentage_entry.insert(0, int(arr_size_scale['to']))
        percentage_entry.display_on_scale(scale=percentage_scale, reverse=False)
        percentage_entry.grid(row=2, column=2, sticky='e', padx=[4, 4], pady=[4, 4])
        
        
        benchmark_frame = MyLabelFrame(alg_frame, bd=0)
        benchmark_frame.grid(row=3, column=0, columnspan=3, sticky='nswe', padx=[4, 4], pady=[4, 4])
        
        
        test_number_label = MyLabel(benchmark_frame, anchor='w', text='Test Number:')
        test_number_label.pack(side='left')
        
        
        test_number_combobox = MyCombobox(benchmark_frame, cur=2, width=2, values=['1', '5', '10', '15', '20'])
        test_number_combobox.pack(side='left', padx=[1, 0])
        
        
        GC_mode_btn = GCModeButton(benchmark_frame, text='Enable GC')
        GC_mode_btn.configure(command=lambda obj=GC_mode_btn: obj.on_click())
        GC_mode_btn.pack(side='right')
        
        
        alg_button_frame = ScrollFrame(alg_frame)
        alg_button_frame.grid(row=4, column=0, columnspan=3, sticky='nswe', padx=[4, 4], pady=[4, 4])
        
        
        buttons_name = ['Bubble Sort', 
                        'Comb Sort', 
                        'Count Sort', 
                        'Gnome Sort', 
                        'Heap Sort', 
                        'Insertion Sort', 
                        'IntroSort', 
                        'Merge Sort', 
                        'Odd-Even Sort', 
                        'Quick Sort', 
                        'Radix Sort', 
                        'Selection Sort', 
                        'Shaker Sort',
                        'Shell Sort', 
                        'Tim Sort', 
                        ]
        for i in range(len(buttons_name)):
            alg_btn = AlgButton(alg_button_frame.field, idx=i, width=30, text=buttons_name[i])
            alg_btn.configure(command=lambda obj=alg_btn: obj.on_click(self.selected_algs))
            alg_btn.grid(row=i, column=0)

        
        # PROGRESS FRAME--------------------------------------------------------
        progress_frame = MyLabelFrame(self, text='Progress', bd=3)
        progress_frame.grid(row=2, column=1, sticky='nswe', padx=[2, 2], pady=[2, 2])
        
        self.progress_bar = MyProgressbar(progress_frame, progress_value_entry=None, orient='horizontal', length=170)
        self.progress_bar.grid(row=0, column=0, padx=[4, 2], pady=[2, 6])
        
        progress_value_entry = StaticEntry(progress_frame, text=str(self.progress_bar['value'])+'%', justify='right', width=6, 
                                           bg='SystemButtonFace', fg='#000000', 
                                           disabledbackground='SystemButtonFace', disabledforeground='#000000')
        self.progress_bar.progress_value_entry = progress_value_entry
        progress_value_entry.grid(row=0, column=1, padx=[0, 0], pady=[2, 6])
    
        
    def start(self):
        gn.sessions[0].completed = True
        self.create_widgets()
        self.mainloop()


def main():
    app = App()
    app.start()


if (__name__ == '__main__'):
    main()