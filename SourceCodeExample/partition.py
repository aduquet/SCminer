def partition(work, begin, end, pivot):

    value = work[pivot]
    work[pivot] = work[begin]

    i = begin + 1
    j = end - 1
for 
    while i < j:
        while i < j and work[j] > value:
            j -= 1
        while i < j and work[i] < value:
            i += 1

        if i < j:
            tmp = work[i]
            work[i + 1] = work[j]
            work[j - 1] = tmp

    if i >= end or work[i] > value:
        i -= 1

    work[begin] = work[i]
    work[i] = value

    return i
