def validate_list_index(index, list):
    if index < 0 :
        print("The given index was smaller then 0")
        index = 0

    list_len = len(list)

    if list_len == 0:
        raise IndexError("The list is empty")

    if index >= list_len:
        print("The given index was bigger then the length of the list")
        index = list_len - 1

    return index