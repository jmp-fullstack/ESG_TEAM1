# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import datetime
import csv
from scrapy.exporters import CsvItemExporter

class NameCsvPipeline:
    def open_spider(self, spider):
        now = datetime.datetime.now()
        filename = f"kosdaq_data_{now.strftime('%Y-%m-%d')}.csv"
        self.file = open(filename, 'wb')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item