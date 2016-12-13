import ifttt
import csv
import os.path
import datetime


class Output(object):

    def on_income(self, amount, category, message):
        pass

    def on_expense(self, amount, category, message):
        pass


class Writer (object):

    def write_row(self, row):
        pass


class CsvWriter(Writer):

    def __init__(self, path):
        self._path = path

    def write_row(self, row):
        with open(self._path, 'ab') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(row)


class ExcelWriter(Writer):

    def __init__(self, path):
        self._path = path


class TimestampSupplier(object):

    def get_timestamp(self):
        pass


class NowSupplier(TimestampSupplier):

    def get_timestamp(self):
        return datetime.datetime.now()


class WriterOutput(Output):

    def __init__(self, writer, timestamp_supplier):
        self._writer = writer
        self._timestamp_supplier = timestamp_supplier

    def _write_row(self, row):
        self._writer.write_row(row)

    def on_income(self, amount, category, message):
        self._write_row([
            self._timestamp_supplier.get_timestamp(),
            amount,
            None,
            category,
            message
        ])

    def on_expense(self, amount, category, message):
        self._write_row([
            self._timestamp_supplier.get_timestamp(),
            None,
            amount,
            category,
            message
        ])


class IftttOutput(Output):

    def __init__(self, key, income_event, expense_event):
        self._client = ifttt.IftttClient(key)
        self._income_event = income_event
        self._expense_event = expense_event

    def on_income(self, amount, category, message):
        self._client.trigger(self._income_event, amount, category, message)

    def on_expense(self, amount, category, message):
        self._client.trigger(self._expense_event, amount, category, message)
