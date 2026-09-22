

def get_data_bubble_sort(cell):
    
    def bubble_sort(array):
        for i in range(len(array)-1):
            for j in range(len(array)-i-1):
                cell.data_item.cmp += 1
                if (array[j] > array[j+1]):
                    array[j], array[j+1] = array[j+1], array[j]
                    cell.data_item.swaps += 1
                    cell.data_item.Mwrites += 2
    
    bubble_sort(cell.array2.copy())


def get_data_insertion_sort(cell):
    
    def insertion_sort(array):
        for i in range(1, len(array)):
            el = array[i]
            j = i-1
            cell.data_item.cmp += 1
            while (j >= 0 and el < array[j]):
                    cell.data_item.Mwrites += 1
                    array[j + 1] = array[j]
                    j -= 1
            cell.data_item.Mwrites += 1
            array[j + 1] = el
    
    insertion_sort(cell.array2.copy())


def get_data_selection_sort(cell):
    
    def selection_sort(array):
        for i in range(len(array) - 1):
            imin = i
            for j in range(i + 1, len(array)):
                cell.data_item.cmp += 1
                if (array[j] < array[imin]):
                    imin = j
            array[i], array[imin] = array[imin], array[i]
            cell.data_item.swaps += 1
            cell.data_item.Mwrites += 2
    
    selection_sort(cell.array2.copy())


def get_data_quick_sort(cell):
    
    def quick_sort(array, front, back):
        if (front >= back):
            return None
        l = front
        r = back
        x = array[(l+r)//2]
        while (l <= r):
            while (array[l] < x):
                cell.data_item.cmp += 1
                l += 1
            while (array[r] > x):
                cell.data_item.cmp += 1
                r -= 1
            if (l <= r):
                array[l], array[r] = array[r], array[l]
                cell.data_item.swaps += 1
                cell.data_item.Mwrites += 2
                l += 1
                r -= 1
        quick_sort(array, front, r)
        quick_sort(array, l, back)
    
    quick_sort(cell.array2.copy(), 0, len(cell.array2)-1)


def get_data_merge_sort(cell):
    
    def merge(array, l, m, r):
        tmp1 = array[l : m + 1]
        tmp2 = array[m + 1 : r + 1]
        cell.data_item.Awrites += len(tmp1) + len(tmp2)
        i = 0
        j = 0
        q = l
        while (i < len(tmp1) and j < len(tmp2)):
            cell.data_item.cmp += 1
            if (tmp1[i] <= tmp2[j]):
                array[q] = tmp1[i]
                i += 1
            else:
                array[q] = tmp2[j]
                j += 1
            cell.data_item.Mwrites += 1
            q += 1
        while (i < len(tmp1)):
            array[q] = tmp1[i]
            cell.data_item.Mwrites += 1
            i += 1
            q += 1
        while (j < len(tmp2)):
            array[q] = tmp2[j]
            cell.data_item.Mwrites += 1
            j += 1
            q += 1
    
    def merge_sort(array, l, r):
        if (l < r):
            m = (l + r) // 2
            merge_sort(array, l, m)
            merge_sort(array, m + 1, r)
            merge(array, l, m, r)
    
    merge_sort(cell.array2.copy(), 0, len(cell.array2)-1)


def get_data_shaker_sort(cell):
    
    def shaker_sort(array):
        swapped = True
        start = 0
        end = len(array)-1
        while (swapped):
            swapped = False
            for i in range (start, end):
                cell.data_item.cmp += 1
                if (array[i] > array[i+1]) :
                    array[i], array[i+1] = array[i+1], array[i]
                    cell.data_item.swaps += 1
                    cell.data_item.Mwrites += 2
                    swapped = True
            if (not(swapped)):
                break
            swapped = False
            end -= 1
            for i in range(end - 1, start - 1, -1):
                cell.data_item.cmp += 1
                if (array[i] > array[i+1]):
                    array[i], array[i+1] = array[i+1], array[i]
                    cell.data_item.swaps += 1
                    cell.data_item.Mwrites += 2
                    swapped = True
            start += 1
    
    shaker_sort(cell.array2.copy())


def get_data_gnome_sort(cell):

    def gnome_sort(array):
        if (len(array) == 1):
            return
        i = 0
        while (i < len(array)):
            if i == 0:
                i += 1
            cell.data_item.cmp += 1
            if (array[i] >= array[i - 1]):
                i += 1
            else:
                array[i], array[i-1] = array[i-1], array[i]
                cell.data_item.swaps += 1
                cell.data_item.Mwrites += 2
                i -= 1
    
    gnome_sort(cell.array2.copy())


def get_data_odd_even_sort(cell):
    
    def odd_even_sort(array):
        is_sorted = False
        while (not(is_sorted)):
            is_sorted = True
            for i in range(1, len(array)-1, 2):
                cell.data_item.cmp += 1
                if (array[i] > array[i+1]):
                    array[i], array[i+1] = array[i+1], array[i]
                    cell.data_item.swaps += 1
                    cell.data_item.Mwrites += 2
                    is_sorted = False
            
            for i in range(0, len(array)-1, 2):
                cell.data_item.cmp += 1
                if (array[i] > array[i+1]):
                    array[i], array[i+1] = array[i+1], array[i]
                    cell.data_item.swaps += 1
                    cell.data_item.Mwrites += 2
                    is_sorted = False
    
    odd_even_sort(cell.array2.copy())


def get_data_comb_sort(cell):
        
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
                cell.data_item.cmp += 1
                if (arr[i] > arr[i + gap]):
                    arr[i], arr[i + gap] = arr[i + gap], arr[i]
                    cell.data_item.swaps += 1
                    cell.data_item.Mwrites += 2
                    swapped = True
                
    comb_sort(cell.array2.copy())


def get_data_heap_sort(cell):
    
    def heapify(array, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        cell.data_item.cmp += 1
        if l < n and array[largest] < array[l]:
            largest = l
        cell.data_item.cmp += 1
        if r < n and array[largest] < array[r]:
            largest = r
        if largest != i:
            array[i], array[largest] = array[largest], array[i]
            cell.data_item.swaps += 1
            cell.data_item.Mwrites += 2
            heapify(array, n, largest)

    def heap_sort(array):
        n = len(array)
        for i in range(n//2-1, -1, -1):
            heapify(array, n, i)
        for i in range(n-1, 0, -1):
            array[0], array[i] = array[i], array[0]
            cell.data_item.swaps += 1
            cell.data_item.Mwrites += 2
            heapify(array, i, 0)
    
    heap_sort(cell.array2.copy())


def get_data_tim_sort(cell):
    
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
                cell.data_item.cmp += 1
                array[j+1] = array[j]
                cell.data_item.Mwrites += 1
                j -= 1
            array[j+1] = element
            cell.data_item.swaps += 1
            cell.data_item.Mwrites += 1
        return array
                
    def merge(array, l, m, r): 
        array_length1 = m - l + 1
        array_length2 = r - m 
        left = []
        right = []
        for i in range(0, array_length1): 
            left.append(array[l + i])
            cell.data_item.Awrites += 1
        for i in range(0, array_length2): 
            right.append(array[m + 1 + i])
            cell.data_item.Awrites += 1
        i=0
        j=0
        k=l
        
        while j < array_length2 and  i < array_length1:
            cell.data_item.cmp += 1
            if left[i] <= right[j]:
                array[k] = left[i] 
                cell.data_item.Mwrites += 1
                i += 1
            else: 
                array[k] = right[j] 
                cell.data_item.Mwrites += 1
                j += 1
            k += 1
        
        while i < array_length1: 
            cell.data_item.cmp += 1
            array[k] = left[i] 
            cell.data_item.Mwrites += 1
            k += 1
            i += 1
        
        while j < array_length2:
            cell.data_item.cmp += 1
            array[k] = right[j]
            cell.data_item.Mwrites += 1
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
    
    tim_sort(cell.array2.copy())


def get_data_introsort(cell):
    
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
                cell.data_item.cmp += 1
                i = i + 1
            j = j - 1
            while array[j] > pivot:
                cell.data_item.cmp += 1
                j = j - 1
    
            if i >= j:
                return j
    
            swap(array, i, j)
    
    def swap(array, i, j):
        array[i], array[j] = array[j], array[i]
        cell.data_item.swaps += 1
        cell.data_item.Mwrites += 2
        
    
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
        cell.data_item.cmp += 1
        if (l < size and array[start + l] > array[start + index]):
            largest = l
        else:
            largest = index
        cell.data_item.cmp += 1
        if (r < size and array[start + r] > array[start + largest]):
            largest = r
        if largest != index:
            swap(array, start + largest, start + index)
            max_heapify(array, largest, start, end)
    
    introsort(cell.array2.copy())


def get_data_shell_sort(cell):
    
    def shell_sort(array):
        interval = len(array) // 2
        while interval > 0:
            for i in range(interval, len(array)):
                temp = array[i]
                j = i
                while j >= interval and array[j - interval] > temp:
                    cell.data_item.cmp += 1
                    array[j] = array[j - interval]
                    cell.data_item.Mwrites += 1
                    j -= interval
                array[j] = temp
                cell.data_item.Mwrites += 1
            interval //= 2
    
    shell_sort(cell.array2.copy())


def get_data_count_sort(cell):
    
    def count_sort(array):
        max_element = -1e9
        min_element = 1e9
        for i in range(len(array)):
            max_element = max(max_element, array[i])
            min_element = min(min_element, array[i])
            cell.data_item.cmp += 2
        
        
        range_of_elements = max_element - min_element + 1
        count_array = []
        for _ in range(range_of_elements):
            count_array.append(0)
            cell.data_item.Awrites += 1

        output_array = []
        for _ in range(len(array)):
            output_array.append(0)
            cell.data_item.Awrites += 1

        for i in range(0, len(array)):
            count_array[array[i]-min_element] += 1
            cell.data_item.Awrites += 1

        for i in range(1, len(count_array)):
            count_array[i] += count_array[i-1]
            cell.data_item.Awrites += 1

        for i in range(len(array)-1, -1, -1):
            output_array[count_array[array[i] - min_element] - 1] = array[i]
            cell.data_item.Awrites += 1
            count_array[array[i] - min_element] -= 1
            cell.data_item.Awrites += 1
            
        for i in range(0, len(array)):
            array[i] = output_array[i]
            cell.data_item.Mwrites += 1
    
    count_sort(cell.array2.copy())


def get_data_radix_sort(cell):
    
    def counting_sort(array, place):
        size = len(array)
        output = [0] * size
        cell.data_item.Awrites += size
        count = [0] * 10
        cell.data_item.Awrites += 10

        for i in range(0, size):
            index = array[i] // place
            count[index % 10] += 1
            cell.data_item.Awrites += 1
        

        for i in range(1, 10):
            count[i] += count[i - 1]
            cell.data_item.Awrites += 1

        i = size - 1
        while i >= 0:
            index = array[i] // place
            output[count[index % 10] - 1] = array[i]
            cell.data_item.Awrites += 1
            count[index % 10] -= 1
            cell.data_item.Awrites += 1
            i -= 1

        for i in range(0, size):
            array[i] = output[i]
            cell.data_item.Mwrites += 1
    
    def radix_sort(array):
        max_element = max(array)
        for i in range(len(array)):
            cell.data_item.cmp += 1
            max_element = max(max_element, array[i])
        
        place = 1
        while max_element // place > 0:
            counting_sort(array, place)
            place *= 10
    
    radix_sort(cell.array2.copy())