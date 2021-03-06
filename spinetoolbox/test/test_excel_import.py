# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 13:40:52 2018

@author: pvper
"""

import os
import uuid
import unittest
from unittest import mock
from unittest.mock import MagicMock
from collections import namedtuple
from sqlalchemy.orm import Session

from spinedatabase_api import DatabaseMapping, DiffDatabaseMapping, create_new_spine_database
from excel_import_export import stack_list_of_tuples, unstack_list_of_tuples, validate_sheet, SheetData, read_parameter_sheet, read_json_sheet, merge_spine_xlsx_data, read_spine_xlsx, export_spine_database_to_xlsx, get_unstacked_objects, import_xlsx_to_db


class TestExcelIntegration(unittest.TestCase):

    def setUp(self):
        """Overridden method. Runs before each test.
        """
        # temp file for excel export
        self.temp_excel_filename = str(uuid.uuid4()) + '.xlsx'

        # create a in memory database with objects, relationship, parameters and values
        input_db = create_new_spine_database('sqlite://')
        db_map = DiffDatabaseMapping(
            "", username='IntegrationTest', create_all=False)
        db_map.engine = input_db
        db_map.engine.connect()
        db_map.session = Session(db_map.engine, autoflush=False)
        db_map.create_mapping()
        db_map.create_diff_tables_and_mapping()
        db_map.init_next_id()

        # create empty database for loading excel into
        input_db_test = create_new_spine_database('sqlite://')
        db_map_test = DiffDatabaseMapping(
            "", username='IntegrationTest', create_all=False)
        db_map_test.engine = input_db_test
        db_map_test.engine.connect()
        db_map_test.session = Session(db_map_test.engine, autoflush=False)
        db_map_test.create_mapping()
        db_map_test.create_diff_tables_and_mapping()
        db_map_test.init_next_id()

        # delete all object_classes to empty database
        oc = set(oc. id for oc in db_map_test.object_class_list().all())
        if oc:
            db_map_test.remove_items(object_class_ids=oc)
        db_map_test.commit_session('empty database')

        oc = set(oc. id for oc in db_map.object_class_list().all())
        if oc:
            db_map.remove_items(object_class_ids=oc)
        db_map.commit_session('empty database')

        # create object classes
        oc_1 = db_map.add_object_class(**{'name': 'object_class_1'})
        oc_2 = db_map.add_object_class(**{'name': 'object_class_2'})

        # create relationship classes
        relc1 = db_map.add_wide_relationship_class(
            **{'name': 'relationship_class', 'object_class_id_list': [oc_1.id, oc_2.id]})

        # create objects
        oc1_obj1 = db_map.add_object(
            **{'name': 'oc1_obj1', 'class_id': oc_1.id})
        oc1_obj2 = db_map.add_object(
            **{'name': 'oc1_obj2', 'class_id': oc_1.id})
        oc2_obj1 = db_map.add_object(
            **{'name': 'oc2_obj1', 'class_id': oc_2.id})
        oc2_obj2 = db_map.add_object(
            **{'name': 'oc2_obj2', 'class_id': oc_2.id})

        # add relationships
        rel1 = db_map.add_wide_relationship(
            **{'name': 'rel1', 'class_id': relc1.id, 'object_id_list': [oc1_obj1.id, oc2_obj1.id]})
        rel2 = db_map.add_wide_relationship(
            **{'name': 'rel2', 'class_id': relc1.id, 'object_id_list': [oc1_obj2.id, oc2_obj2.id]})

        # create parameters
        p1 = db_map.add_parameter(
            **{'name': 'parameter1', 'object_class_id': oc_1.id})
        p2 = db_map.add_parameter(
            **{'name': 'parameter2', 'object_class_id': oc_1.id})
        p3 = db_map.add_parameter(
            **{'name': 'parameter3', 'object_class_id': oc_2.id})
        p4 = db_map.add_parameter(
            **{'name': 'parameter4', 'object_class_id': oc_2.id})
        rel_p1 = db_map.add_parameter(
            **{'name': 'rel_parameter1', 'relationship_class_id': relc1.id})
        rel_p2 = db_map.add_parameter(
            **{'name': 'rel_parameter2', 'relationship_class_id': relc1.id})
        rel_p3 = db_map.add_parameter(
            **{'name': 'rel_parameter3', 'relationship_class_id': relc1.id})
        rel_p4 = db_map.add_parameter(
            **{'name': 'rel_parameter4', 'relationship_class_id': relc1.id})

        # add parameter values
        db_map.add_parameter_value(
            **{'parameter_id': p1.id, 'object_id': oc1_obj1.id, 'value': 0})
        db_map.add_parameter_value(
            **{'parameter_id': p2.id, 'object_id': oc1_obj2.id, 'value': 3.5})
        db_map.add_parameter_value(
            **{'parameter_id': p3.id, 'object_id': oc2_obj1.id, 'json': '[1, 2, 3, 4]'})
        db_map.add_parameter_value(
            **{'parameter_id': p4.id, 'object_id': oc2_obj2.id, 'json': '[5, 6, 7]'})
        db_map.add_parameter_value(
            **{'parameter_id': rel_p1.id, 'relationship_id': rel1.id, 'value': 0})
        db_map.add_parameter_value(
            **{'parameter_id': rel_p2.id, 'relationship_id': rel2.id, 'value': 4})
        db_map.add_parameter_value(
            **{'parameter_id': rel_p3.id, 'relationship_id': rel1.id, 'json': '[5, 6, 7]'})
        db_map.add_parameter_value(
            **{'parameter_id': rel_p4.id, 'relationship_id': rel2.id, 'json': '[1, 2, 3, 4]'})

        # commit
        db_map.commit_session('test')

        self.db_map = db_map
        self.empty_db_map = db_map_test

    def tearDown(self):
        """Overridden method. Runs after each test.
        Use this to free resources after a test if needed.
        """
        # delete temp excel file if it exists
        try:
            os.remove(self.temp_excel_filename)
        except OSError:
            pass

    def compare_dbs(self, db1, db2):
        # compare imported database with exported database
        # don't check ids since they might be different
        # object classes
        oc = db1.object_class_list().all()
        oc = {c.id: c.name for c in oc}
        oc_org = db2.object_class_list().all()
        oc_org = {c.id: c.name for c in oc_org}
        self.assertEqual(set(oc.values()), set(oc_org.values()),
                         msg='Difference in objects classes')
        # objects
        ol = db1.object_list().all()
        ol_id = {o.id: o.name for o in ol}
        ol = {o.name: oc[o.class_id] for o in ol}
        ol_org = db2.object_list().all()
        ol_id_org = {o.id: o.name for o in ol_org}
        ol_org = {o.name: oc_org[o.class_id] for o in ol_org}
        self.assertEqual(ol, ol_org, msg='Difference in objects')
        # relationship classes
        rc = db1.relationship_class_list().all()
        rc = {c.id: (c.name, tuple(oc[o.object_class_id]
                                   for o in rc if o.name == c.name)) for c in rc}
        rc_org = db2.relationship_class_list().all()
        rc_org = {c.id: (c.name, tuple(
            oc_org[o.object_class_id] for o in rc_org if o.name == c.name)) for c in rc_org}
        self.assertEqual(set(rc.values()), set(rc_org.values()),
                         msg='Difference in relationship classes')
        # relationships
        rel = db1.relationship_list().all()
        rel = {c.id: (rc[c.class_id][0], tuple(ol_id[o.object_id]
                                               for o in rel if o.id == c.id)) for c in rel}
        rel_org = db2.relationship_list().all()
        rel_org = {c.id: (rc_org[c.class_id][0], tuple(
            ol_id_org[o.object_id] for o in rel_org if o.id == c.id)) for c in rel_org}
        self.assertEqual(set(rc.values()), set(rc_org.values()),
                         msg='Difference in relationships')
        # parameters
        par = db1.parameter_list().all()
        par = {p.id: (p.name, oc[p.object_class_id]
                      if p.object_class_id else rc[p.relationship_class_id][0]) for p in par}
        par_org = db2.parameter_list().all()
        par_org = {p.id: (p.name, oc_org[p.object_class_id]
                          if p.object_class_id else rc_org[p.relationship_class_id][0]) for p in par_org}
        self.assertEqual(set(par.values()), set(
            par_org.values()), msg='Difference in parameters')
        # parameters values
        parv = db1.parameter_value_list().all()
        parv = set((par[p.parameter_id][0], p.value, p.json, ol_id[p.object_id] if p.object_id else None,
                    rel[p.relationship_id][1] if p.relationship_id else None) for p in parv)
        parv_org = db2.parameter_value_list().all()
        parv_org = set((par_org[p.parameter_id][0], p.value, p.json, ol_id_org[p.object_id] if p.object_id else None,
                        rel_org[p.relationship_id][1] if p.relationship_id else None) for p in parv_org)
        self.assertEqual(set(par.values()), set(
            par_org.values()), msg='Difference in parameter values')

    def test_export_import(self):
        """Integration test exporting an excel and then importing it to a new database."""
        # export to excel
        export_spine_database_to_xlsx(self.db_map, self.temp_excel_filename)

        # import into empty database
        import_xlsx_to_db(self.empty_db_map, self.temp_excel_filename)
        self.empty_db_map.commit_session('Excel import')

        # compare dbs
        self.compare_dbs(self.empty_db_map, self.db_map)

    def test_import_to_existing_data(self):
        """Integration test importing data to a database with existing items"""
        # export to excel
        export_spine_database_to_xlsx(self.db_map, self.temp_excel_filename)

        # import into empty database
        import_xlsx_to_db(self.empty_db_map, self.temp_excel_filename)
        self.empty_db_map.commit_session('Excel import')

        # delete 1 object class
        self.db_map.remove_items(object_class_ids=set([1]))
        self.db_map.commit_session("Delete class")

        # reimport data
        import_xlsx_to_db(self.db_map, self.temp_excel_filename)
        self.db_map.commit_session("reimport data")

        # compare dbs
        self.compare_dbs(self.empty_db_map, self.db_map)


class TestExcelImport(unittest.TestCase):

    def setUp(self):
        """Overridden method. Runs before each test.
        """
        # mock data for relationship sheets
        ws_mock = {}
        ws_mock['A2'] = MagicMock(value='relationship')
        ws_mock['B2'] = MagicMock(value='parameter')
        ws_mock['C2'] = MagicMock(value='relationship_name')
        ws_mock['D2'] = MagicMock(value=2)
        ws_mock['A4:B4'] = [
            [MagicMock(value='object_class_name1'), MagicMock(value='object_class_name2')]]
        ws_mock[4] = [MagicMock(value='object_class_name1'), MagicMock(value='object_class_name2'),
                      MagicMock(value='parameter1'), MagicMock(value='parameter2')]
        ws_mock['A'] = [1, 2, 3, 4, 5, 6]
        ws = MagicMock()
        ws.__getitem__.side_effect = ws_mock.__getitem__
        ws.title = 'title'
        self.ws_rel = ws
        self.data_parameter = ['parameter1', 'parameter2']
        self.data_class_rel = [['object_class_name1', 'object_class_name2']]
        self.data_rel = [['a_obj1', 'b_obj1', 1, 'a'],
                         ['a_obj2', 'b_obj2', 2, 'b']]
        self.class_obj_rel = [['a_obj1', 'b_obj1'], ['a_obj2', 'b_obj2']]
        self.RelData = namedtuple(
            'Data', ['parameter_type', 'object0', 'object1', 'parameter', 'value'])

        # mock data for object sheets
        ws_mock = {}
        ws_mock['A2'] = MagicMock(value='object')
        ws_mock['B2'] = MagicMock(value='parameter')
        ws_mock['C2'] = MagicMock(value='object_class_name')
        ws_mock[4] = [MagicMock(value='object_class_name'), MagicMock(
            value='parameter1'), MagicMock(value='parameter2')]
        ws_mock['A'] = [1, 2, 3, 4, 5, 6]
        ws = MagicMock()
        ws.__getitem__.side_effect = ws_mock.__getitem__
        ws.title = 'title'
        self.ws_obj = ws
        self.data_parameter = ['parameter1', 'parameter2']
        self.data_class_obj = [['object_class_name']]
        self.data_obj = [['obj1', 1, 'a'],
                         ['obj2', 2, 'b']]
        self.class_obj_obj = ['obj1', 'obj2']
        self.ObjData = namedtuple(
            'Data', ['parameter_type', 'object0', 'parameter', 'value'])

        # mock data for json sheet object

        ws_mock = {}
        ws_mock['A2'] = MagicMock(value='object')
        ws_mock['B2'] = MagicMock(value='json array')
        ws_mock['C2'] = MagicMock(value='object_class_name')
        ws_mock['A4'] = MagicMock(value='object_class_name')
        ws_mock[4] = [MagicMock(value='object_class_name'), MagicMock(
            value='obj1'), MagicMock(value='obj2')]
        ws_mock['B'] = [MagicMock(value=None), MagicMock(value=None), MagicMock(value=None), MagicMock(
            value='obj1'), MagicMock(value='parameter1'), MagicMock(value=1), MagicMock(value=2), MagicMock(value=3)]
        ws_mock['C'] = [MagicMock(value=None), MagicMock(value=None), MagicMock(value=None), MagicMock(
            value='obj2'), MagicMock(value='parameter2'), MagicMock(value=4), MagicMock(value=5), MagicMock(value=6)]
        ws = MagicMock()
        ws.__getitem__.side_effect = ws_mock.__getitem__
        ws.title = 'title'
        self.ws_obj_json = ws

        # mock data for json sheets relationship
        ws_mock = {}
        ws_mock['A2'] = MagicMock(value='relationship')
        ws_mock['B2'] = MagicMock(value='json array')
        ws_mock['C2'] = MagicMock(value='relationship_name')
        ws_mock['D2'] = MagicMock(value=2)
        ws_mock['A4'] = MagicMock(value='object_class_name1')
        ws_mock['A5'] = MagicMock(value='object_class_name2')
        ws_mock['A4:A5'] = [[MagicMock(value='object_class_name1')], [
            MagicMock(value='object_class_name2')]]
        ws_mock[4] = [MagicMock(value='object_class_name1'), MagicMock(
            value='a_obj1'), MagicMock(value='a_obj2')]
        ws_mock['B'] = [MagicMock(value=None), MagicMock(value=None), MagicMock(value=None), MagicMock(value='a_obj1'), MagicMock(
            value='b_obj1'), MagicMock(value='parameter1'), MagicMock(value=1), MagicMock(value=2), MagicMock(value=3)]
        ws_mock['C'] = [MagicMock(value=None), MagicMock(value=None), MagicMock(value=None), MagicMock(value='a_obj2'), MagicMock(
            value='b_obj2'), MagicMock(value='parameter2'), MagicMock(value=4), MagicMock(value=5), MagicMock(value=6)]

        ws = MagicMock()
        ws.__getitem__.side_effect = ws_mock.__getitem__
        ws.title = 'title'
        self.ws_rel_json = ws

    def tearDown(self):
        """Overridden method. Runs after each test.
        Use this to free resources after a test if needed.
        """

    def assertEqualSheetData(self, d1, d2):
        self.assertEqual(d1.sheet_name, d2.sheet_name)
        self.assertEqual(d1.class_name, d2.class_name)
        self.assertEqual(d1.object_classes, d2.object_classes)
        self.assertEqual(set(d1.parameters), set(d2.parameters))
        self.assertEqual(set(d1.parameter_values), set(d2.parameter_values))
        if d1.class_type == 'relationship':
            self.assertEqual(set(tuple(r) for r in d1.objects),
                             set(tuple(r) for r in d2.objects))
        else:
            self.assertEqual(set(d1.objects), set(d2.objects))
        self.assertEqual(d1.class_type, d2.class_type)

    @mock.patch('excel_import_export.load_workbook')
    @mock.patch('excel_import_export.read_parameter_sheet')
    @mock.patch('excel_import_export.read_json_sheet')
    def test_read_spine_xlsx(self, mock_read_json_sheet, mock_read_parameter_sheet, mock_load_workbook):
        # workbook mock
        wb_dict = {'object': self.ws_obj,
                   'object_json': self.ws_obj_json,
                   'relationship': self.ws_rel,
                   'relationship_json': self.ws_rel_json}
        wb_mock = MagicMock()
        wb_mock.__getitem__.side_effect = wb_dict.__getitem__
        wb_mock.sheetnames = ['object', 'object_json',
                              'relationship', 'relationship_json']
        mock_load_workbook.side_effect = [wb_mock]

        # data for object parameter sheet
        parameter_values = [self.ObjData('value', 'obj1', 'parameter1', 1),
                            self.ObjData('value', 'obj1', 'parameter2', 'a'),
                            self.ObjData('value', 'obj2', 'parameter1', 2),
                            self.ObjData('value', 'obj2', 'parameter2', 'b')]
        data_obj = SheetData('object', 'object_class_name',
                             self.data_class_obj[0], self.data_parameter,
                             parameter_values, self.class_obj_obj, 'object')
        # data for object json sheet
        parameter_values = [self.ObjData('json', 'obj1', 'parameter1', '[1, 2, 3]'),
                            self.ObjData('json', 'obj2', 'parameter2', '[4, 5, 6]')]
        data_obj_json = SheetData('object_json', 'object_class_name',
                                  self.data_class_obj[0], list(
                                      set(self.data_parameter)),
                                  parameter_values, [], 'object')
        # data for relationship parameter sheet
        parameter_values = [self.RelData('value', 'a_obj1', 'b_obj1', 'parameter1', 1),
                            self.RelData('value', 'a_obj1',
                                         'b_obj1', 'parameter2', 'a'),
                            self.RelData('value', 'a_obj2',
                                         'b_obj2', 'parameter1', 2),
                            self.RelData('value', 'a_obj2', 'b_obj2', 'parameter2', 'b')]
        data_rel = SheetData('relationship', 'relationship_name',
                             self.data_class_rel[0], self.data_parameter,
                             parameter_values, self.class_obj_rel, 'relationship')
        # data for relationship json sheet
        parameter_values = [self.RelData('json', 'a_obj1', 'b_obj1', 'parameter1', '[1, 2, 3]'),
                            self.RelData('json', 'a_obj2', 'b_obj2', 'parameter2', '[4, 5, 6]')]
        data_rel_json = SheetData('relationship_json', 'relationship_name',
                                  self.data_class_rel[0], list(
                                      set(self.data_parameter)),
                                  parameter_values, [], 'relationship')

        mock_read_json_sheet.side_effect = [data_obj_json, data_rel_json]
        mock_read_parameter_sheet.side_effect = [data_obj, data_rel]

        obj_data, rel_data, error_log = read_spine_xlsx('filepath_mocked_away')

        # only test that lenght is correct since all other functions is tested elsewhere
        self.assertTrue(len(error_log) == 0)
        self.assertTrue(len(obj_data) == 1)
        self.assertTrue(len(rel_data) == 1)

    def test_merge_spine_xlsx_data(self):
        """Test merging array of SheetData"""
        parameter_values1 = [self.RelData('value', 'a_obj1', 'b_obj1', 'parameter1', 1),
                             self.RelData('value', 'a_obj2', 'b_obj2', 'parameter2', 2)]
        parameter_values2 = [self.RelData('value', 'a_obj1', 'b_obj1', 'parameter1', 1),
                             self.RelData('value', 'a_obj3', 'b_obj3', 'parameter3', 3)]
        data1 = SheetData('title', 'relationship_name',
                          self.data_class_rel[0], ['parameter1', 'parameter2'],
                          parameter_values1, [['a_obj1', 'b_obj1'], ['a_obj2', 'b_obj2']], 'relationship')
        data2 = SheetData('title', 'relationship_name',
                          self.data_class_rel[0], ['parameter1', 'parameter3'],
                          parameter_values2, [['a_obj1', 'b_obj1'], ['a_obj3', 'b_obj3']], 'relationship')

        parameter_values3 = parameter_values1 + parameter_values2
        valid_data = SheetData('title', 'relationship_name',
                               self.data_class_rel[0], [
                                   'parameter1', 'parameter2', 'parameter3'],
                               parameter_values3, [['a_obj1', 'b_obj1'], ['a_obj2', 'b_obj2'], ['a_obj3', 'b_obj3']], 'relationship')

        test_data, test_log = merge_spine_xlsx_data([data1, data2])

        self.assertEqual(len(test_log), 0)
        self.assertEqual(len(test_data), 1)
        self.assertEqualSheetData(test_data[0], valid_data)

    def test_merge_spine_xlsx_data_diffent_obj_class_names(self):
        """Test merging array of SheetData with different object class names, keep only first SheetData"""
        parameter_values1 = [self.RelData('value', 'a_obj1', 'b_obj1', 'parameter1', 1),
                             self.RelData('value', 'a_obj2', 'b_obj2', 'parameter2', 2)]
        parameter_values2 = [self.RelData('value', 'a_obj1', 'b_obj1', 'parameter1', 1),
                             self.RelData('value', 'a_obj3', 'b_obj3', 'parameter3', 2)]
        data1 = SheetData('title', 'relationship_name',
                          self.data_class_rel[0], ['parameter1', 'parameter2'],
                          parameter_values1, [['a_obj1', 'b_obj1'], ['a_obj2', 'b_obj2']], 'relationship')
        data2 = SheetData('title', 'relationship_name',
                          ['object_class_name', 'wrong_name'], [
                              'parameter1', 'parameter3'],
                          parameter_values2, [['a_obj1', 'b_obj1'], ['a_obj3', 'b_obj3']], 'relationship')

        test_data, test_log = merge_spine_xlsx_data([data1, data2])

        self.assertEqual(len(test_log), 1)
        self.assertEqual(len(test_data), 1)
        self.assertEqualSheetData(test_data[0], data1)

    def test_read_json_sheet_all_valid_relationship(self):
        """Test reading a sheet with object parameter"""
        ws = self.ws_rel_json
        parameter_values = [self.RelData('json', 'a_obj1', 'b_obj1', 'parameter1', '[1, 2, 3]'),
                            self.RelData('json', 'a_obj2', 'b_obj2', 'parameter2', '[4, 5, 6]')]
        test_data = SheetData('title', 'relationship_name',
                              self.data_class_rel[0], list(
                                  set(self.data_parameter)),
                              parameter_values, [], 'relationship')

        with mock.patch('excel_import_export.read_2d') as mock_read_2d:
            mock_read_2d.side_effect = self.data_class_rel
            out_data = read_json_sheet(ws, 'relationship')
        self.assertEqualSheetData(test_data, out_data)

    def test_read_json_sheet_all_valid_object(self):
        """Test reading a sheet with object parameter"""
        ws = self.ws_obj_json
        parameter_values = [self.ObjData('json', 'obj1', 'parameter1', '[1, 2, 3]'),
                            self.ObjData('json', 'obj2', 'parameter2', '[4, 5, 6]')]
        test_data = SheetData('title', 'object_class_name',
                              self.data_class_obj[0], list(
                                  set(self.data_parameter)),
                              parameter_values, [], 'object')

        with mock.patch('excel_import_export.read_2d') as mock_read_2d:
            mock_read_2d.side_effect = self.data_class_obj
            out_data = read_json_sheet(ws, 'object')
        self.assertEqualSheetData(test_data, out_data)

    def test_read_parameter_sheet_all_valid_object(self):
        """Test reading a sheet with object parameter"""
        ws = self.ws_obj
        parameter_values = [self.ObjData('value', 'obj1', 'parameter1', 1),
                            self.ObjData('value', 'obj1', 'parameter2', 'a'),
                            self.ObjData('value', 'obj2', 'parameter1', 2),
                            self.ObjData('value', 'obj2', 'parameter2', 'b')]
        test_data = SheetData('title', 'object_class_name',
                              self.data_class_obj[0], self.data_parameter,
                              parameter_values, self.class_obj_obj, 'object')

        with mock.patch('excel_import_export.read_2d') as mock_read_2d:
            mock_read_2d.side_effect = [self.data_class_obj, self.data_obj]
            out_data = read_parameter_sheet(ws)
        self.assertEqualSheetData(test_data, out_data)

    def test_read_parameter_sheet_all_valid_relationship(self):
        """Test reading a sheet with object parameter"""
        ws = self.ws_rel
        parameter_values = [self.RelData('value', 'a_obj1', 'b_obj1', 'parameter1', 1),
                            self.RelData('value', 'a_obj1',
                                         'b_obj1', 'parameter2', 'a'),
                            self.RelData('value', 'a_obj2',
                                         'b_obj2', 'parameter1', 2),
                            self.RelData('value', 'a_obj2', 'b_obj2', 'parameter2', 'b')]
        test_data = SheetData('title', 'relationship_name',
                              self.data_class_rel[0], self.data_parameter,
                              parameter_values, self.class_obj_rel, 'relationship')

        with mock.patch('excel_import_export.read_2d') as mock_read_2d:
            mock_read_2d.side_effect = [self.data_class_rel, self.data_rel]
            out_data = read_parameter_sheet(ws)
        self.assertEqualSheetData(test_data, out_data)

    def test_read_parameter_sheet_with_None_containing_rels(self):
        """Test reading a sheet where one relationship contains a None value
        to make sure invalid rows are not read"""
        ws = self.ws_rel
        # make last row in data invalid
        self.data_rel[1][0] = None
        self.class_obj_rel.pop(1)

        parameter_values = [self.RelData('value', 'a_obj1', 'b_obj1', 'parameter1', 1),
                            self.RelData('value', 'a_obj1', 'b_obj1', 'parameter2', 'a')]
        test_data = SheetData('title', 'relationship_name',
                              self.data_class_rel[0], self.data_parameter,
                              parameter_values, self.class_obj_rel, 'relationship')

        with mock.patch('excel_import_export.read_2d') as mock_read_2d:
            mock_read_2d.side_effect = [self.data_class_rel, self.data_rel]
            out_data = read_parameter_sheet(ws)
        self.assertEqualSheetData(test_data, out_data)

    def test_read_parameter_sheet_with_None_parameter_values(self):
        """Test reading a sheet with None values in parameter value cells"""
        ws = self.ws_obj
        self.data_obj[1][1] = None
        parameter_values = [self.ObjData('value', 'obj1', 'parameter1', 1),
                            self.ObjData('value', 'obj1', 'parameter2', 'a'),
                            self.ObjData('value', 'obj2', 'parameter2', 'b')]
        test_data = SheetData('title', 'object_class_name',
                              self.data_class_obj[0], self.data_parameter,
                              parameter_values, self.class_obj_obj, 'object')

        with mock.patch('excel_import_export.read_2d') as mock_read_2d:
            mock_read_2d.side_effect = [self.data_class_obj, self.data_obj]
            out_data = read_parameter_sheet(ws)
        self.assertEqualSheetData(test_data, out_data)

    def test_validate_sheet_valid_relationship(self):
        """Test that a valid sheet with relationship as sheet_type will return true"""
        with mock.patch('excel_import_export.read_2d') as mock_read_2d:
            mock_read_2d.return_value = [['obj_class1', 'obj_class2']]
            ws_mock = self.ws_rel
            self.assertTrue(validate_sheet(ws_mock))
            # check that validation is case insensitive
            ws_mock['A2'].value = 'RelatIonShip'
            ws_mock['B2'].value = 'paRameTer'
            self.assertTrue(validate_sheet(ws_mock))
            # check json array as Data type
            ws_mock['B2'].value = 'json array'
            mock_read_2d.return_value = [['obj_class1'], ['obj_class2']]
            self.assertTrue(validate_sheet(ws_mock))

    def test_validate_sheet_invalid_relationship(self):
        """Test that an invalid sheet with relationship as sheet_type will return false"""
        ws_mock = self.ws_rel
        # check invalid type
        with mock.patch('excel_import_export.read_2d') as mock_read_2d:
            mock_read_2d.return_value = [['obj_class1', 'obj_class2']]
            # wrong relationship name
            ws_mock['C2'].value = ''
            self.assertFalse(validate_sheet(ws_mock))
            ws_mock['C2'].value = None
            self.assertFalse(validate_sheet(ws_mock))
            ws_mock['C2'].value = 3
            self.assertFalse(validate_sheet(ws_mock))
            # wrong number of relationship classes
            ws_mock['C2'].value = 'relationship_name'
            mock_read_2d.return_value = [['obj_class1', None]]
            self.assertFalse(validate_sheet(ws_mock))
            mock_read_2d.return_value = [['obj_class1', 1]]
            self.assertFalse(validate_sheet(ws_mock))
            mock_read_2d.return_value = [['obj_class1', '']]
            self.assertFalse(validate_sheet(ws_mock))
            # wrong number of relationship supplied
            mock_read_2d.return_value = [['obj_class1', 'obj_class2']]
            ws_mock['D2'].value = 0
            self.assertFalse(validate_sheet(ws_mock))
            ws_mock['D2'].value = 'abc'
            self.assertFalse(validate_sheet(ws_mock))
            ws_mock['D2'].value = 1
            self.assertFalse(validate_sheet(ws_mock))

    def test_validate_sheet_valid_object(self):
        """Test that a valid sheet with object as sheet_type will return true"""
        ws_mock = self.ws_obj
        self.assertTrue(validate_sheet(ws_mock))
        # check json array as Data type
        ws_mock['B2'].value = 'json array'
        self.assertTrue(validate_sheet(ws_mock))
        # check that validation is case insensitive
        ws_mock['A2'].value = 'oBjeCt'
        ws_mock['B2'].value = 'paRameTer'
        self.assertTrue(validate_sheet(ws_mock))

    def test_validate_sheet_invalid_object(self):
        """Test that an invalid sheet with object as sheet_type will return false"""
        ws_mock = self.ws_obj
        # check invalid type
        ws_mock['A2'].value = 1
        self.assertFalse(validate_sheet(ws_mock))
        ws_mock['A2'].value = 'object'
        ws_mock['B2'].value = 4
        ws_mock['C2'].value = 'some_name'
        self.assertFalse(validate_sheet(ws_mock))
        ws_mock['A2'].value = 'object'
        ws_mock['B2'].value = 'parameter'
        ws_mock['C2'].value = 6
        # check invalid name
        ws_mock['A2'].value = 'invalid_sheet_type'
        ws_mock['B2'].value = 'parameter'
        ws_mock['C2'].value = 'some_name'
        self.assertFalse(validate_sheet(ws_mock))
        ws_mock['A2'].value = 'object'
        ws_mock['B2'].value = 'invalid_parameter_type'
        ws_mock['C2'].value = 'some_name'
        self.assertFalse(validate_sheet(ws_mock))
        # check invlad object name
        ws_mock['A2'].value = 'object'
        ws_mock['B2'].value = 'parameter'
        ws_mock['C2'].value = ''
        self.assertFalse(validate_sheet(ws_mock))
        # check empty values
        ws_mock['A2'].value = None
        ws_mock['B2'].value = 'parameter'
        ws_mock['C2'].value = 'some_name'
        self.assertFalse(validate_sheet(ws_mock))
        ws_mock['A2'].value = 'object'
        ws_mock['B2'].value = None
        ws_mock['C2'].value = 'some_name'
        self.assertFalse(validate_sheet(ws_mock))
        ws_mock['A2'].value = 'object'
        ws_mock['B2'].value = 'parameter'
        ws_mock['C2'].value = None
        self.assertFalse(validate_sheet(ws_mock))


class TestStackUnstack(unittest.TestCase):

    def test_stack_list_of_tuples(self):
        """Test transformation of pivoted table into a stacked table"""

        fieldnames = ["col1", "col2", "parameter", "value"]
        TestDataTuple = namedtuple("Data", fieldnames)
        headers = ["col1", "col2", "pivot_col1", "pivot_col2"]
        key_cols = [0, 1]
        value_cols = [2, 3]
        data_in = [["col1_v1", "col2_v1", "pivot_col1_v1", "pivot_col2_v1"],
                   ["col1_v2", "col2_v2", "pivot_col1_v2", "pivot_col2_v2"],
                   ["col1_v3", "col2_v3", "pivot_col1_v3", "pivot_col2_v3"]]
        data_out = sorted([TestDataTuple("col1_v1", "col2_v1", "pivot_col1", "pivot_col1_v1"),
                           TestDataTuple("col1_v2", "col2_v2",
                                         "pivot_col1", "pivot_col1_v2"),
                           TestDataTuple("col1_v1", "col2_v1",
                                         "pivot_col2", "pivot_col2_v1"),
                           TestDataTuple("col1_v2", "col2_v2",
                                         "pivot_col2", "pivot_col2_v2"),
                           TestDataTuple("col1_v3", "col2_v3",
                                         "pivot_col1", "pivot_col1_v3"),
                           TestDataTuple("col1_v3", "col2_v3", "pivot_col2", "pivot_col2_v3")])

        test_data_out = sorted(stack_list_of_tuples(
            data_in, headers, key_cols, value_cols))

        for d, t in zip(data_out, test_data_out):
            for f in fieldnames:
                self.assertEqual(getattr(d, f), getattr(t, f))
        #self.assertEqual(data_out, test_data_out)

    def test_unstack_list_of_tuples(self):
        """Test transformation of unpivoted table into a pivoted table"""

        fieldnames = ["col1", "col2", "pivot_col1", "pivot_col2"]
        headers = ["col1", "col2", "parameter", "value"]
        key_cols = [0, 1]
        value_name_col = 2
        value_col = 3
        data_in = [["col1_v1", "col2_v1", "pivot_col1", "pivot_col1_v1"],
                   ["col1_v2", "col2_v2", "pivot_col1", "pivot_col1_v2"],
                   ["col1_v1", "col2_v1", "pivot_col2", "pivot_col2_v1"],
                   ["col1_v2", "col2_v2", "pivot_col2", "pivot_col2_v2"],
                   ["col1_v3", "col2_v3", "pivot_col2", "pivot_col2_v3"]]

        data_out = [["col1_v1", "col2_v1", "pivot_col1_v1", "pivot_col2_v1"],
                    ["col1_v2", "col2_v2", "pivot_col1_v2", "pivot_col2_v2"],
                    ["col1_v3", "col2_v3", None, "pivot_col2_v3"]]

        test_data_out, new_headers  = unstack_list_of_tuples(data_in, headers, key_cols, value_name_col, value_col)

        self.assertEqual(test_data_out, data_out)
        self.assertEqual(new_headers, fieldnames)

    def test_unstack_list_of_tuples_with_bad_names(self):
        """Test transformation of unpivoted table into a pivoted table when column to pivot has name not supported by namedtuple"""

        fieldnames = ["col1", "col2", "pivot col1", "pivot col2"]
        headers = ["col1", "col2", "parameter", "value"]
        key_cols = [0, 1]
        value_name_col = 2
        value_col = 3
        data_in = [["col1_v1", "col2_v1", "pivot col1", "pivot_col1_v1"],
                   ["col1_v2", "col2_v2", "pivot col1", "pivot_col1_v2"],
                   ["col1_v1", "col2_v1", "pivot col2", "pivot_col2_v1"],
                   ["col1_v2", "col2_v2", "pivot col2", "pivot_col2_v2"],
                   ["col1_v3", "col2_v3", "pivot col2", "pivot_col2_v3"]]

        data_out = [["col1_v1", "col2_v1", "pivot_col1_v1", "pivot_col2_v1"],
                    ["col1_v2", "col2_v2", "pivot_col1_v2", "pivot_col2_v2"],
                    ["col1_v3", "col2_v3", None, "pivot_col2_v3"]]

        test_data_out, new_headers = unstack_list_of_tuples(data_in, headers, key_cols, value_name_col, value_col)

        self.assertEqual(test_data_out, data_out)
        self.assertEqual(new_headers, fieldnames)

    # TODO: add functionality to function
    def test_unstack_list_of_tuples_multiple_pivot_cols(self):
        """Test transformation of unpivoted table into a pivoted table with multiple pivot columns"""
        headers = ["col1", "col2", "parameter", "value"]
        key_cols = [0]
        value_name_col = [1, 2]
        value_col = 3
        data_in = [["col1_v1", "col2_v1", "pivot_col1", "pivot_col1_v1"],
                   ["col1_v2", "col2_v2", "pivot_col1", "pivot_col1_v2"],
                   ["col1_v1", "col2_v1", "pivot_col2", "pivot_col2_v1"],
                   ["col1_v2", "col2_v2", "pivot_col2", "pivot_col2_v2"],
                   ["col1_v3", "col2_v3", "pivot_col2", "pivot_col2_v3"]]

        headers_out = ["col1",
                       ("col2_v1", "pivot_col1"),
                       ("col2_v1", "pivot_col2"),
                       ("col2_v2", "pivot_col1"),
                       ("col2_v2", "pivot_col2"),
                       ("col2_v3", "pivot_col2")]
        data_out = [["col1_v1", "pivot_col1_v1", "pivot_col2_v1", None, None, None],
                    ["col1_v2", None, None, "pivot_col1_v2", "pivot_col2_v2", None],
                    ["col1_v3", None, None, None, None, "pivot_col2_v3"]]

        test_data_out, test_header_out = unstack_list_of_tuples(data_in, headers, key_cols, value_name_col, value_col)

        self.assertEqual(data_out, test_data_out)
        self.assertEqual(headers_out, test_header_out)


if __name__ == '__main__':
    unittest.main()
