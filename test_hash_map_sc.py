import unittest
from hash_map_sc import *

class MyTestCase ( unittest.TestCase ):
    def test_hash_map_builtin(self):
        hm = HashMap(50, hash_function_1)

        hm.put("name","Ted")
        self.assertEqual(hm.empty_buckets(),49)
        self.assertEqual(hm.get_size(),1)
        self.assertEqual(hm.get_capacity(),50)
        self.assertEqual(hm._buckets[17]._head.value, "Ted")
        counter = 0
        for i in range(50):
            hm.put('str' + str(i), i*100)
            if i % 25 == 24 and counter == 1:
                self.assertEqual(hm.empty_buckets(),39)
                self.assertEqual(hm.get_size(),25)
                self.assertEqual(hm.get_capacity(), 50)

                counter += 1
            elif i % 25 == 24 and counter == 2:
                self.assertEqual(hm.empty_buckets(), 37)
                self.assertEqual(hm.get_size(), 50)
                self.assertEqual(hm.get_capacity(), 50)
                counter += 1
            elif i % 25 == 24 and counter == 3:
                self.assertEqual(hm.empty_buckets(), 35)
                self.assertEqual(hm.get_size(), 75)
                self.assertEqual(hm.get_capacity(), 50)
                counter += 1
            elif i % 25 == 24 and counter == 4:
                self.assertEqual(hm.empty_buckets(), 32)
                self.assertEqual(hm.get_size(), 100)
                self.assertEqual(hm.get_capacity(), 50)
                counter += 1
            elif i % 25 == 24 and counter == 5:
                self.assertEqual(hm.empty_buckets(), 30)
                self.assertEqual(hm.get_size(), 125)
                self.assertEqual(hm.get_capacity(), 50)
                counter += 1
            elif i % 25 == 24 and counter == 6:
                self.assertEqual(hm.empty_buckets(), 30)
                self.assertEqual(hm.get_size(), 150)
                self.assertEqual(hm.get_capacity(), 50)
                counter += 1
        m = HashMap(40, hash_function_2)
        counter = 0
        for i in range(50):
            m.put('str'+ str(i//3), i*100)
            if i % 10 == 9 and counter == 0:
                self.assertEqual(m.empty_buckets(), 36)
                self.assertEqual(m.get_size(), 4)
                self.assertEqual(m.get_capacity(), 40)
                counter += 1
            elif i % 10 == 9 and counter == 1:
                self.assertEqual(m.empty_buckets(), 33)
                self.assertEqual(m.get_size(), 7)
                self.assertEqual(m.get_capacity(), 40)
                counter += 1
            elif i % 10 == 9 and counter == 2:
                self.assertEqual(m.empty_buckets(), 30)
                self.assertEqual(m.get_size(), 10)
                self.assertEqual(m.get_capacity(), 40)
                counter += 1
            elif i % 10 == 9 and counter == 3:
                self.assertEqual(m.empty_buckets(), 27)
                self.assertEqual(m.get_size(), 14)
                self.assertEqual(m.get_capacity(), 40)
                counter += 1
            elif i % 10 == 9 and counter == 4:
                self.assertEqual(m.empty_buckets(), 25)
                self.assertEqual(m.get_size(), 17)
                self.assertEqual(m.get_capacity(), 40)
                counter += 1

    def test_empty_buckets(self):
        hm = HashMap(50, hash_function_1)
        self.assertEqual(hm.empty_buckets(),50)
        m = HashMap(100, hash_function_1)
        self.assertEqual ( m.empty_buckets (), 100)
        self.assertEqual(m.get_size(),0)
        self.assertEqual(m.get_capacity(),100)
        m.put('key1', 10)
        self.assertEqual(m.empty_buckets(), 99)
        self.assertEqual(m.get_size(),1)
        self.assertEqual(m.get_capacity(),100)
        m.put('key2',20)

        self.assertEqual(m.empty_buckets(), 98)
        self.assertEqual(m.get_size(),2)
        self.assertEqual(m.get_capacity(),100)

        m.put('key1', 30)

        self.assertEqual(m.empty_buckets(), 98)
        self.assertEqual(m.get_size(),2)
        self.assertEqual(m.get_capacity(),100)

        m.put('key4',40)

        self.assertEqual(m.empty_buckets(), 97)
        self.assertEqual(m.get_size(),3)
        self.assertEqual(m.get_capacity(),100)

        m2 = HashMap ( 50, hash_function_1 )
        counter = 0
        for i in range ( 150 ):
            m2.put ( 'key' + str ( i ), i * 100 )
            if i % 30 == 0 and counter == 0:
                self.assertEqual(m2.empty_buckets(), 49)
                self.assertEqual(m2.get_size(),1)
                self.assertEqual(m2.get_capacity(), 50)
                counter += 1
            elif i % 30 == 0 and counter == 1:
                self.assertEqual(m2.empty_buckets(), 39)
                self.assertEqual(m2.get_size(),31)
                self.assertEqual(m2.get_capacity(), 50)
                counter += 1
            elif i % 30 == 0 and counter == 2:
                self.assertEqual(m2.empty_buckets(), 36)
                self.assertEqual(m2.get_size(),61)
                self.assertEqual(m2.get_capacity(), 50)
                counter += 1
            elif i % 30 == 0 and counter == 3:
                self.assertEqual(m2.empty_buckets(), 33)
                self.assertEqual(m2.get_size(),91)
                self.assertEqual(m2.get_capacity(), 50)
                counter += 1
            elif i % 30 == 0 and counter == 4:
                self.assertEqual(m2.empty_buckets(), 30)
                self.assertEqual(m2.get_size(),121)
                self.assertEqual(m2.get_capacity(), 50)
                counter += 1

    def test_resize_tables(self):
        m = HashMap(20, hash_function_1)
        m.put('key1',10)
        self.assertEqual(m.get_size(),1)
        self.assertEqual(m.get_capacity(),20)
        self.assertEqual(m.get('key1'),10)
        self.assertTrue(m.contains_key('key1'))
        m.resize_table(30)
        self.assertEqual(m.get_size(),1)
        self.assertEqual(m.get_capacity(),30)
        self.assertEqual(m.get('key1'),10)
        self.assertTrue(m.contains_key('key1'))

    def test_table_load(self):
        m = HashMap(100, hash_function_1)
        self.assertEqual(m.table_load(),0.0)
        m.put('key1',10)
        self.assertEqual(m.table_load(),0.01)
        m.put ( 'key2', 20 )
        self.assertEqual(m.table_load (),0.02 )
        m.put ( 'key1', 30 )
        self.assertEqual(m.table_load (), 0.02 )

        m2 = HashMap ( 50, hash_function_1 )
        counter = 0
        for i in range ( 50 ):
            m2.put ( 'key' + str ( i ), i * 100 )
            if i % 10 == 0 and counter == 0:
                self.assertEqual(m2.table_load(),0.02)
                self.assertEqual(m2.get_size(),1)
                self.assertEqual(m2.get_capacity(),50)
                counter += 1
            elif i % 10 == 0 and counter == 1:
                self.assertEqual(m2.table_load(),0.22)
                self.assertEqual(m2.get_size(),11)
                self.assertEqual(m2.get_capacity(),50)
                counter += 1
            elif i % 10 == 0 and counter == 2:
                self.assertEqual(m2.table_load(),0.42)
                self.assertEqual(m2.get_size(),21)
                self.assertEqual(m2.get_capacity(),50)
                counter += 1
            elif i % 10 == 0 and counter == 3:
                self.assertEqual(m2.table_load(),0.62)
                self.assertEqual(m2.get_size(),31)
                self.assertEqual(m2.get_capacity(),50)
                counter += 1
            elif i % 10 == 0 and counter == 1:
                self.assertEqual(m2.table_load(),0.82)
                self.assertEqual(m2.get_size(),41)
                self.assertEqual(m2.get_capacity(),50)
                counter += 1
    def test_clear(self):
        m = HashMap ( 100, hash_function_1 )
        self.assertEqual(m.get_size(),0)
        self.assertEqual(m.get_capacity(),100)
        m.put ( 'key1', 10 )
        m.put ( 'key2', 20 )
        m.put ( 'key1', 30 )
        self.assertEqual(m.get_size(),2)
        self.assertEqual(m.get_capacity(),100)
        m.clear ()
        self.assertEqual(m.get_size(),0)
        self.assertEqual(m.get_capacity(),100)

    def test_get(self):
        m = HashMap(30, hash_function_1)
        self.assertIsNone(m.get('key1'))
        m.put('key1',10)
        self.assertEqual(m.get('key1'),10)
if __name__ == '__main__':
    unittest.main ()
