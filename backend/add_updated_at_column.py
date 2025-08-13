import sqlite3

conn = sqlite3.connect('instance/scriptscope.db')
try:
    conn.execute('ALTER TABLE section ADD COLUMN updated_at DATETIME')
    print('Column added successfully.')
except Exception as e:
    print('Error:', e)
finally:
    conn.commit()
    conn.close()
