# Name: Ted Janney
# OSU Email: janneyt@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 7
# Due Date: 4/6/2022
# Description: Implements a hash map using separate chaining


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Puts a new key/value pair into the hashmap
        """

        # Modulo to keep the index within the bounds of the array
        index = self._hash_function(key) % self._capacity

        node = self._buckets[index]._head

        # This is the basic form of traversal. Go along the dynamic array...then up the linked list until you find what
        # you're looking for
        while node:
            if node.key == key:
                node.value = value
                return
            node = node.next

        self._buckets[index].insert(key, value)
        self._size += 1


    def empty_buckets(self) -> int:
        """
        Counts the number of empty buckets in the hashmap
        """
        num_buckets = 0
        for bucket in range(self._capacity):

            # An empty bucket is one with length zero (from the linked list class)
            if self._buckets[bucket].length() == 0:
                num_buckets += 1
        return num_buckets

    def table_load(self) -> float:
        """
        Computes the table load as number of elements divided by number of buckets in a HashMap

        Not really used in the SC implementation, although perhaps if there was a dreadful mismatch you could start resizing

        """
        return self._size/self._capacity

    def clear(self) -> None:
        """
        Clears the entire hashmap without changing the capacity
        """
        for num_bucket in range(self._buckets.length()):
            if self._buckets[num_bucket].length != 0:
                self._buckets[num_bucket] = LinkedList()
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes a table by doubling the capacity and rehashes only the full indices

        Again, not really used in the SC implementation, but on particularly large orders would probably be required
        """
        if new_capacity < 1:
            return
        old_capacity = self._capacity
        self._capacity = new_capacity


        # Divided processing into two divisions. If the dynamic array is expanding, we have to add linked lists to the
        # dynamic array, thus also expanding the dynamic array
        if new_capacity >= old_capacity:
            for elements in range(new_capacity-old_capacity):
                self._buckets.append(LinkedList())

        # This is the actual "resize", as it were.
        for element in range(old_capacity):
            if self._buckets[element].length() > 0:

                # Standard traversal
                node = self._buckets[element]._head
                while node:

                    # Insert the value at the front, remove it from wherever it is hiding in the linked list
                    index = self._hash_function(node.key) % self._capacity
                    self._buckets[index].insert(node.key, node.value)
                    self._buckets[element].remove(node.key)
                    node = node.next
        # This is the second division of processing, this time for lists that are shrinking. The capacity needs to
        # already be set correctly for this to work, while above there are index out of bounds errors if the capacity
        # is set too early
        if old_capacity > new_capacity:
            for elements in range(old_capacity, new_capacity, -1):
                self._buckets.pop()
        return



    def get(self, key: str) -> object:
        """
        Gets a key/value pair from the hashmap, or none if there is no such key
        """
        index = self._hash_function(key) % self._capacity
        linklist = self._buckets[index]._head
        while linklist:

            # Aside from the standard traversal, the important factor here is that we're returning something
            if linklist.key == key:
                return linklist.value
            else:
                linklist = linklist.next
        return None


    def contains_key(self, key: str) -> bool:
        """
        Returns true if the key is in the hashmap, false if not
        """
        index = self._hash_function ( key ) % self._capacity
        node = self._buckets[index]._head
        while node:
            if node.key == key:
                return True
            node = node.next
        return False

    def remove(self, key: str) -> None:
        """
        Removes a value from the hashmap (no response if key is not found)
        """
        index = self._hash_function ( key ) % self._capacity
        linklist = self._buckets[index]

        # The remove method on the linked list actually returns True or False/None, so use that to determine whether
        # size needs to be altered
        if linklist.remove(key):
            self._size -= 1

    def get_keys(self) -> DynamicArray:
        """
        Returns all keys in the hashmap
        """
        new_da = DynamicArray()
        for num_slots in range(self._buckets.length()):
            if self._buckets[num_slots].length() != 0:
                node = self._buckets[num_slots]._head
                while node:
                    new_da.append(node.key)
                    node = node.next
        return new_da


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Finds the mode of all elements in a dynamicarray by first converting it to a hashmap
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    ret_da = DynamicArray()
    map = HashMap(da.length() // 3, hash_function_1)
    max = 0

    for elements in range(da.length()):

        # Iterate along DA, with each key/value pair actually being the key in the original DA, and then the frequency
        key = da[elements]
        current = map.get(key)
        if current is not None:
            current += 1
        else:

            # Sets the initial frequency to 1
            current = 1

        # Store the key/value pair again
        map.put(key,current)

        # Maintain the max value to know if we need this value as the mode
        if current > max:
            max = current

            # Add to the return DA after clearing out the Dynamic Array of previous contenders for Mode
            ret_da = DynamicArray()
            ret_da.append(key)

        # If we have another instance of the same mode, add to the return DA
        elif current == max:
            max = current
            ret_da.append(key)


    return(ret_da, max)

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")
