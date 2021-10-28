from sqlalchemy import create_engine

DATABASEURI = "postgresql://zh2481:123465@35.196.73.133/proj1part2"

engine = create_engine(DATABASEURI)  # 用户名:密码@localhost:端口/数据库名
conn = engine.connect()

queries = "SELECT * FROM FOLLOW"
cursor = conn.execute(queries)
record = cursor.fetchone()
print(record)
