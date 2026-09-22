import timeit

tests_number = 10
gc = False

def execute(function):
    if (gc):
        return round(timeit.timeit(lambda: function(), 'gc.enable()', number=tests_number)/tests_number*1000, 3)
    else:
        return round(timeit.timeit(lambda: function(), 'gc.disable()', number=tests_number)/tests_number*1000, 3)


def none_function(*args, **kwargs):
    return None


def time_bubble_sort(array):

    def bubble_sort(array):
        for i in range(len(array)-1):
            for j in range(len(array)-i-1):
                if (array[j] > array[j+1]):
                    array[j], array[j+1] = array[j+1], array[j]

    return execute(lambda array=array: bubble_sort(array.copy()))


def time_insertion_sort(array):
    
    def insertion_sort(array):
        for i in range(1, len(array)):
            el = array[i]
            j = i-1
            while (j >= 0 and el < array[j]):
                    array[j + 1] = array[j]
                    j -= 1
            array[j + 1] = el

    return execute(lambda array=array: insertion_sort(array.copy()))


def time_selection_sort(array):
    
    def selection_sort(array):
        for i in range(len(array)-1):
            imin = i
            for j in range(i+1, len(array)):
                if (array[j] < array[imin]):
                    imin = j
            array[i], array[imin] = array[imin], array[i]

    return execute(lambda array=array: selection_sort(array.copy()))


def time_quick_sort(array):
    
    def quick_sort(array, front, back):
        if (front >= back):
            return None
        l = front
        r = back
        x = array[(l+r)//2]
        while (l <= r):
            while (array[l] < x):
                l += 1
            while (array[r] > x):
                r -= 1
            if (l <= r):
                array[l], array[r] = array[r], array[l]
                l += 1
                r -= 1
        quick_sort(array, front, r)
        quick_sort(array, l, back)
    
    return execute(lambda array=array, front=0, back=len(array)-1: quick_sort(array.copy(), front, back))


def time_merge_sort(array):
    
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
            q += 1
        while (i < len(tmp1)):
            array[q] = tmp1[i]
            i += 1
            q += 1
        while (j < len(tmp2)):
            array[q] = tmp2[j]
            j += 1
            q += 1
    
    def merge_sort(array, l, r):
        if (l < r):
            m = (l+r) // 2
            merge_sort(array, l, m)
            merge_sort(array, m + 1, r)
            merge(array, l, m, r)
    
    return execute(lambda array=array, l=0, r=len(array)-1: merge_sort(array.copy(), l, r))


def time_shaker_sort(array):
    
    def shaker_sort(array):
        swapped = True
        start = 0
        end = len(array)-1
        while (swapped):
            swapped = False
            for i in range(start, end):
                if (array[i] > array[i+1]):
                    array[i], array[i+1] = array[i+1], array[i]
                    swapped=True
            if (not(swapped)):
                break
            swapped = False
            end -= 1
            for i in range(end-1, start-1, -1):
                if (array[i] > array[i+1]):
                    array[i], array[i+1] = array[i+1], array[i]
                    swapped = True
            start += 1
    
    return execute(lambda array=array: shaker_sort(array.copy()))


def time_gnome_sort(array):

    def gnome_sort(array):
        if (len(array) == 1):
            return
        i = 0
        while (i < len(array)):
            if i == 0:
                i += 1
            if (array[i] >= array[i - 1]):
                i += 1
            else:
                array[i], array[i-1] = array[i-1], array[i]
                i -= 1
    
    return execute(lambda array=array: gnome_sort(array.copy()))


def time_odd_even_sort(array):
    
    def odd_even_sort(array):
        is_sorted = False
        while (not(is_sorted)):
            is_sorted = True
            for i in range(1, len(array)-1, 2):
                if (array[i] > array[i+1]):
                    array[i], array[i+1] = array[i+1], array[i]
                    is_sorted = False
                    
            for i in range(0, len(array)-1, 2):
                if (array[i] > array[i+1]):
                    array[i], array[i+1] = array[i+1], array[i]
                    is_sorted = False
    
    return execute(lambda array=array: odd_even_sort(array.copy()))


def time_comb_sort(array):
        
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
    
    return execute(lambda array=array: comb_sort(array.copy()))


def time_heap_sort(array):
    
    def heapify(array, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if (l < n and array[largest] < array[l]):
            largest = l
        if (r < n and array[largest] < array[r]):
            largest = r
        if (largest != i):
            array[i], array[largest] = array[largest], array[i]
            heapify(array, n, largest)

    def heap_sort(array):
        n = len(array)
        for i in range(n//2-1, -1, -1):
            heapify(array, n, i)
        for i in range(n-1, 0, -1):
            array[i], array[0] = array[0], array[i]
            heapify(array, i, 0)
    
    return execute(lambda array=array: heap_sort(array.copy()))


def time_tim_sort(array):
    
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
                j -= 1
            array[j+1] = element
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
                i += 1
            else: 
                array[k] = right[j] 
                j += 1
            k += 1
        
        while i < array_length1: 
            array[k] = left[i] 
            k += 1
            i += 1
        
        while j < array_length2: 
            array[k] = right[j] 
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
    
    return execute(lambda array=array: tim_sort(array.copy()))


def time_introsort(array):
    
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
                i = i + 1
            j = j - 1
            while array[j] > pivot:
                j = j - 1
    
            if i >= j:
                return j
    
            swap(array, i, j)
    
    def swap(array, i, j):
        array[i], array[j] = array[j], array[i]
    
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
    
    return execute(lambda array=array: introsort(array.copy()))


def time_shell_sort(array):
    
    def shell_sort(array):
        interval = len(array) // 2
        while interval > 0:
            for i in range(interval, len(array)):
                temp = array[i]
                j = i
                while j >= interval and array[j - interval] > temp:
                    array[j] = array[j - interval]
                    j -= interval
                array[j] = temp
            interval //= 2
    
    return execute(lambda array=array: shell_sort(array.copy()))


def time_count_sort(array):
    
    def count_sort(array):
        max_element = -1e9
        min_element = 1e9
        for i in range(len(array)):
            max_element = max(max_element, array[i])
            min_element = min(min_element, array[i])
        range_of_elements = max_element - min_element + 1
        
        count_array = []
        for _ in range(range_of_elements):
            count_array.append(0)
        
        output_array = []
        for _ in range(len(array)):
            output_array.append(0)

        for i in range(0, len(array)):
            count_array[array[i]-min_element] += 1

        for i in range(1, len(count_array)):
            count_array[i] += count_array[i-1]

        for i in range(len(array)-1, -1, -1):
            output_array[count_array[array[i] - min_element] - 1] = array[i]
            count_array[array[i] - min_element] -= 1

        for i in range(0, len(array)):
            array[i] = output_array[i]
    
    return execute(lambda array=array: count_sort(array.copy()))


def time_radix_sort(array):
    
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
            count[index % 10] -= 1
            i -= 1

        for i in range(0, size):
            array[i] = output[i]
    
    def radix_sort(array):
        max_element = max(array)
        for i in range(len(array)):
            max_element = max(max_element, array[i])

        place = 1
        while max_element // place > 0:
            counting_sort(array, place)
            place *= 10
    
    return execute(lambda array=array: radix_sort(array.copy()))