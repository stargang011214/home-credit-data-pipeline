import pandas as pd
from sqlalchemy import create_engine
import time

# 시작 시간 기록 (최적화 성능을 눈으로 확인하기 위함)
start_time = time.time()

# 1. 파일 경로 및 DB 커넥션 설정
file_path = r'C:\Users\User\Downloads\home-credit-default-risk\application_train.csv'
engine = create_engine('sqlite:///test_etl.db')
table_name = 'application_train_full'

print("🚀 30만 건 대용량 Batch 적재를 시작합니다...\n")

# 2. 데이터를 5만 건씩(chunksize) 잘라서 가져오기
chunk_size = 50000
chunk_iter = pd.read_csv(file_path, chunksize=chunk_size)

# 3. 잘라온 데이터를 순서대로 DB에 밀어넣기
for i, chunk in enumerate(chunk_iter):
    if i == 0:
        # 첫 번째 상자(0번)를 넣을 때는 기존 테이블을 싹 지우고 새로 만들기 (replace)
        chunk.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
    else:
        # 두 번째 상자부터는 기존 데이터 밑에 차곡차곡 이어 붙이기 (append)
        chunk.to_sql(name=table_name, con=engine, if_exists='append', index=False)
    
    print(f"✔️ {i + 1}번째 상자 ({len(chunk)}건) 적재 완료!")

# 종료 시간 기록 및 총 소요 시간 계산
end_time = time.time()
print(f"\n🎉 전체 데이터 적재가 완료되었습니다!")
print(f"⏱️ 총 소요 시간: {end_time - start_time:.2f}초")