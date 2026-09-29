import pandas as pd
from sqlalchemy import create_engine

# 1. 원본 CSV 파일의 데이터 건수 세기 
# (30만 건 전체를 메모리에 다 올리면 무거우므로, 고유 ID인 첫 번째 컬럼 딱 1개만 가볍게 읽어옵니다)
file_path = r'C:\Users\User\Downloads\home-credit-default-risk\application_train.csv'
df_csv = pd.read_csv(file_path, usecols=[0]) 
csv_count = len(df_csv)

# 2. DB 창고에 적재된 데이터 건수 세기 (SQL 쿼리 사용)
engine = create_engine('sqlite:///C:/Users/User/Downloads/test_etl.db')
query = "SELECT COUNT(*) FROM application_train_final"

# DB에 쿼리를 날려서 나온 결과표의 첫 번째 줄, 첫 번째 칸(0,0)의 숫자만 쏙 뽑아옵니다.
db_count = pd.read_sql(query, con=engine).iloc[0, 0]

# 3. 결과 대조 및 출력
print("📊 [Day 15] 데이터 적재 건수 검증 결과")
print("-" * 50)
print(f"📁 원본 CSV 파일 건수 : {csv_count:,}건")
print(f"🗄️ DB 테이블 적재 건수 : {db_count:,}건")
print("-" * 50)

if csv_count == db_count:
    print("✅ 검증 통과: 데이터 건수가 100% 일치합니다! (유실/중복 없음)")
else:
    print("❌ 검증 실패: 데이터 건수가 불일치합니다. 파이프라인 누수를 확인하세요.")