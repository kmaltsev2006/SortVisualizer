import threading
import time
import time_algs
import data_algs
import global_namespace as gn

barrier = threading.Barrier(parties=1)
waiting = 0
finished = 0


def collect_data(markup, display_frame, progress_bar, session_number):
    global finished
    for i in range(len(markup)):
        for j in range(len(markup)):
            if (gn.sessions[session_number].interrupted):
                gn.sessions[session_number].interrupt_time = time.monotonic_ns()
                progress_bar.set_value(0)
                barrier.wait()
                return
            if (markup[i][j].name != 'None'):
                markup[i][j].name_entry.change_text(markup[i][j].name + ' (In Progress)')
                markup[i][j].data_item.Stime = markup[i][j].measure_function(markup[i][j])
                display_frame.data.append(markup[i][j].data_item)
                markup[i][j].name_entry.change_text(markup[i][j].name + ' (Finished)')
                finished += 1
                markup[i][j].data_frame.Stime.entry.change_text(markup[i][j].data_item.Stime)
                markup[i][j].data_frame.cmp.entry.change_text(markup[i][j].data_item.cmp)
                markup[i][j].data_frame.swaps.entry.change_text(markup[i][j].data_item.swaps)
                markup[i][j].data_frame.Mwrites.entry.change_text(markup[i][j].data_item.Mwrites)
                markup[i][j].data_frame.Awrites.entry.change_text(markup[i][j].data_item.Awrites)
                if (waiting != 0):
                    progress_bar.set_value(finished/waiting*100)
                else:
                    progress_bar.set_value(0)
                time.sleep(0.05)
    barrier.wait()
    return


def none_function(*args, **kwargs):
    return None


def measure_bubble_sort(cell):
    data_algs.get_data_bubble_sort(cell)
    return time_algs.time_bubble_sort(cell.array2)


def measure_insertion_sort(cell):
    data_algs.get_data_insertion_sort(cell)
    return time_algs.time_insertion_sort(cell.array2)


def measure_selection_sort(cell):
    data_algs.get_data_selection_sort(cell)
    return time_algs.time_selection_sort(cell.array2)


def measure_quick_sort(cell):
    data_algs.get_data_quick_sort(cell)
    return time_algs.time_quick_sort(cell.array2)


def measure_merge_sort(cell):
    data_algs.get_data_merge_sort(cell)
    return time_algs.time_merge_sort(cell.array2)


def measure_shaker_sort(cell):
    data_algs.get_data_shaker_sort(cell)
    return time_algs.time_shaker_sort(cell.array2)


def measure_gnome_sort(cell):
    data_algs.get_data_gnome_sort(cell)
    return time_algs.time_gnome_sort(cell.array2)


def measure_odd_even_sort(cell):
    data_algs.get_data_odd_even_sort(cell)
    return time_algs.time_odd_even_sort(cell.array2)


def measure_comb_sort(cell):
    data_algs.get_data_comb_sort(cell)
    return time_algs.time_comb_sort(cell.array2)


def measure_heap_sort(cell):
    data_algs.get_data_heap_sort(cell)
    return time_algs.time_heap_sort(cell.array2)


def measure_tim_sort(cell):
    data_algs.get_data_tim_sort(cell)
    return time_algs.time_tim_sort(cell.array2)


def measure_introsort(cell):
    data_algs.get_data_introsort(cell)
    return time_algs.time_introsort(cell.array2)


def measure_shell_sort(cell):
    data_algs.get_data_shell_sort(cell)
    return time_algs.time_shell_sort(cell.array2)


def measure_count_sort(cell):
    data_algs.get_data_count_sort(cell)
    return time_algs.time_count_sort(cell.array2)


def measure_radix_sort(cell):
    data_algs.get_data_radix_sort(cell)
    return time_algs.time_radix_sort(cell.array2)