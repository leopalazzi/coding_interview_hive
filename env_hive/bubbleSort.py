def bubbleSort(array): 
  # loop through each element of array
  for i in range(len(array)):   
    # keep track of swapping
    isSwapped = False
    # loop to compare array elements
    for j in range(0, len(array) - i - 1):
      # compare two adjacent elements
      if array[j] > array[j + 1]:
        # swapping occurs if elements are not in the intended order
        temp_var = array[j]
        array[j] = array[j+1]
        array[j+1] = temp_var
        isSwapped = True 
    # if there is  swapping means the array is already sorted
    if not swapped:
      break
    print(array)