"""
在数据库中创建表faq，
将数据加入到faq数据库，给出后续想要加载数据库文件的接口
"""

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "data", "faq.db")


def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faq (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def insert_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    data = [
        ("多久发货？", "一般在24小时内发货"),
        ("支持退货吗？", "支持7天无理由退货"),
        ("运费怎么算？", "满99元包邮，不满收取10元运费"),
        ("可以开发票吗？", "可以提供电子发票"),
        ("订单多久能到？", "一般3-5个工作日送达"),
        ("如何联系客服？", "请通过邮箱联系我们"),
        ("如何退货？", "请先联系客服，确认退货条件，然后进行退货"),
        ("如何申请退货？", "请先联系客服，确认退货条件，然后进行退货"),
        ("如何申请退款？", "请先联系客服，确认退款条件，然后进行退款"),
        ("如何申请换货？", "请先联系客服，确认换货条件，然后进行换货"),
        ("如何申请售后？", "请先联系客服，确认售后条件，然后进行售后"),
        ("如何申请投诉？", "请先联系客服，确认投诉条件，然后进行投诉"),
        ("如何申请注销账户？", "请先联系客服，确认注销条件，然后进行注销"),

    ]

    cursor.executemany("INSERT INTO faq (question, answer) VALUES (?, ?)", data)

    conn.commit()
    conn.close()

def query_all():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM faq")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()

def load_faq():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, question, answer FROM faq")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "question": r[1], "answer": r[2]} for r in rows]

if __name__ == "__main__":
    create_table()
    insert_data()
    query_all()
