import pandas as pd
from sqlalchemy import create_engine

# 1. DB 연결 설정 (안전한 절대 경로 유지)
engine = create_engine('sqlite:///C:/Users/User/Downloads/test_etl.db')

# 2. PK 중복 검증 쿼리 (SK_ID_CURR 고유 ID 기준)
# ID별로 그룹을 묶었을 때 개수가 1개를 초과하는(즉, 중복된) 데이터의 건수를 셉니다.
pk_query = """
SELECT COUNT(*) 
FROM (
    SELECT SK_ID_CURR 
    FROM application_train_final 
    GROUP BY SK_ID_CURR 
    HAVING COUNT(SK_ID_CURR) > 1
);
"""
duplicate_pk_count = pd.read_sql(pk_query, con=engine).iloc[0, 0]

# 3. 필수 컬럼(Not Null) 누락 검증 쿼리
# 고유 ID에 빈칸(NULL)이 있는 데이터의 건수를 셉니다.
null_query = """
SELECT COUNT(*) 
FROM application_train_final 
WHERE SK_ID_CURR IS NULL;
"""
null_count = pd.read_sql(null_query, con=engine).iloc[0, 0]

# 4. 결과 출력
print("🔑 [Day 18] PK 중복 및 Not Null 검증 결과")
print("-" * 50)
print(f"👯 중복된 PK(고유 ID) 건수 : {duplicate_pk_count:,}건")
print(f"👻 필수 컬럼(빈칸) 누락 건수 : {null_count:,}건")
print("-" * 50)

if duplicate_pk_count == 0 and null_count == 0:
    print("✅ 검증 통과: 데이터 식별자(PK)가 아주 건강합니다! (중복/누락 0건)")
else:
    print("❌ 검증 실패: 중복되거나 누락된 데이터가 발견되었습니다.")