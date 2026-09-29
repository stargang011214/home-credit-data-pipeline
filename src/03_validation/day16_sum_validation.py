import pandas as pd
from sqlalchemy import create_engine

# 1. 원본 CSV 파일에서 특정 금액 컬럼의 합계 구하기
# (메모리 절약을 위해 타깃인 'AMT_CREDIT'(대출 금액) 컬럼 딱 1개만 읽어옵니다)
file_path = r'C:\Users\User\Downloads\home-credit-default-risk\application_train.csv'
df_csv = pd.read_csv(file_path, usecols=['AMT_CREDIT'])

# 파이썬과 DB의 미세한 소수점 계산 차이(부동소수점 오차)를 방지하기 위해 소수점 2자리에서 반올림 처리
csv_sum = round(df_csv['AMT_CREDIT'].sum(), 2)

# 2. DB 창고에 적재된 데이터의 금액 합계 구하기 (SQL 쿼리 사용)
# Day 15에서 길 잃음을 방지하기 위해 사용했던 '절대 경로'를 그대로 사용합니다.
engine = create_engine('sqlite:///C:/Users/User/Downloads/test_etl.db')
query = "SELECT SUM(AMT_CREDIT) FROM application_train_final"

# DB에 쿼리를 날려서 총합을 계산해 오라고 시킨 뒤, 결과를 소수점 2자리로 맞춥니다.
db_sum = round(pd.read_sql(query, con=engine).iloc[0, 0], 2)

# 3. 결과 대조 및 출력
print("💰 [Day 16] 수치 합계(Sum) 검증 결과")
print("-" * 50)
print(f"📁 원본 파일 총 대출 금액 : {csv_sum:,.2f}")
print(f"🗄️ DB 테이블 총 대출 금액 : {db_sum:,.2f}")
print("-" * 50)

if csv_sum == db_sum:
    print("✅ 검증 통과: 총 대출 금액이 100% 일치합니다! (수치 변조/누락 없음)")
else:
    print(f"❌ 검증 실패: 금액이 불일치합니다. 차액: {abs(csv_sum - db_sum):,.2f}")