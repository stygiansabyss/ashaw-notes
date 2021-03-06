"""Connection Manager Module
"""
import importlib
import ashaw_notes.utils.configuration


class ConnectionManager:
    """Connection Manager Class"""
    connectors = None

    def __init__(self):
        if not self.connectors:
            self.load_connectors()

    def load_connectors(self):
        """Returns all enabled plugins"""
        self.connectors = []
        config = ashaw_notes.utils.configuration.load_config()
        module_names = config.get('base_config', 'data_backends')
        for module_name in [name.strip() for name in module_names.split(',')]:
            self.connectors.append(
                self.load_connector(module_name)
            )
        return self.connectors

    def load_connector(self, connector_class_name):
        return importlib.import_module(
            "ashaw_notes.connectors.%s" % connector_class_name
        )

    def get_primary_connector(self):
        """Returns primary backend connector"""
        return self.connectors[0]
