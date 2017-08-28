""" Testing Migration Module
"""

import unittest
from mock import MagicMock, patch, call
from ashaw_notes.utils.connection_manager import ConnectionManager
from ashaw_notes.scripts import migration


class MigrationTests(unittest.TestCase):
    """Unit Testing Migration"""

    @patch('ashaw_notes.scripts.migration.migrate_notes')
    @patch.object(ConnectionManager, 'load_connector')
    def test_run_migrations_no_parameters(
            self,
            load_connector,
            migrate_notes):
        """Verifies run_migrations blocks call with no parameters"""
        migration.run(None, None)
        load_connector.assert_not_called()
        migrate_notes.assert_not_called()

    @patch('ashaw_notes.scripts.migration.migrate_notes')
    @patch.object(ConnectionManager, 'load_connectors')
    @patch.object(ConnectionManager, 'load_connector')
    def test_run_migrations_one_parameters(
            self,
            load_connector,
            load_connectors,
            migrate_notes):
        """Verifies run_migrations blocks call with only one parameter"""
        load_connector.return_value = 1
        load_connectors.return_value = True
        migration.run('local_notes', None)
        load_connector.assert_called_once_with('local_notes')
        migrate_notes.assert_not_called()

    @patch('ashaw_notes.scripts.migration.migrate_notes')
    @patch.object(ConnectionManager, 'load_connectors')
    @patch.object(ConnectionManager, 'load_connector')
    def test_run_migrations_success(
            self,
            load_connector,
            load_connectors,
            migrate_notes):
        """Verifies run_migrations is properly functioning"""
        load_connector.side_effect = ['source', 'target']
        load_connectors.return_value = True
        migration.run('local_notes', 'redis_notes')
        load_connector.assert_has_calls(
            [call('local_notes'), call('redis_notes')])
        migrate_notes.assert_called_once_with('source', 'target')

    def test_migrate_notes(self):
        """Verifies migrate_notes is properly functioning"""
        source = MagicMock()
        source.find_notes.return_value = [
            (0, 'note1'),
            (1, 'note2'),
            (2, 'note3'),
        ]
        target = MagicMock()

        migration.migrate_notes(source, target)

        source.find_notes.assert_called_once_with([])
        target.save_note.assert_has_calls([
            call(0, 'note1'),
            call(1, 'note2'),
            call(2, 'note3'),
        ])
