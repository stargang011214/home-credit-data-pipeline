import pandas as pd
from sqlalchemy import create_engine

# 1. 아까 만든 DB 창고(test_etl.db)에 다시 연결 통로 열기
engine = create_engine('sqlite:///test_etl.db')

# 2. SQL 쿼리문으로 데이터 가져오기 
# (의미: application_train_test 테이블의 모든(*) 데이터를 가져와라!)
query = "SELECT * FROM application_train_test"
df_from_db = pd.read_sql(query, con=engine)

# 3. 창고에서 꺼낸 데이터 화면에 출력하기
print("✨ DB 창고 안에 안전하게 보관된 데이터 10건:")
print(df_from_db)