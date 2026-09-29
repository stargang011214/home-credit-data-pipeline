import pandas as pd
from sqlalchemy import create_engine

# 1. DB 연결 및 원본 파일 경로 설정
engine = create_engine('sqlite:///C:/Users/User/Downloads/test_etl.db')
file_path = r'C:\Users\User\Downloads\home-credit-default-risk\application_train.csv'

# 2. 원본(CSV)과 DB 데이터 읽어오기 (비교에 필요한 ID와 대출 금액만 쏙 뽑아옵니다)
print("데이터를 불러오고 대조하는 중입니다. 잠시만 기다려주세요...")
df_csv = pd.read_csv(file_path, usecols=['SK_ID_CURR', 'AMT_CREDIT'])
df_db = pd.read_sql("SELECT SK_ID_CURR, AMT_CREDIT FROM application_train_final", con=engine)

# 3. 소수점 오차 방지를 위해 2자리까지 반올림
df_csv['AMT_CREDIT'] = df_csv['AMT_CREDIT'].round(2)
df_db['AMT_CREDIT'] = df_db['AMT_CREDIT'].round(2)

# 4. 데이터 병합 (Merge)을 통한 1:1 정밀 대조
# ID를 기준으로 원본과 DB를 양옆으로 이어 붙입니다.
comparison = df_csv.merge(df_db, on='SK_ID_CURR', how='outer', suffixes=('_csv', '_db'), indicator=True)

# 5. 불일치 데이터 필터링 (금액이 다르거나, 한쪽에만 데이터가 있는 경우)
mismatch = comparison[
    (comparison['_merge'] != 'both') | 
    (comparison['AMT_CREDIT_csv'] != comparison['AMT_CREDIT_db'])
]

# 6. 결과 출력
print("\n🔍 [Day 19] 트러블슈팅: 불일치 원인 추적 결과")
print("-" * 60)
if mismatch.empty:
    print("✅ 트러블 데이터 0건: CSV 원본과 DB 적재 데이터가 행 단위로 100% 완벽히 일치합니다!")
else:
    print(f"❌ 불일치 또는 누락 데이터 {len(mismatch):,}건 발견!")
    print("아래는 문제가 발생한 데이터의 상세 내역입니다 (상위 5건):")
    print(mismatch.head())
print("-" * 60)