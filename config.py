import yaml
import categories
import outputs

class Config(object):

    @property
    def telegram_token(self):
        return self._telegram_token

    @telegram_token.setter
    def telegram_token(self, value):
        self._telegram_token = value

    @property
    def allowed_users(self):
        return self._allowed_users

    @allowed_users.setter
    def allowed_users(self, value):
        self._allowed_users = value

    @property
    def outputs(self):
        return self._outputs

    @outputs.setter
    def outputs(self, value):
        self._outputs = value

    @property
    def categories_supplier(self):
        return self._categories_supplier

    @categories_supplier.setter
    def categories_supplier(self, value):
        self._categories_supplier = value

class ConfigFactory(object):

    def get_config(self):
        pass

class YamlConfigFactory(ConfigFactory):

    def __init__(self, path):
        self._path = path

    def get_config(self):
        with open(self._path) as file:
            return self._build(yaml.load(file))

    def _build(self, data):
        config = Config()
        config.telegram_token = self._get_mandatory_parameter(data, 'telegram_token')
        config.allowed_users = self._get_mandatory_parameter(data, 'allowed_users')
        cats = self._get_mandatory_parameter(data, 'categories')
        config.categories_supplier = categories.CategoriesSupplier(cats)
        config.outputs = []
        outs = self._get_mandatory_parameter(data, 'outputs')
        for output in outs:
            type = self._get_mandatory_parameter(output, 'type')
            if type == 'ifttt':
                config.outputs.append(outputs.IftttOutput(
                    self._get_mandatory_parameter(output, 'api_key'),
                    self._get_mandatory_parameter(output, 'income_event'),
                    self._get_mandatory_parameter(output, 'expense_event')))
            if type == 'csv':
                config.outputs.append(outputs.WriterOutput(outputs.CsvWriter(
                    self._get_mandatory_parameter(output, 'file')), outputs.NowSupplier()))
            if type == 'excel':
                config.outputs.append(outputs.WriterOutput(outputs.ExcelWriter(
                    self._get_mandatory_parameter(output, 'file')), outputs.NowSupplier()))
        return config

    def _get_mandatory_parameter(self, data, key):
        if not key in data:
            raise Exception("Missing parameter: {}".format(key))
        return data[key]