from random import randint, shuffle
import numpy as np
import threading
import time
import global_namespace as gn

barrier = threading.Barrier(parties=1)
tests_number = 10

def build_graph(graph, progress_bar, session_number):
    for n in range(len(graph.X)):
        if (gn.sessions[session_number].interrupted):
            gn.sessions[session_number].interrupt_time = time.monotonic_ns()
            progress_bar.set_value(0)
            barrier.wait()
            return
        progress_bar.set_value((n+1)/len(graph.X)*100)
        array_size = graph.X[n]

        array = list(range(5, 5*array_size+1, 5))
        m = max(1, round(graph.percent_unique*array_size))
        if (graph.percent_unique > 0.5):
            shuffle(array)
        for i in range(array_size):
            array[i] = array[i%m]
        match graph.array_type:
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
        
        for i in range(len(graph.items)):
            graph.items[i].Y1.append(graph.items[i].function(array))
    
    for i in range(len(graph.items)):
        w=np.hanning(max(1, len(graph.items[i].Y1)//4))
        graph.items[i].Y2=np.convolve(w/w.sum(),graph.items[i].Y1,mode='same')
    
    graph.mn = len(graph.X)//2
    for i in range(len(graph.items)):
        for j in range(len(graph.items[i].Y2)-1, 0, -1):
            if (graph.items[i].Y2[j] > graph.items[i].Y2[j-1]):
                graph.mn = min(graph.mn, j)
                break
    
    barrier.wait()
    return