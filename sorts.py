def insertion_sort_scores(lst):         #sort the scores from highest to lowest using insertion sort algorithm
    length = len(lst)
    for i in range(1, length):
        temp = lst[i]
        j = i-1
        while j >= 0 and temp[2] > lst[j][2]:

            if temp[2] > lst[j][2] :        # If score is greater
                lst[j+1] = lst[j]           # Swap element at jth position with (j+1)th position
                j -= 1
        else:
            lst[j+1] = temp
            
def bubble_sort_time(lst):          # sort the scores, if equal, based on time taken to complete from lowest to highest
                                    # using bubble sort algorithm
    n = len(lst)
    for i in range(n): # Number of passes
        for j in range(0, n-i-1):
    
            if lst[j][2] == lst[j+1][2]:                    # Check if scores are equal
                if lst[j][3] > lst[j+1][3]:                 # If time is greater
                    lst[j], lst[j+1] = lst[j+1], lst[j]     # Swap element at jth position with (j+1)th position

