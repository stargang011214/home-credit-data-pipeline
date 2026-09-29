import pandas as pd
from sqlalchemy import create_engine

# 1. DB 창고(test_etl.db) 연결
engine = create_engine('sqlite:///test_etl.db')

# 2. SQL 쿼리 작성: 대출 종류별 전체 건수, 연체 건수, 연체율(%) 계산
query = """
SELECT 
    NAME_CONTRACT_TYPE AS '대출 종류',
    COUNT(*) AS '전체 건수',
    SUM(TARGET) AS '연체 건수',
    ROUND(SUM(TARGET) * 100.0 / COUNT(*), 2) AS '연체율(%)'
FROM application_train_full
GROUP BY NAME_CONTRACT_TYPE
"""

# 3. DB에 쿼리 날려서 결과 받아오기
df_analysis = pd.read_sql(query, con=engine)

print("📊 대출 종류별 실제 연체율 비교:\n")
print(df_analysis)