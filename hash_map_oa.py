# Name: Ted Janney
# OSU Email: janneyt@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 7
# Due Date: 4/6/2022
# Description: Implement a hash map using open addressing


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

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

    # ------------------------------------------------------------------ #)




    def put(self, key: str, value: object) -> None:
        """
        Puts a key/value pair into an open addressing Hashmap
        """

        # Resize if table load is too high
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        initial = self._hash_function(key) % self._capacity
        entry = self._buckets[initial]
        counter = 1

        # Just in case we skip while loop
        new_index = initial

        # Quadratic probing/update logic
        while entry is not None:

            # Either it's an update
            if entry.key == key and not entry.is_tombstone:
                entry.value = value
                entry.is_tombtone = False
                return

            # A formerly deleted value
            elif entry.key == key and entry.is_tombstone:
                entry.key = key
                entry.value = value
                entry.is_tombstone = False
                self._size += 1
                return

            # Or we need to continue quadratic probing
            new_index = (initial + counter ** 2) % self._capacity
            entry = self._buckets[new_index]
            counter += 1

        # Entry is none, so need to create a hashmap entry instead of reusing old ones
        self._buckets[new_index] = HashEntry(key, value)

        self._size += 1


    def table_load(self) -> float:
        """
        Computes the table load as number of elements divided by number of buckets in a HashMap
        """
        return self._size/self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets.

        The empty buckets tests seem to treat both tombstone and non-tombstone values as non-empty.
        """
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the table based on the new_capacity parameter

        Can both grow and shrink the table
        """

        # These are nonsensical capacities and are rejected
        if new_capacity < 1 or new_capacity < self._size:
            return

        # Setup some temp variables to help with swap operations.
        old_capacity = self._capacity
        self._capacity = new_capacity
        new_da = DynamicArray()
        temp_da = self._buckets

        # We need to have a Dynamic Array that is entirely full of None values in order to rehash everything
        for num_element in range(new_capacity):
            new_da.append(None)

        self._buckets = new_da
        self._size = 0

        # Switch in and rehash the the old bucket values. Note: the tombstone issue is taken care of by the put method
        for entries in range(old_capacity):
            entry = temp_da[entries]
            if entry is not None:
                self.put(entry.key, entry.value)

    def get(self, key: str) -> object:
        """
        Gets the value associated with a key

        This is a pretty basic traverse (see also remove, contains keys, etc). The difference is really just the return value
        """
        initial = self._hash_function ( key ) % self._capacity
        entry = self._buckets[initial]
        counter = 1

        # Continue quadratic probing until a value that is either a tombstone or None is reached, then return
        # Due to resizing, the table will never have zero None values, so this is not an infinite loop
        while entry is not None and not entry.is_tombstone:
            print(entry)
            if entry.key == key:
                return entry.value
            entry = self._buckets[(initial + counter ** 2) % self._capacity]
            counter += 1

    def contains_key(self, key: str) -> bool:
        """
        Returns a boolean indicating if a key is found by using the same quadratic probing that put it in the hashmap
        in the first place
        """
        initial = self._hash_function ( key ) % self._capacity
        entry = self._buckets[initial]
        counter = 1

        # Traversal as per other methods
        while entry is not None:
            if entry.key == key:
                return True
            entry = self._buckets[(initial + counter ** 2) % self._capacity]
            counter += 1
        return False

    def remove(self, key: str) -> None:
        """
        Removes a value by setting the tombstone to True, which allows later values to be inserted and will be
        skipped for other tasks
        """
        initial = self._hash_function ( key ) % self._capacity
        entry = self._buckets[initial]
        counter = 1
        while entry is not None:

            # Found it, set to true
            if entry.key == key and not entry.is_tombstone:
                entry.is_tombstone = True
                self._size -= 1
                return
            entry = self._buckets[(initial + counter ** 2) % self._capacity]
            counter += 1

    def clear(self) -> None:
        """
        This brute forces the elements all to None, but retains the capacity. Note that size is set to be zero
        """
        for num_elements in range(self._buckets.length()):
            self._buckets[num_elements] = None
        self._size = 0


    def get_keys(self) -> DynamicArray:
        """
        Returns all keys in the hashmap.
        """
        ret_da = DynamicArray ()
        for num_elements in range ( self._buckets.length () ):
            entry = self._buckets[num_elements]
            if entry is not None and not entry.is_tombstone:
                ret_da.append ( entry.key )
        return ret_da



# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())
    '''
    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

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

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))
    '''
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
