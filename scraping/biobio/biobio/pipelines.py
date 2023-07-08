# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pathlib import Path
import sqlite3
from settings import DATA_PATH

DATA_PATH.as_posix()


class BiobioPipeline:
    def open_spider(self, spider):
        with sqlite3.connect(DATA_PATH.as_posix() / "biobio.db") as self.con:
            self.cur = self.con.cursor()
            self.cur.execute("""DROP TABLE IF EXISTS noticia""")
            self.cur.execute(
                """CREATE TABLE noticia (url text, title text, category text, date text, view_count text)"""
            )

    def close_spider(self, spider):
        self.con.close()

    def process_item(self, item, spider):
        try:
            with self.con:
                self.cur.execute(
                    """INSERT INTO noticia (url, title, category, date, view_count) VALUES (?, ?, ?, ?, ?)""",
                    (
                        item["url"],
                        item["title"],
                        item["category"],
                        item["date"],
                        item["view_count"],
                    ),
                )
                spider.logger.info(
                    f"[Translatio] Item inserted into SQLITE3 {item}"
                )
        except Exception as e:
            spider.logger.error(
                f"[Translatio] Failed to insert item into database: {e}"
            )
        return item
