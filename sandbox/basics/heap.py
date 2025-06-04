# j.siedersleben
# fasttrack to professional programming
# lesson 2: collections
# 24.12.2020


########################################
##           Handmade Heap            ##
########################################

# tree-like data structure on a list.
# Invariants:
# heap[0] is smallest element
# heap[k] <= heap[2*k+1] and heap[2*k+2]
# popping all elements yields a non-descending list

########################################

def heappush(heap: list, x):
    """
    :param heap: a list organized as a heap
    :param x: object to be inserted
    :return: None
    Idea: put x at last position; let x rise to desired position
    Complexity = O(log n)
    """
    heap.append(x)

    # start at tail, heap now contains at least one element
    child = len(heap) - 1  # heap[j] == x, x is last element

    while True:
        # find parent of child if any
        if child == 0:
            return
        else:
            parent = (child - 1) // 2

        # swap heap[child] and heap[parent] if necessary, otherwise stop
        if heap[parent] > heap[child]:
            heap[child], heap[parent] = heap[parent], heap[child]
            child = parent  # one step up
        else:
            return


def heappop(heap):
    """
    :param heap: a list organized as a heap
    :return: heap[0] which is the smallest element
    Idea: put last element at 0 = root; let it sink to desired position
    Complexity = O(log n)
    """
    result = heap[0]  # exception if heap is empty
    last = heap.pop()  # remove last element

    if len(heap) == 0:
        return result
    else:  # put last element at 0
        heap[0] = last

    parent = 0  # start at root

    while True:
        # find children of parent if any
        child1, child2 = 2 * parent + 1, 2 * parent + 2

        if child1 >= len(heap):  # no children
            return result
        elif child2 >= len(heap):  # just one child
            child = child1
        else:  # take child with smaller value
            child = child1 if heap[child1] <= heap[child2] else child2

        # swap heap[child] and heap[parent] if necessary, otherwise stop
        if heap[parent] > heap[child]:
            heap[child], heap[parent] = heap[parent], heap[child]
            parent = child  # one step down
        else:
            return result


# These algorithms wrapped in a class

class Heap(list):
    # heappush(h, x) becomes h.heappush(x)
    # which is the same as heappush(self, x)
    # Note that
    # left of = : local namespace
    # right of = : global namespace
    # So, what happens is in fact
    # Heap.heappush = heappush
    # Heap.heappop = heappop

    heappush = heappush
    heappop = heappop
