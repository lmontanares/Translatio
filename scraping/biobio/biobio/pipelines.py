# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pathlib import Path
import sqlite3


class BiobioPipeline:
    def open_spider(self, spider):
        self.con = sqlite3.connect("/opt/scraped_data/biobio.db")
        self.cur = self.con.cursor()

        # Check if the 'news' table exists, create it if not
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS news
            (url text UNIQUE, title text, category text, date text, view_count text)
            """
        )

    def close_spider(self, spider):
        self.con.close()

    def process_item(self, item, spider):
        try:
            self.cur.execute(
                "SELECT 1 FROM news WHERE url = ?", (item["url"],)
            )
            row_exists = self.cur.fetchone() is not None

            self.cur.execute(
                """
                INSERT INTO news (url, title, category, date, view_count)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(url) DO UPDATE SET
                title = excluded.title,
                category = excluded.category,
                date = excluded.date,
                view_count = excluded.view_count
                """,
                (
                    item["url"],
                    item["title"],
                    item["category"],
                    item["date"],
                    item["view_count"],
                ),
            )
            self.con.commit()
            if row_exists:
                spider.logger.info(
                    f"[Translatio] Item updated in SQLITE3 {item}"
                )
            else:
                spider.logger.info(
                    f"[Translatio] Item inserted into SQLITE3 {item}"
                )

        except Exception as e:
            spider.logger.error(
                f"[Translatio] Failed to insert or update item into database: {e}"
            )
        return item
