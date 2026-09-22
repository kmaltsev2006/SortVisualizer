import threading
import time
import global_namespace as gn

delay = 0
stopped = False
barrier = threading.Barrier(parties=1)
mx = 0
waiting = 0
finished = 0

def draw_array(cell, set_delay = True, redraw = False):
    while (stopped and not(redraw)):
        time.sleep(0.1)
    if (set_delay):
        time.sleep(delay / 1000)
    
    # copying frame
    cell.bottom_canvas.update()
    bottom_canvas_width = cell.bottom_canvas.winfo_width()
    bottom_canvas_height = cell.bottom_canvas.winfo_height()
    cell.bottom_canvas.grid_remove()
    cell.bottom_canvas.delete('all')
    for i in range(len(cell.array1)):
        cell.bottom_canvas.create_rectangle(i*bottom_canvas_width/len(cell.array1), bottom_canvas_height-cell.array1[i]*bottom_canvas_height/mx, 
                                       (i+1)*bottom_canvas_width/len(cell.array1), bottom_canvas_height, 
                                       fill='#FFFFFF' if i not in cell.specials else cell.specials[i])
    cell.bottom_canvas.update()
    cell.bottom_canvas.grid()
    
    # redrawing frame
    cell.top_canvas.update()
    top_canvas_width = cell.top_canvas.winfo_width()
    top_canvas_height = cell.top_canvas.winfo_height()
    cell.top_canvas.grid_remove()
    cell.top_canvas.delete('all')
    for i in range(len(cell.array1)):
        cell.top_canvas.create_rectangle(i*top_canvas_width/len(cell.array1), top_canvas_height-cell.array1[i]*top_canvas_height/mx, 
                                    (i+1)*top_canvas_width/len(cell.array1), top_canvas_height, 
                                    fill='#FFFFFF' if i not in cell.specials else cell.specials[i])
    cell.top_canvas.update()
    cell.top_canvas.grid()
    cell.last_rendered += len(cell.array1)


def draw_sorted_array(cell):
    cell.specials.clear()
    draw_array(cell)
    for i in range(len(cell.array1)):
        while (stopped):
            time.sleep(0.1)
        cell.top_canvas.itemconfigure(cell.last_rendered-len(cell.array1)+i+1, fill='#00FF00')
        cell.specials[i] = '#00FF00'
        time.sleep(0.01)


def draw_multiple_arrays(size, markup):
    for i in range(size):
        for j in range(size):
            if (markup[i][j].name != 'None'):
                if (gn.mode == 'No Visualization'):
                    markup[i][j].data_frame.grid()
                    markup[i][j].top_canvas.grid_remove()
                    markup[i][j].bottom_canvas.grid_remove()
                else:
                    draw_array(markup[i][j], set_delay=False, redraw=True)


def execute(cell, function):
    global finished
    start = time.monotonic()
    cell.name_entry.change_text(cell.name + ' (In Progress)')
    function()
    draw_sorted_array(cell)
    cell.name_entry.change_text(cell.name + ' (Finished)')
    end = time.monotonic()
    cell.data_item.Vtime = round(end - start, 2)
    finished += 1
    if (waiting != 0):
        cell.master.master.progress_bar.set_value(finished/waiting*100)
    else:
        cell.master.master.progress_bar.set_value(0)
    barrier.wait()


def none_function(*args, **kwargs):
    barrier.wait()


def perform_bubble_sort(cell):
    
    def bubble_sort(array):
        for i in range(len(array)-1):
            for j in range(len(array)-i-1):
                if (array[j] > array[j+1]):
                    array[j], array[j+1] = array[j+1], array[j]
                cell.specials = {j: '#FF0000', j+1: '#FF0000'}
                draw_array(cell)
    
    execute(cell, lambda array=cell.array1: bubble_sort(array))


def perform_insertion_sort(cell):
    
    def insertion_sort(array):
        for i in range(1, len(array)):
            el = array[i]
            j = i-1
            while (j >= 0 and el < array[j]):
                    array[j + 1] = array[j]
                    cell.specials = {i: '#0000FF', j: '#FF0000', j+1: '#FF0000'}
                    draw_array(cell)
                    j -= 1
            array[j + 1] = el
            cell.specials = {i: '#0000FF', j+1: '#FF0000'}
            draw_array(cell)
            
    execute(cell, lambda array=cell.array1: insertion_sort(array))


def perform_selection_sort(cell):
    
    def selection_sort(array):
        for i in range(len(array) - 1):
            imin = i
            for j in range(i + 1, len(array)):
                if (array[j] < array[imin]):
                    imin = j
                cell.specials = {i: '#0000FF', imin: '#FF0000', j: '#FF0000'}
                draw_array(cell)
            array[i], array[imin] = array[imin], array[i]
            cell.specials = {i: '#0000FF', imin: '#FF0000'}
            draw_array(cell)
    
    execute(cell, lambda array=cell.array1: selection_sort(array))


def perform_quick_sort(cell):
    
    def quick_sort(array, front, back):
        if (front >= back):
            return None
        l = front
        r = back
        x = array[(l+r)//2]
        while (l <= r):
            while (array[l] < x):
                l += 1
                cell.specials = {(l+r)//2: '#0000FF', l: '#FF0000', r: '#FF0000'}
                draw_array(cell)
            while (array[r] > x):
                r -= 1
                cell.specials = {(l+r)//2: '#0000FF', l: '#FF0000', r: '#FF0000'}
            if (l <= r):
                array[l], array[r] = array[r], array[l]
                l += 1
                r -= 1
                cell.specials = {(l+r)//2: '#0000FF', l: '#FF0000', r: '#FF0000'}
                draw_array(cell)
        quick_sort(array, front, r)
        quick_sort(array, l, back)
    
    execute(cell, lambda array=cell.array1, front=0, back=len(cell.array1)-1: quick_sort(array, front, back))


def perform_merge_sort(cell):
    
    def merge(array, l, m, r):
        tmp1 = array[l : m + 1]
        tmp2 = array[m + 1 : r + 1]
        i = 0
        j = 0
        q = l
        while (i < len(tmp1) and j < len(tmp2)):
            if (tmp1[i] <= tmp2[j]):
                array[q] = tmp1[i]
                i += 1
            else:
                array[q] = tmp2[j]
                j += 1
            cell.specials = {l+i: '#FF0000', m+1+j: '#FF0000', q: '#0000FF'}
            draw_array(cell)
            q += 1
        while (i < len(tmp1)):
            array[q] = tmp1[i]
            cell.specials = {q: '#0000FF'}
            draw_array(cell)
            i += 1
            q += 1
        while (j < len(tmp2)):
            array[q] = tmp2[j]
            cell.specials = {q: '#0000FF'}
            draw_array(cell)
            j += 1
            q += 1
    
    def merge_sort(array, l, r):
        if (l < r):
            m = (l + r) // 2
            merge_sort(array, l, m)
            merge_sort(array, m + 1, r)
            merge(array, l, m, r)
    
    execute(cell, lambda array=cell.array1, l=0, r=len(cell.array1)-1: merge_sort(array, l, r))


def perform_shaker_sort(cell):
    
    def shaker_sort(array):
        swapped = True
        start = 0
        end = len(array)-1
        while (swapped):
            swapped = False
            for i in range (start, end):
                if (array[i] > array[i+1]) :
                    array[i], array[i+1] = array[i+1], array[i]
                    swapped = True
                cell.specials = {i: '#FF0000', i+1: '#FF0000'}
                draw_array(cell)
            if (not(swapped)):
                break
            swapped = False
            end -= 1
            for i in range(end - 1, start - 1, -1):
                if (array[i] > array[i+1]):
                    array[i], array[i+1] = array[i+1], array[i]
                    swapped = True
                cell.specials = {i: '#FF0000', i+1: '#FF0000'}
                draw_array(cell)
            start += 1
    
    execute(cell, lambda array=cell.array1: shaker_sort(array))


def perform_gnome_sort(cell):

    def gnome_sort(array):
        if (len(array) == 1):
            return
        i = 0
        while (i < len(array)):
            if i == 0:
                i += 1
            if (array[i] >= array[i - 1]):
                i += 1
                cell.specials = {i: '#FF0000'}
            else:
                array[i], array[i-1] = array[i-1], array[i]
                cell.specials = {i: '#FF0000', i-1: '#FF0000'}
                i -= 1
            draw_array(cell)
    
    execute(cell, lambda array=cell.array1: gnome_sort(array))


def perform_odd_even_sort(cell):
    
    def odd_even_sort(array):
        is_sorted = False
        while (not(is_sorted)):
            is_sorted = True
            for i in range(1, len(array)-1, 2):
                if (array[i] > array[i+1]):
                    array[i], array[i+1] = array[i+1], array[i]
                    is_sorted = False
                cell.specials = {i: '#FF0000', i+1: '#FF0000'}
                draw_array(cell)
            
            for i in range(0, len(array)-1, 2):
                if (array[i] > array[i+1]):
                    array[i], array[i+1] = array[i+1], array[i]
                    is_sorted = False
                cell.specials = {i: '#FF0000', i+1: '#FF0000'}
                draw_array(cell)
    
    execute(cell, lambda array=cell.array1: odd_even_sort(array))


def perform_comb_sort(cell):
        
    def get_next_gap(gap):
        gap = (gap * 10) // 13
        if (gap < 1):
            return 1
        return gap

    def comb_sort(arr):
        n = len(arr)
        gap = n
        swapped = True
        while (gap != 1 or swapped):
            gap = get_next_gap(gap)
            swapped = False
            for i in range(0, n-gap):
                if (arr[i] > arr[i + gap]):
                    arr[i], arr[i + gap] = arr[i + gap], arr[i]
                    swapped = True
                cell.specials = {i: '#FF0000', i+gap: '#FF0000'}
                draw_array(cell)
                
    execute(cell, lambda array=cell.array1: comb_sort(array))


def perform_heap_sort(cell):
    
    def heapify(array, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n and array[largest] < array[l]:
            largest = l
        if r < n and array[largest] < array[r]:
            largest = r
        if largest != i:
            array[i], array[largest] = array[largest], array[i]
            cell.specials = {i: '#FF0000', largest: '#FF0000'}
            draw_array(cell)
            heapify(array, n, largest)

    def heap_sort(array):
        n = len(array)
        for i in range(n//2-1, -1, -1):
            heapify(array, n, i)
        for i in range(n-1, 0, -1):
            array[0], array[i] = array[i], array[0]
            cell.specials = {0: '#FF0000', i: '#FF0000'}
            draw_array(cell)
            heapify(array, i, 0)
    
    execute(cell, lambda array=cell.array1: heap_sort(array))


def perform_tim_sort(cell):
    
    MINIMUM= 32
  
    def find_minrun(n):
        r = 0
        while n >= MINIMUM: 
            r |= n & 1
            n >>= 1
        return n + r 
    
    def insertion_sort(array, left, right): 
        for i in range(left+1,right+1):
            element = array[i]
            j = i-1
            while element<array[j] and j>=left :
                array[j+1] = array[j]
                cell.specials = {j+1: '#FF0000', j: '#FF0000'}
                draw_array(cell)
                j -= 1
            array[j+1] = element
            cell.specials = {j+1: '#FF0000'}
            draw_array(cell)
        return array
                
    def merge(array, l, m, r): 
        array_length1 = m - l + 1
        array_length2 = r - m 
        left = []
        right = []
        for i in range(0, array_length1): 
            left.append(array[l + i]) 
        for i in range(0, array_length2): 
            right.append(array[m + 1 + i]) 
        i=0
        j=0
        k=l
        
        while j < array_length2 and  i < array_length1: 
            if left[i] <= right[j]:
                array[k] = left[i]
                cell.specials = {k: '#FF0000'}
                draw_array(cell)
                i += 1
            else: 
                array[k] = right[j]
                cell.specials = {k: '#FF0000'}
                draw_array(cell)
                j += 1
            k += 1
        
        while i < array_length1: 
            array[k] = left[i]
            cell.specials = {k: '#FF0000'}
            draw_array(cell)
            k += 1
            i += 1
        
        while j < array_length2:
            array[k] = right[j]
            cell.specials = {k: '#FF0000'}
            draw_array(cell)
            k += 1
            j += 1

    def tim_sort(array): 
        n = len(array) 
        minrun = find_minrun(n) 
        
        for start in range(0, n, minrun): 
            end = min(start + minrun - 1, n - 1) 
            insertion_sort(array, start, end) 
        
        size = minrun 
        while size < n:         
            for left in range(0, n, 2 * size): 
                mid = min(n - 1, left + size - 1) 
                right = min((left + 2 * size - 1), (n - 1)) 
                merge(array, left, mid, right) 
            size = 2 * size
    
    execute(cell, lambda array=cell.array1: tim_sort(array))


def perform_introsort(cell):
    
    def introsort(array):
        maxdepth = (len(array).bit_length() - 1)*2
        introsort_helper(array, 0, len(array), maxdepth)
    
    def introsort_helper(array, start, end, maxdepth):
        if end - start <= 1:
            return
        elif maxdepth == 0:
            heapsort(array, start, end)
        else:
            p = partition(array, start, end)
            introsort_helper(array, start, p + 1, maxdepth - 1)
            introsort_helper(array, p + 1, end, maxdepth - 1)
    
    def partition(array, start, end):
        pivot = array[start]
        i = start - 1
        j = end
    
        while True:
            i = i + 1
            while array[i] < pivot:
                cell.specials = {i: '#FF0000', pivot: '#0000FF'}
                draw_array(cell)
                i = i + 1
            j = j - 1
            while array[j] > pivot:
                cell.specials = {j: '#FF0000', pivot: '#0000FF'}
                draw_array(cell)
                j = j - 1
    
            if i >= j:
                return j
    
            swap(array, i, j)
    
    def swap(array, i, j):
        array[i], array[j] = array[j], array[i]
        cell.specials = {i: '#FF0000', j: '#FF0000'}
        draw_array(cell)
    
    def heapsort(array, start, end):
        build_max_heap(array, start, end)
        for i in range(end - 1, start, -1):
            swap(array, start, i)
            max_heapify(array, index=0, start=start, end=i)
    
    def build_max_heap(array, start, end):
        def parent(i):
            return (i - 1)//2
        length = end - start
        index = parent(length - 1)
        while index >= 0:
            max_heapify(array, index, start, end)
            index = index - 1
    
    def max_heapify(array, index, start, end):
        def left(i):
            return 2*i + 1
        def right(i):
            return 2*i + 2
    
        size = end - start
        l = left(index)
        r = right(index)
        if (l < size and array[start + l] > array[start + index]):
            largest = l
        else:
            largest = index
        if (r < size and array[start + r] > array[start + largest]):
            largest = r
        if largest != index:
            swap(array, start + largest, start + index)
            max_heapify(array, largest, start, end)
    
    execute(cell, lambda array=cell.array1: introsort(array))


def perform_shell_sort(cell):
    
    def shell_sort(array):
        interval = len(array) // 2
        while interval > 0:
            for i in range(interval, len(array)):
                temp = array[i]
                cell.specials = {i: '#0000FF'}
                draw_array(cell)
                j = i
                while j >= interval and array[j - interval] > temp:
                    array[j] = array[j - interval]
                    cell.specials = {i: '#0000FF', j: '#FF0000', j - interval: '#FF0000'}
                    draw_array(cell)
                    j -= interval
                array[j] = temp
                cell.specials = {i: '#0000FF', j: '#FF0000'}
                draw_array(cell)
            interval //= 2
    
    execute(cell, lambda array=cell.array1: shell_sort(array))


def perform_count_sort(cell):
    
    def count_sort(array):
        max_element = -1e9
        min_element = 1e9
        for i in range(len(array)):
            max_element = max(max_element, array[i])
            min_element = min(min_element, array[i])
            cell.specials = {i: '#0000FF'}
            draw_array(cell)
        range_of_elements = max_element - min_element + 1
        
        count_array = []
        for _ in range(range_of_elements):
            count_array.append(0)
        
        output_array = []
        for _ in range(len(array)):
            output_array.append(0)
        
        for i in range(0, len(array)):
            count_array[array[i]-min_element] += 1
            cell.specials = {i: '#FF0000'}
            draw_array(cell)
        
        for i in range(1, len(count_array)):
            count_array[i] += count_array[i-1]
        
        for i in range(len(array)-1, -1, -1):
            output_array[count_array[array[i] - min_element] - 1] = array[i]
            cell.specials = {i: '#FF0000'}
            draw_array(cell)
            count_array[array[i] - min_element] -= 1
        
        for i in range(0, len(array)):
            array[i] = output_array[i]
            cell.specials = {i: '#FF0000'}
            draw_array(cell)
    
    execute(cell, lambda array=cell.array1: count_sort(array))


def perform_radix_sort(cell):
    
    def counting_sort(array, place):
        size = len(array)
        output = [0] * size
        count = [0] * 10

        for i in range(0, size):
            index = array[i] // place
            count[index % 10] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        i = size - 1
        while i >= 0:
            index = array[i] // place
            output[count[index % 10] - 1] = array[i]
            cell.specials = {i: '#FF0000'}
            draw_array(cell)
            count[index % 10] -= 1
            i -= 1

        for i in range(0, size):
            array[i] = output[i]
            cell.specials = {i: '#FF0000'}
            draw_array(cell)
    
    def radix_sort(array):
        max_element = max(array)
        for i in range(len(array)):
            cell.specials = {i: '#0000FF'}
            draw_array(cell)
            max_element = max(max_element, array[i])

        place = 1
        while max_element // place > 0:
            counting_sort(array, place)
            place *= 10
    
    execute(cell, lambda array=cell.array1: radix_sort(array))