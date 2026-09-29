import pandas as pd
from sqlalchemy import create_engine

# 1. 아까 만든 DB 창고(test_etl.db)에 연결
engine = create_engine('sqlite:///test_etl.db')
table_name = 'application_train_full'

# 2. 전체 데이터 개수(Count) 확인하기
# SQL 쿼리: "테이블의 모든 행(*) 개수를 세어라(COUNT)"
count_query = f"SELECT COUNT(*) FROM {table_name}"
total_count = pd.read_sql(count_query, con=engine).iloc[0, 0]

print(f"✅ DB 창고에 안전하게 보관된 총 데이터 건수: {total_count:,}건\n")

# 3. 데이터가 예쁘게 들어갔는지 위에서 5건만(LIMIT) 꺼내보기
# SQL 쿼리: "테이블에서 모든 데이터(*)를 가져오되, 딱 5개까지만 제한(LIMIT)해라"
select_query = f"SELECT * FROM {table_name} LIMIT 5"
df_head = pd.read_sql(select_query, con=engine)

print("✨ 창고 안의 데이터 미리보기 (상위 5건):")
print(df_head)