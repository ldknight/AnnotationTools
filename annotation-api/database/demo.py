import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()
print ("数据库打开成功")

cursor = c.execute("select * from project where  proj_url_ago='/Users/liudun/Desktop/anno_tools/AnnotationTools/demo_imgs'  limit 1")
names = list(map(lambda x: x[0], cursor.description))
print(names)
for row in cursor:
   print(row)

print ("数据操作成功")
conn.close()