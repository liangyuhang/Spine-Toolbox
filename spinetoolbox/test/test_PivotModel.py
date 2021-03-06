######################################################################################################################
# Copyright (C) 2017 - 2018 Spine project consortium
# This file is part of Spine Toolbox.
# Spine Toolbox is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

"""
Unit tests for PivotModel class.

:author: P. Vennström (VTT)
:date:   16.11.2018
"""

import unittest
from unittest import mock
from tabularview_models import PivotModel


class TestPivotModel(unittest.TestCase):

    def setUp(self):
        self.data = [['a', 'aa', 1, 'value_a_aa_1'],
                     ['a', 'bb', 2, 'value_a_bb_2'],
                     ['b', 'cc', 3, 'value_b_cc_3'],
                     ['c', 'cc', 4, 'value_c_cc_4'],
                     ['d', 'dd', 5, 'value_d_dd_5'],
                     ['e', 'ee', 5, 'value_e_ee_5']]
        self.index_names = ['test1','test2','test3']
        self.index_types = [str, str, int]
        self.dict_data = {('a', 'aa', 1): 'value_a_aa_1',
                          ('a', 'bb', 2): 'value_a_bb_2',
                          ('b', 'cc', 3): 'value_b_cc_3',
                          ('c', 'cc', 4): 'value_c_cc_4',
                          ('d', 'dd', 5): 'value_d_dd_5',
                          ('e', 'ee', 5): 'value_e_ee_5'}
        self.tuple_index_entries = {('test1', 'test2'): set([('f', 'ee'), ('a', 'cc')]),
                                    ('test3',): set([(6,)])}

    def test_init_model(self):
        PivotModel()
    
    def test_set_data(self):
        """test set model data"""
        row_headers = [('a', 'aa', 1),
                       ('a', 'bb', 2),
                       ('b', 'cc', 3),
                       ('c', 'cc', 4),
                       ('d', 'dd', 5),
                       ('e', 'ee', 5)]
        column_headers = []
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        self.assertEqual(model._data, self.dict_data)
        self.assertEqual(model.index_names, tuple(self.index_names))
        self.assertEqual(model.pivot_rows, tuple(self.index_names))
        self.assertEqual(model.pivot_columns, ())
        self.assertEqual(model.pivot_frozen, ())
        self.assertEqual(model.frozen_value, ())
        self.assertEqual(model._row_data_header, row_headers)
        self.assertEqual(model._column_data_header, column_headers)
        self.assertEqual(model._row_data_header_set, set(row_headers))
        self.assertEqual(model._column_data_header_set, set(column_headers))
    
    def test_set_data2(self):
        """Test set data with tuple_index_entries"""
        row_headers = [('a', 'aa', 1),
                       ('a', 'bb', 2),
                       ('b', 'cc', 3),
                       ('c', 'cc', 4),
                       ('d', 'dd', 5),
                       ('e', 'ee', 5),
                       ('a', 'cc', None),
                       ('f', 'ee', None),
                       (None, None, 6)]
        column_headers = []
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, tuple_index_entries=self.tuple_index_entries)
        self.assertEqual(model._data, self.dict_data)
        self.assertEqual(model.index_names, tuple(self.index_names))
        self.assertEqual(model.pivot_rows, tuple(self.index_names))
        self.assertEqual(model.pivot_columns, ())
        self.assertEqual(model.pivot_frozen, ())
        self.assertEqual(model.frozen_value, ())
        self.assertEqual(model._row_data_header, row_headers)
        self.assertEqual(model._column_data_header, column_headers)
        self.assertEqual(model._row_data_header_set, set(r for r in row_headers if all(r)))
        self.assertEqual(model._column_data_header_set, set(column_headers))
        self.assertEqual(model._invalid_row, set([6,7,8]))
        
    def test_set_data3(self):
        """Test set data with pivot and tuple_index_entries"""
        column_headers = [('a', 'aa', 1),
                       ('a', 'bb', 2),
                       ('b', 'cc', 3),
                       ('c', 'cc', 4),
                       ('d', 'dd', 5),
                       ('e', 'ee', 5),
                       ('a', 'cc', None),
                       ('f', 'ee', None),
                       (None, None, 6)]
        row_headers = []
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, rows=(), columns=tuple(self.index_names), tuple_index_entries=self.tuple_index_entries)
        self.assertEqual(model._data, self.dict_data)
        self.assertEqual(model.index_names, tuple(self.index_names))
        self.assertEqual(model.pivot_rows, ())
        self.assertEqual(model.pivot_columns, tuple(self.index_names))
        self.assertEqual(model.pivot_frozen, ())
        self.assertEqual(model.frozen_value, ())
        self.assertEqual(model._row_data_header, row_headers)
        self.assertEqual(model._column_data_header, column_headers)
        self.assertEqual(model._row_data_header_set, set(r for r in row_headers if all(r)))
        self.assertEqual(model._column_data_header_set, set(r for r in column_headers if all(r)))
        self.assertEqual(model._invalid_column, set([6,7,8]))
    
    def test_set_pivot(self):
        """Test set_pivot"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        model.set_pivot(['test1','test2'], ['test3'], [], ())
        row_headers = [('a', 'aa'),
                       ('a', 'bb'),
                       ('b', 'cc'),
                       ('c', 'cc'),
                       ('d', 'dd'),
                       ('e', 'ee')]
        column_headers = [(1,), (2,), (3,), (4,), (5,)]
        self.assertEqual(model._row_data_header, row_headers)
        self.assertEqual(model._column_data_header, column_headers)
        self.assertEqual(model._row_data_header_set, set(row_headers))
        self.assertEqual(model._column_data_header_set, set(column_headers))
        
    
    def test_set_pivot_with_frozen(self):
        """Test set_pivot with frozen dimension"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        model.set_pivot(['test2'], ['test3'], ['test1'], ('a',))
        row_headers = [('aa',),
                       ('bb',)]
        data = [['value_a_aa_1', None],
                [None, 'value_a_bb_2']]
        column_headers = [(1,), (2,)]
        data_model = [[d for d in inner] for inner in model.get_pivoted_data(range(2),range(2))]
        self.assertEqual(model._row_data_header, row_headers)
        self.assertEqual(model._column_data_header, column_headers)
        self.assertEqual(model._row_data_header_set, set(row_headers))
        self.assertEqual(model._column_data_header_set, set(column_headers))
        self.assertEqual(data_model, data)
    
    def test_set_pivot_with_frozen2(self):
        """Test set_pivot with frozen dimension and tuple_index_entries"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, tuple_index_entries=self.tuple_index_entries)
        model.set_pivot(['test2'], ['test3'], ['test1'], ('a',))
        row_headers = [('aa',),
                       ('bb',),
                       ('cc',)]
        column_headers = [(1,), (2,), (3,), (4,), (5,), (6,)]
        self.assertEqual(model._row_data_header, row_headers)
        self.assertEqual(model._column_data_header, column_headers)
        self.assertEqual(model._row_data_header_set, set(row_headers))
        self.assertEqual(model._column_data_header_set, set(column_headers))
        
    
    def test_set_pivot2(self):
        """Test set_pivot with tuple_index_entries"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, tuple_index_entries=self.tuple_index_entries)
        model.set_pivot(['test1','test2'], ['test3'], [], ())
        column_headers = [(1,), (2,), (3,), (4,), (5,), (6,)]
        row_headers = [('a', 'aa'),
                       ('a', 'bb'),
                       ('a', 'cc'),
                       ('b', 'cc'),
                       ('c', 'cc'),
                       ('d', 'dd'),
                       ('e', 'ee'),
                       ('f', 'ee')]
        self.assertEqual(model._row_data_header, row_headers)
        self.assertEqual(model._column_data_header, column_headers)
        self.assertEqual(model._row_data_header_set, set(row_headers))
        self.assertEqual(model._column_data_header_set, set(column_headers))
        
        
    def test_index_entries_without_data1(self):
        """test _index_entries_without_data with tuple_index_entries"""
        model = PivotModel()
        row_headers = set([('a', 'aa', 1),
                           ('a', 'bb', 2),
                           ('e', 'ee', 3)])
        new_keys, new_none_keys, new_entries = model._index_entries_without_data(('test1','test2', 'test3'), row_headers, (), (), self.tuple_index_entries)
        self.assertEqual(new_keys, set())
        self.assertEqual(new_none_keys, set([('a','cc',None),('f','ee', None), (None, None, 6)]))
        self.assertEqual(new_entries, {'test2': set(['cc','ee']),'test1': set(['a','f']), 'test3': set([6])})
    
    def test_index_entries_without_data2(self):
        """test _index_entries_without_data with tuple_index_entries and a frozen index"""
        model = PivotModel()
        row_headers = set([('aa', 1),
                           ('bb', 2)])
        new_keys, new_none_keys, new_entries = model._index_entries_without_data(('test2','test3'), row_headers, ('test1',), ('a',), self.tuple_index_entries)
        self.assertEqual(new_keys, set())
        self.assertEqual(new_none_keys, set([('cc',None), (None, 6)]))
        self.assertEqual(new_entries, {'test2': set(['cc']), 'test3': set([6])})
    
    def test_index_entries_without_data3(self):
        """test _index_entries_without_data with tuple_index_entries and a frozen index wich is not in tuple_index_entries"""
        model = PivotModel()
        row_headers = set([(1,),
                           (2,)])
        new_keys, new_none_keys, new_entries = model._index_entries_without_data(('test3',), row_headers, ('test1',), ('a',), self.tuple_index_entries)
        self.assertEqual(new_keys, set([(6,)]))
        self.assertEqual(new_none_keys, set())
        self.assertEqual(new_entries, {'test3': set([6])})
    
    def test_index_entries_without_data4(self):
        """test _index_entries_without_data with tuple_index_entries with no new keys"""
        model = PivotModel()
        row_headers = set([('a', 'cc'),
                           ('f', 'ee'),
                           ('a', 'aa')])
        new_keys, new_none_keys, new_entries = model._index_entries_without_data(('test1','test2'), row_headers, (), (), self.tuple_index_entries)
        self.assertEqual(new_keys, set())
        self.assertEqual(new_none_keys, set())
        self.assertEqual(new_entries, {'test1': set(), 'test2': set()})
    
    def test_set_pivoted_data1(self):
        """set data"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, tuple_index_entries=self.tuple_index_entries)
        data = [['row0_c0','row0_c1'],
                ['row2_c0','row2_c1']]
        row_mask = [0, 2]
        col_mask = [0, 1]
        new_data = {('a', 'aa', 1): 'row0_c0',
                    ('b', 'cc', 3): 'row2_c0'}
        edit_data = {('a', 'aa', 1): 'value_a_aa_1',
                    ('b', 'cc', 3): 'value_b_cc_3'}
        model.set_pivoted_data(data, row_mask, col_mask)
        self.assertEqual(model._data, {**self.dict_data, **new_data})
        self.assertEqual(model._edit_data, edit_data)
        self.assertEqual(model._deleted_data, {})
        self.assertEqual(model._invalid_data, {})
        
    def test_set_pivoted_data2(self):
        """set data with invalid rows"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, tuple_index_entries=self.tuple_index_entries)
        data = [['row0_c0','row0_c1'],
                ['row8_c0','row8_c1']]
        row_mask = [0, 8]
        col_mask = [0, 1]
        new_data = {('a', 'aa', 1): 'row0_c0'}
        edit_data = {('a', 'aa', 1): 'value_a_aa_1'}
        invalid_data = {(8, 0): 'row8_c0'}
        model.set_pivoted_data(data, row_mask, col_mask)
        self.assertEqual(model._data, {**self.dict_data, **new_data})
        self.assertEqual(model._edit_data, edit_data)
        self.assertEqual(model._deleted_data, {})
        self.assertEqual(model._invalid_data, invalid_data)
    
    def test_set_pivoted_data3(self):
        """set data with pivot"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, rows = ('test1','test2'), columns = ('test3',))
        data = [['row0_c0','row0_c1'],
                ['row2_c0','row2_c1']]
        row_mask = [0, 2]
        col_mask = [0, 1]
        new_data = {('a', 'aa', 1): 'row0_c0',
                    ('a', 'aa', 2): 'row0_c1',
                    ('b', 'cc', 1): 'row2_c0',
                    ('b', 'cc', 2): 'row2_c1'}
        edit_data = {('a', 'aa', 1): 'value_a_aa_1',
                     ('a', 'aa', 2): None,
                     ('b', 'cc', 1): None,
                     ('b', 'cc', 2): None}
        model.set_pivoted_data(data, row_mask, col_mask)
        self.assertEqual(model._data, {**self.dict_data, **new_data})
        self.assertEqual(model._edit_data, edit_data)
        self.assertEqual(model._deleted_data, {})
        self.assertEqual(model._invalid_data, {})
    
    def test_set_pivoted_data4(self):
        """set data with pivot and invalid columns"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, rows = ('test1',), columns = ('test2','test3'), tuple_index_entries = self.tuple_index_entries)
        data = [['row0_c0','row0_c6']]
        row_mask = [0]
        col_mask = [0, 6]
        new_data = {('a', 'aa', 1): 'row0_c0'}
        edit_data = {('a', 'aa', 1): 'value_a_aa_1'}
        invalid_data = {(0, 6): 'row0_c6'}
        model.set_pivoted_data(data, row_mask, col_mask)
        self.assertEqual(model._data, {**self.dict_data, **new_data})
        self.assertEqual(model._edit_data, edit_data)
        self.assertEqual(model._deleted_data, {})
        self.assertEqual(model._invalid_data, invalid_data)
    
    def test_get_pivoted_data1(self):
        """get data with pivot and frozen index and tuple_index_entries"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, tuple_index_entries=self.tuple_index_entries)
        model.set_pivot(['test2'], ['test3'], ['test1'], ('a',))
        data = [['value_a_aa_1', None, None, None, None, None],
                [None, 'value_a_bb_2', None, None, None, None],
                [None, None, None, None, None, None]]
        data_model = [[d for d in inner] for inner in model.get_pivoted_data(range(3),range(6))]
        self.assertEqual(data_model, data)
    
    def test_get_pivoted_data2(self):
        """get data from pivoted model wiht tuple_index_entries"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, tuple_index_entries=self.tuple_index_entries)
        model.set_pivot(['test1','test2'], ['test3'], [], ())
        data = [['value_a_aa_1', None, None, None, None, None],
                [None, 'value_a_bb_2', None, None, None, None],
                [None, None, None, None, None, None],
                [None, None, 'value_b_cc_3', None, None, None],
                [None, None, None, 'value_c_cc_4', None, None],
                [None, None, None, None, 'value_d_dd_5', None],
                [None, None, None, None, 'value_e_ee_5', None],
                [None, None, None, None, None, None]]
        data_model = [[d for d in inner] for inner in model.get_pivoted_data(range(8),range(6))]
        self.assertEqual(data_model, data)

    def test_get_pivoted_data3(self):
        """get data from pivoted model"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        model.set_pivot(['test1','test2'], ['test3'], [], ())
        data = [['value_a_aa_1', None, None, None, None],
                [None, 'value_a_bb_2', None, None, None],
                [None, None, 'value_b_cc_3', None, None],
                [None, None, None, 'value_c_cc_4', None],
                [None, None, None, None, 'value_d_dd_5'],
                [None, None, None, None, 'value_e_ee_5']]
        data_model = [[d for d in inner] for inner in model.get_pivoted_data(range(6),range(5))]
        self.assertEqual(data_model, data)
    
    def test_edit_index1(self):
        """edit existing index to new"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        data = self.dict_data
        data.pop(('a', 'aa', 1))
        delete_data = {('a', 'aa', 1): 'value_a_aa_1'}
        new_data = {('new1', 'new2', 1): 'value_a_aa_1'}
        edit_data = {('new1', 'new2', 1): None}
        model.edit_index([('new1', 'new2', 1)],[0],'row')
        self.assertEqual(model._row_data_header[0],('new1', 'new2', 1))
        self.assertEqual(model._data, {**data, **new_data})
        self.assertEqual(model._edit_data, edit_data)
        self.assertEqual(model._deleted_data, delete_data)
    
    def test_edit_index2(self):
        """edit existing index to new with pivot"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        model.set_pivot(['test1','test2'], ['test3'], [], ())
        data = self.dict_data
        data.pop(('a', 'aa', 1))
        delete_data = {('a', 'aa', 1): 'value_a_aa_1'}
        new_data = {('a', 'aa', 8): 'value_a_aa_1'}
        edit_data = {('a', 'aa', 8): None}
        model.edit_index([(8,)],[0],'column')
        self.assertEqual(model._column_data_header[0],(8,))
        self.assertEqual(model._data, {**data, **new_data})
        self.assertEqual(model._edit_data, edit_data)
        self.assertEqual(model._deleted_data, delete_data)
    
    def test_edit_index3(self):
        """edit existing index to invalid"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        data = self.dict_data
        data.pop(('a', 'bb', 2))
        delete_data = {('a', 'bb', 2): 'value_a_bb_2'}
        new_data = {}
        edit_data = {}
        invalid_row = set([1])
        invalid_data = {(1,0): 'value_a_bb_2'}
        model.edit_index([('new1', 'new2', 'wrong_type')],[1],'row')
        self.assertEqual(model._data, {**data, **new_data})
        self.assertEqual(model._edit_data, edit_data)
        self.assertEqual(model._deleted_data, delete_data)
        self.assertEqual(model._invalid_row, invalid_row)
        self.assertEqual(model._invalid_data, invalid_data)
        self.assertEqual(model._row_data_header[1],('new1', 'new2', 'wrong_type'))
    
    def test_edit_index4(self):
        """test that tuple_index_entries is updated when index change"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, tuple_index_entries = self.tuple_index_entries)
        set1 = set(model.tuple_index_entries[('test1','test2')])
        set2 = set(model.tuple_index_entries[('test3',)])
        set1.add(('new1','new2'))
        set2.add((10,))
        model.edit_index([('new1', 'new2', 10)],[1],'row')
        self.assertEqual(model.tuple_index_entries[('test1','test2')], set1)
        self.assertEqual(model.tuple_index_entries[('test3',)], set2)
    
    def test_edit_index5(self):
        """test that tuple_index_entries is not updated when index change with invalid indexes"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, tuple_index_entries = self.tuple_index_entries)
        set1 = set(model.tuple_index_entries[('test1','test2')])
        set2 = set(model.tuple_index_entries[('test3',)])
        model.edit_index([(1, 2, 'invalid types')],[1],'row')
        self.assertEqual(model.tuple_index_entries[('test1','test2')], set1)
        self.assertEqual(model.tuple_index_entries[('test3',)], set2)
    
    def test_edit_index6(self):
        """test that index_entries is updated when index change"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, tuple_index_entries = self.tuple_index_entries)
        set1 = set(model.index_entries['test1'])
        set2 = set(model.index_entries['test2'])
        set3 = set(model.index_entries['test3'])
        set1.add('new1')
        set2.add('new2')
        set3.add(10)
        model.edit_index([('new1', 'new2', 10)],[1],'row')
        self.assertEqual(model.index_entries['test1'],set1)
        self.assertEqual(model.index_entries['test2'],set2)
        self.assertEqual(model.index_entries['test3'],set3)
    
    def test_edit_index7(self):
        """test that index_entries doesn't add invalid entries when editing index"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, tuple_index_entries = self.tuple_index_entries)
        set1 = set(model.index_entries['test1'])
        set2 = set(model.index_entries['test2'])
        set3 = set(model.index_entries['test3'])
        model.edit_index([(2, 4, 'invalid_types')],[1],'row')
        self.assertEqual(model.index_entries['test1'],set1)
        self.assertEqual(model.index_entries['test2'],set2)
        self.assertEqual(model.index_entries['test3'],set3)
    
    def test_edit_index8(self):
        """test adding new rows"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        row_headers = model._row_data_header.copy()
        model.edit_index([('new1', 'new2', 10), ('new1', 'new2', 11)],[6,7],'row')
        self.assertEqual(model._row_data_header, row_headers + [('new1', 'new2', 10), ('new1', 'new2', 11)])
    
    def test_edit_index9(self):
        """test adding new rows invalid rows"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        row_headers = model._row_data_header.copy()
        model.edit_index([('new1', 'new2', 'wrong_type')],[6],'row')
        self.assertEqual(model._row_data_header, row_headers + [('new1', 'new2', 'wrong_type')])
        self.assertEqual(model._invalid_row, set([6]))
    
    def test_get_unique_index_values1(self):
        """test that _get_unique_index_values returns unique values for specified indexes"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        index_set = set([('a', 'aa'), ('a', 'bb'), ('b', 'cc'),
                         ('c', 'cc'), ('d', 'dd'), ('e', 'ee')])
        index_header_values = model._get_unique_index_values(('test1','test2'), (), ())
        self.assertEqual(index_header_values, index_set)
    
    def test_get_unique_index_values2(self):
        """test that _get_unique_index_values returns unique values for specified indexes with filter index and value"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        index_set = set([('d', 'dd'), ('e', 'ee')])
        index_header_values = model._get_unique_index_values(('test1','test2'), ('test3',), (5,))
        self.assertEqual(index_header_values, index_set)
    
    def test_is_valid_index1(self):
        """test if index of correct type is valid"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        self.assertTrue(model.is_valid_index('test_str', 'test1'))
    
    def test_is_valid_index2(self):
        """test if index of incorrect type is invalid"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        self.assertFalse(model.is_valid_index('should_be_int', 'test3'))

    def test_is_valid_index3(self):
        """test if index of correct value is valid when model has valid_index_values"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, valid_index_values={'test1': set(['correct_value']), 'test3': range(10)})
        self.assertTrue(model.is_valid_index('correct_value', 'test1'))
        self.assertTrue(model.is_valid_index(5, 'test3'))
    
    def test_is_valid_index4(self):
        """test if index of incorrect value is invalid when model has valid_index_values"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, valid_index_values={'test1': set(['correct_value']), 'test3': range(10)})
        self.assertFalse(model.is_valid_index('bad_value', 'test1'))
        self.assertFalse(model.is_valid_index(-52, 'test3'))
    
    def test_is_valid_key1(self):
        """test that a correct key is valid"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        model._add_index_value('valid1','test1')
        model._add_index_value('valid2','test2')
        model._add_index_value(4,'test3')
        self.assertTrue(model.is_valid_key(('valid1', 'valid2', 4),
                                            model._row_data_header_set,
                                            ('test1', 'test2', 'test3')))
    
    def test_is_valid_key2(self):
        """test that a duplicate key is invalid"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        self.assertFalse(model.is_valid_key(('a', 'aa', 1),
                                            model._row_data_header_set,
                                            ('test1', 'test2', 'test3')))
    
    def test_is_valid_key3(self):
        """test that akey with invalid type is invalid"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        self.assertFalse(model.is_valid_key(('a', 'aa', 'invalid_type'),
                                            model._row_data_header_set,
                                            ('test1', 'test2', 'test3')))
    
    def test_delete_pivoted_values(self):
        """test deleting pivoted values"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        data_dict = self.dict_data
        data_dict.pop(('a','aa',1))
        data_dict.pop(('a','bb',2))
        deleted_data = {('a','aa',1): 'value_a_aa_1', ('a','bb',2): 'value_a_bb_2'}
        model.delete_pivoted_values([(0, 0), (1, 0)])
        self.assertEqual(model._data, data_dict)
        self.assertEqual(model._deleted_data, deleted_data)

    def test_delete_index_values1(self):
        """test deleting index values deletes data"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        data_dict = self.dict_data
        deleted_data = {}
        deleted_data[('a','aa',1)] = data_dict.pop(('a','aa',1))
        deleted_data[('a','bb',2)] = data_dict.pop(('a','bb',2))
        model.delete_index_values({'test1': set(['a'])})
        self.assertEqual(model._data, data_dict)
        self.assertEqual(model._deleted_data, deleted_data)
    
    def test_delete_index_values2(self):
        """test deleting index values deletes row headers"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        row_headers = model._row_data_header.copy()
        row_headers.pop(0)
        row_headers.pop(0)
        row_headers_set = set(model._row_data_header_set)
        row_headers_set.discard(('a','aa',1))
        row_headers_set.discard(('a','bb',2))
        model.delete_index_values({'test1': set(['a'])})
        self.assertEqual(model._row_data_header, row_headers)
        self.assertEqual(model._row_data_header_set, row_headers_set)
    
    def test_delete_index_values3(self):
        """test deleting index values deletes column headers"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, rows = ('test1','test2'), columns = ('test3',))
        row_headers = model._column_data_header.copy()
        row_headers.pop(4)
        row_headers_set = set(model._row_data_header_set)
        row_headers_set.discard((5,))
        model.delete_index_values({'test3': set([5])})
        self.assertEqual(model._column_data_header, row_headers)
        self.assertEqual(model._row_data_header_set, row_headers_set)
    
    def test_delete_index_values4(self):
        """test deleting index values deletes them from index_entries"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        model.delete_index_values({'test1': set(['a'])})
        self.assertEqual(model.index_entries['test1'], set(['b','c','d','e']))
        self.assertEqual(model._deleted_index_entries['test1'], set(['a']))
    
    def test_delete_index_values5(self):
        """test deleting index values also deletes tuple index entries"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, tuple_index_entries=self.tuple_index_entries)
        expected_tuple_values = set([('b', 'cc'), ('c', 'cc'), ('d', 'dd'), ('e', 'ee'), ('f', 'ee')])
        deleted_tuple_values = set([('a','aa'), ('a', 'bb'), ('a', 'cc')])
        model.delete_index_values({'test1': set(['a'])})
        self.assertEqual(model.tuple_index_entries[('test1', 'test2')], expected_tuple_values)
        self.assertEqual(model._deleted_tuple_index_entries[('test1', 'test2')], deleted_tuple_values)
    
    def test_delete_index_values6(self):
        """test deleting index values deletes them from _added_index_entries"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        model._added_index_entries['test1'] = set(['a','b','c'])
        model.delete_index_values({'test1': set(['a'])})
        self.assertEqual(model._added_index_entries['test1'], set(['b','c']))
    
    def test_delete_tuple_index_values1(self):
        """test that delete_tuple_index_values deletes data"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, tuple_index_entries=self.tuple_index_entries)
        data_dict = self.dict_data
        deleted_data = {}
        deleted_data[('a','aa',1)] = data_dict.pop(('a','aa',1))
        model.delete_tuple_index_values({('test1', 'test2'): set([('a','aa')])})
        self.assertEqual(model._data, data_dict)
        self.assertEqual(model._deleted_data, deleted_data)
    
    def test_delete_tuple_index_values2(self):
        """test deleting index values deletes row headers"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, tuple_index_entries=self.tuple_index_entries)
        row_headers = model._row_data_header.copy()
        row_headers.pop(0)
        row_headers_set = set(model._row_data_header_set)
        row_headers_set.discard(('a','aa',1))
        model.delete_tuple_index_values({('test1', 'test2'): set([('a','aa')])})
        self.assertEqual(model._row_data_header, row_headers)
        self.assertEqual(model._row_data_header_set, row_headers_set)
    
    def test_delete_tuple_index_values3(self):
        """test deleting index values deletes column headers"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, rows=(), columns=tuple(self.index_names), tuple_index_entries=self.tuple_index_entries)
        column_headers = model._column_data_header.copy()
        column_headers.pop(0)
        column_headers_set = set(model._column_data_header_set)
        column_headers_set.discard(('a','aa',1))
        model.delete_tuple_index_values({('test1', 'test2'): set([('a','aa')])})
        self.assertEqual(model._column_data_header, column_headers)
        self.assertEqual(model._column_data_header_set, column_headers_set)
    
    def test_delete_tuple_index_values4(self):
        """test deleting tuple index values where tuple exists over both row and column don't delete row or column values"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, rows=('test1','test3'), columns=('test2',), tuple_index_entries=self.tuple_index_entries)
        column_headers = model._column_data_header.copy()
        row_headers = model._row_data_header.copy()
        model.delete_tuple_index_values({('test1', 'test2'): set([('a','aa')])})
        self.assertEqual(model._column_data_header, column_headers)
        self.assertEqual(model._row_data_header, row_headers)
    
    def test_delete_tuple_index_values5(self):
        """test deleting tuple index values also deletes tuple index entries"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, tuple_index_entries=self.tuple_index_entries)
        expected_tuple_values = set([('a', 'bb'), ('a', 'cc'),('b', 'cc'), ('c', 'cc'), ('d', 'dd'), ('e', 'ee'), ('f', 'ee')])
        deleted_tuple_values = set([('a','aa')])
        model.delete_tuple_index_values({('test1', 'test2'): set([('a','aa')])})
        self.assertEqual(model.tuple_index_entries[('test1', 'test2')], expected_tuple_values)
        self.assertEqual(model._deleted_tuple_index_entries[('test1', 'test2')], deleted_tuple_values)
    
    def test_delete_tuple_index_values6(self):
        """test deleting tuple index values also deletes added tuple index entries"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, tuple_index_entries=self.tuple_index_entries)
        model._added_tuple_index_entries[('test1', 'test2')] = set([('a', 'aa'), ('a', 'cc')])
        model.delete_tuple_index_values({('test1', 'test2'): set([('a','aa')])})
        self.assertEqual(model._added_tuple_index_entries[('test1', 'test2')], set([('a', 'cc')]))
    
    def test_paste_values1(self):
        """test pasting data into data only"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        model.set_pivot(['test1','test2'], ['test3'], [], ())
        data = [['paste1', 'paste2', None, None, None],
                ['paste3', 'paste4', None, None, None],
                [None, None, 'value_b_cc_3', None, None],
                [None, None, None, 'value_c_cc_4', None],
                [None, None, None, None, 'value_d_dd_5'],
                [None, None, None, None, 'value_e_ee_5']]
        model.paste_data(data=[['paste1', 'paste2'],['paste3', 'paste4']], row_mask=[0, 1], col_mask=[0, 1])
        data_model = [[d for d in inner] for inner in model.get_pivoted_data(range(6),range(5))]
        self.assertEqual(data_model, data)
        
    def test_paste_values2(self):
        """test pasting data into row headers only"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        paste_data = [['aa_new', 9],['bb_new', 10]]
        row_header_data = model._row_data_header.copy()
        row_header_data[0] = ('a','aa_new', 9)
        row_header_data[1] = ('a','bb_new', 10)
        model.paste_data(row_start=1, row_header_data=paste_data, row_mask=[0,1])
        self.assertEqual(model._row_data_header, row_header_data)
    
    def test_paste_values3(self):
        """test pasting data into row headers only with new row"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        paste_data = [['aa_new', 9],['bb_new', 10]]
        row_header_data = model._row_data_header.copy()
        row_header_data[0] = ('a','aa_new', 9)
        row_header_data.append((None,'bb_new', 10))
        model.paste_data(row_start=1, row_header_data=paste_data, row_mask=[0,6])
        self.assertEqual(model._row_data_header, row_header_data)
    
    def test_paste_values4(self):
        """test pasting data into columns headers only"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, rows=(), columns=tuple(self.index_names))
        paste_data = [['aa_new', 'bb_new'],[9, 10]]
        col_header_data = model._column_data_header.copy()
        col_header_data[0] = ('a','aa_new', 9)
        col_header_data[1] = ('a','bb_new', 10)
        model.paste_data(col_start=1, col_header_data=paste_data, col_mask=[0,1])
        self.assertEqual(model._column_data_header, col_header_data)
    
    def test_paste_values5(self):
        """test pasting data into columns headers only with new column"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, rows=(), columns=tuple(self.index_names))
        paste_data = [['aa_new', 'bb_new'],[9, 10]]
        col_header_data = model._column_data_header.copy()
        col_header_data[0] = ('a','aa_new', 9)
        col_header_data.append((None,'bb_new', 10))
        model.paste_data(col_start=1, col_header_data=paste_data, col_mask=[0,6])
        self.assertEqual(model._column_data_header, col_header_data)
    
    def test_delete_then_add_value(self):
        """test that deleting a value and then adding it back tracks in _deleted_data and _edited_data"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, rows=(), columns=tuple(self.index_names))
        model.set_pivoted_data([['']],[0],[0])
        model.set_pivoted_data([['edited_val']],[0],[0])
        self.assertEqual(model._deleted_data, {})
        self.assertEqual(model._edit_data, {('a','aa',1): 'value_a_aa_1'})
    
    def test_add_new_value_then_delete(self):
        """test that adding a value and then deleteing it tracks in _deleted_data and _edited_data"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, rows=('test1','test3'), columns=('test2',))
        model.set_pivoted_data([['new_data']],[0],[1])
        model.set_pivoted_data([['']],[0],[1])
        self.assertEqual(model._deleted_data, {})
        self.assertEqual(model._edit_data, {})
    
    def test_edit_value_edit_back(self):
        """test that edit a value and editing it to original value to make sure it's not in _edit_value"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        model.set_pivoted_data([['new_data']],[0],[0])
        model.set_pivoted_data([['value_a_aa_1']],[0],[0])
        self.assertEqual(model._deleted_data, {})
        self.assertEqual(model._edit_data, {})
    
    def test_restore_edited_value(self):
        """test that restoring an edited data works"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        model._add_data(('a','aa',1), 'edit')
        model._restore_data(('a','aa',1))
        self.assertEqual(model._deleted_data, {})
        self.assertEqual(model._edit_data, {})
        self.assertEqual(model._data[('a','aa',1)], 'value_a_aa_1')
    
    def test_restore_deleted_value(self):
        """test that restoring a deleted value works"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        model._delete_data(('a','aa',1))
        model._restore_data(('a','aa',1))
        self.assertEqual(model._deleted_data, {})
        self.assertEqual(model._edit_data, {})
        self.assertEqual(model._data[('a','aa',1)], 'value_a_aa_1')
    
    def test_restore_added_value(self):
        """test that restoring a added data works"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        model._add_data(('new_key','aa',1),'new value')
        model._restore_data(('new_key','aa',1))
        self.assertEqual(model._deleted_data, {})
        self.assertEqual(model._edit_data, {})
        self.assertFalse(('new_key','aa',1) in model._data)
        
    def test_add_index_value1(self):
        """test that adding a new index value works"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, used_index_values = {('test1',): set()})
        result = model._add_index_value('new_index', 'test1')
        self.assertTrue(result)
        self.assertEqual(model._added_index_entries['test1'], set(['new_index']))
        self.assertEqual(model._used_index_values[('test1',)], set(['new_index']))
    
    def test_add_index_value2(self):
        """test that adding an existing doesn't do anything"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types)
        result = model._add_index_value('a', 'test1')
        self.assertTrue(result)
        self.assertEqual(model._added_index_entries['test1'], set())
    
    def test_add_index_value3(self):
        """test that adding a new index with name already taken doesn't work"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, used_index_values = {('test1',): set(['used_value'])})
        result = model._add_index_value('used_value', 'test1')
        self.assertFalse(result)
        self.assertEqual(model._added_index_entries['test1'], set())
    
    def test_add_index_value4(self):
        """test that adding a new index with name already taken doesn't work for multiple shared values"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, used_index_values = {('test1', 'test2'): set()})
        result1 = model._add_index_value('used_value', 'test1')
        result2 = model._add_index_value('used_value', 'test2')
        self.assertTrue(result1)
        self.assertFalse(result2)
        self.assertEqual(model._added_index_entries['test1'], set(['used_value']))
        self.assertEqual(model._added_index_entries['test2'], set())
    
    def test_add_index_value5(self):
        """test that adding a to two different indexes with same real name"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, index_real_names = ['real','real','test3'])
        result1 = model._add_index_value('new_val1', 'test1')
        result2 = model._add_index_value('new_val2', 'test2')
        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertEqual(model._added_index_entries['real'], set(['new_val1','new_val2']))
    
    def test_delete_index_then_add(self):
        """test that deleting an index and then readding it removes it from _deleted_index_entries and doesn't add to _added_index_entries"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, used_index_values = {('test1', 'test2'): set()})
        model.delete_index_values({'test1': set(['a'])})
        self.assertEqual(model._deleted_index_entries['test1'], set(['a']))
        self.assertEqual(model._added_index_entries['test1'], set())
        result1 = model._add_index_value('a', 'test1')
        self.assertTrue(result1)
        self.assertEqual(model._added_index_entries['test1'], set())
        self.assertEqual(model._deleted_index_entries['test1'], set())
        
    def test_delete_tuple_index_values_with_frozen_pivot1(self):
        """test that delete_tuple_index_values deletes data when pivot has frozen dimension"""
        model = PivotModel()
        tuple_entries = {('test1','test2'):set()}
        model.set_new_data(self.data, self.index_names, self.index_types, tuple_index_entries=tuple_entries)
        model.set_pivot(['test1','test3'], [], ['test2'], ('aa',))
        model.delete_tuple_index_values({('test1', 'test2'): set([('a','aa')])})
        self.assertEqual(model._row_data_header, [])
    
    def test_delete_tuple_index_values_with_frozen_pivot2(self):
        """test that delete_tuple_index_values doesn't delete data when pivot has frozen dimension when frozen value doesn't match delete value"""
        model = PivotModel()
        tuple_entries = {('test1','test2'):set()}
        model.set_new_data(self.data, self.index_names, self.index_types, tuple_index_entries=tuple_entries)
        model.set_pivot(['test1','test3'], [], ['test2'], ('aa',))
        model.delete_tuple_index_values({('test1', 'test2'): set([('a','bb')])})
        self.assertEqual(model._row_data_header, [('a',1),('a',None)])
    
    def test_delete_tuple_index_values_with_frozen_pivot3(self):
        """test that delete_tuple_index_values deletes data when pivot has frozen dimension, column"""
        model = PivotModel()
        tuple_entries = {('test1','test2'):set()}
        model.set_new_data(self.data, self.index_names, self.index_types, tuple_index_entries=tuple_entries)
        model.set_pivot([], ['test1','test3'], ['test2'], ('aa',))
        model.delete_tuple_index_values({('test1', 'test2'): set([('a','aa')])})
        self.assertEqual(model._column_data_header, [])
    
    def test_delete_tuple_index_values_with_frozen_pivot4(self):
        """test that delete_tuple_index_values doesn't delete data when pivot has frozen dimension when frozen value doesn't match delete value, column"""
        model = PivotModel()
        tuple_entries = {('test1','test2'):set()}
        model.set_new_data(self.data, self.index_names, self.index_types, tuple_index_entries=tuple_entries)
        model.set_pivot([], ['test1','test3'], ['test2'], ('aa',))
        model.delete_tuple_index_values({('test1', 'test2'): set([('a','bb')])})
        self.assertEqual(model._column_data_header, [('a',1),('a',None)])
    
    def test_delete_entries_with_wrong_index(self):
        """Test that deleting an entrie with wrong index doesn't delete from used_index_values"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, used_index_values = {('test1', 'test2'): set(['wrong_index'])})
        model._add_index_value('wrong_index','test1')
        model.delete_index_values({'test2': set(['wrong_index'])})
        self.assertEqual(model._used_index_values, {('test1', 'test2'): set(['wrong_index'])})
    
    def test_add_indexes_with_same_name(self):
        """Test that adding indexes with same name only creates one entry in index_entries"""
        model = PivotModel()
        model.set_new_data(self.data, self.index_names, self.index_types, index_real_names = ['test','test','test3'])
        self.assertEqual(model.index_entries['test'], set(['a','b','c','d','e','aa','bb','cc','dd','ee']))
        self.assertEqual(sorted(list(model.index_entries.keys())), ['test','test3'])
    
    def test_delete_index_values_with_same_name(self):
        """Test that deleteing indexes with same name deletes all rows"""
        model = PivotModel()
        data = [['a', 'b', 'c', 1], ['d', 'a', 'c', 1] , ['c','d','e', 1]]
        model.set_new_data(data, self.index_names, self.index_types, index_real_names = ['test','test','test3'])
        model.delete_index_values({'test': set(['a'])})
        self.assertEqual(model._row_data_header, [('c','d','e')])
        self.assertEqual(model._row_data_header_set, set([('c','d','e')]))
    
    def test_delete_index_values_with_same_name2(self):
        """Test that deleteing indexes with same name deletes all data"""
        model = PivotModel()
        data = [['a', 'b', 'c', 1], ['d', 'a', 'c', 1] , ['c','d','e', 1]]
        model.set_new_data(data, self.index_names, self.index_types, index_real_names = ['test','test','test3'])
        model.delete_index_values({'test': set(['a'])})
        self.assertEqual(model._data, {('c','d','e'): 1})
    
    def test_delete_index_values_with_same_name3(self):
        """Test that deleteing indexes with same name deletes all tuple_index_entries"""
        model = PivotModel()
        data = [['a', 'b', 'c', 1], ['d', 'a', 'c', 1] , ['c','d','e', 1]]
        model.set_new_data(data, self.index_names, self.index_types, index_real_names = ['test','test','test3'], tuple_index_entries={('test1','test2','test3'): set()})
        model.delete_index_values({'test': set(['a'])})
        self.assertEqual(model.tuple_index_entries[('test1','test2','test3')], set([('c','d','e')]))
    
    def test_delete_index_values_with_same_name4(self):
        """Test that deleteing indexes with same name deletes all in _used_index_entries"""
        model = PivotModel()
        data = [['a', 'b', 'c', 1], ['d', 'a', 'c', 1] , ['c','d','e', 1]]
        model.set_new_data(data, self.index_names, self.index_types, index_real_names = ['test','test','test3'], used_index_values={('test',): set(['a','b','c','d'])})
        model.delete_index_values({'test': set(['a'])})
        self.assertEqual(model._used_index_values[('test',)], set(['b','c','d']))


if __name__ == '__main__':
    unittest.main()
    


