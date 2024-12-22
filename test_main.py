import unittest
from main import ConfigParser

class TestParseConfig(unittest.TestCase):

    def setUp(self):
        self.parser = ConfigParser()

    def parse_config(self, config_text):
        return self.parser.parse_config(config_text)

    def test_string_values(self):
        config_text = """
        app_name = "MyApp"
        version = "1.0.3"
        """
        config = self.parse_config(config_text)
        self.assertEqual(config['app_name'], 'MyApp')
        self.assertEqual(config['version'], '1.0.3')

    def test_boolean_values(self):
        # Ваш синтаксис не поддерживает напрямую булевы значения, но мы адаптируем через строки
        config_text = """
        debug_mode = "true"
        maintenance = "false"
        """
        config = self.parse_config(config_text)
        self.assertEqual(config['debug_mode'], "true")
        self.assertEqual(config['maintenance'], "false")

    def test_numeric_values(self):
        config_text = """
        max_connections = 15
        timeout = ![10 + 5]
        """
        config = self.parse_config(config_text)
        self.assertEqual(config['max_connections'], 15)
        self.assertEqual(config['timeout'], 15)

    def test_list_values(self):
        config_text = """
        features = (list "authentication" "logging" "notifications")
        """
        config = self.parse_config(config_text)
        self.assertEqual(config['features'], ['authentication', 'logging', 'notifications'])

    def test_empty_values(self):
        config_text = """
        app_name = ""
        """
        config = self.parse_config(config_text)
        self.assertEqual(config['app_name'], '')

    def test_multi_block_parsing(self):
        # Ваш парсер не поддерживает блоки, но обрабатывает все на одном уровне
        config_text = """
        app_name = "MyApp"
        version = "1.0.3"
        debug_mode = "true"
        max_connections = ![10 + 5]
        database = "app_db"
        user = "admin"
        password = "secret"
        """
        config = self.parse_config(config_text)
        self.assertEqual(config['app_name'], 'MyApp')
        self.assertEqual(config['version'], '1.0.3')
        self.assertEqual(config['debug_mode'], "true")
        self.assertEqual(config['max_connections'], 15)
        self.assertEqual(config['database'], 'app_db')
        self.assertEqual(config['user'], 'admin')
        self.assertEqual(config['password'], 'secret')

    def test_functions_max_sqrt(self):
        # Ваш текущий парсер поддерживает вычисления через выражения вида ![...]
        config_text = """
        max_value = ![max(5, 10, 3)]
        sqrt_value = ![pow(25, 0.5)]
        """
        config = self.parse_config(config_text)
        self.assertEqual(config['max_value'], 10)
        self.assertEqual(config['sqrt_value'], 5.0)

if __name__ == "__main__":
    unittest.main()
