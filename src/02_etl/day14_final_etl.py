import pandas as pd
from sqlalchemy import create_engine
import time
import logging

# 1. 관제 모니터(Logging) 세팅
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 2. 파일 경로 및 DB 연결 설정
file_path = r'C:\Users\User\Downloads\home-credit-default-risk\application_train.csv'
engine = create_engine('sqlite:///C:/Users/User/Downloads/test_etl.db')
table_name = 'application_train_final'  # 최종 적재용 테이블

logging.info("🚀 [Day 14] 최종 ETL 파이프라인 가동을 시작합니다...")
start_time = time.time()

# 3. Batch 설정 (메모리 최적화)
chunk_size = 50000
chunk_iter = pd.read_csv(file_path, chunksize=chunk_size)

# 4. 방어막을 갖춘 적재 프로세스 (try-except)
for i, chunk in enumerate(chunk_iter):
    try:
        if i == 0:
            # 첫 번째 상자: 새 테이블 만들기
            chunk.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
        else:
            # 두 번째 상자부터: 기존 테이블 밑에 이어 붙이기
            chunk.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        
        logging.info(f"✔️ {i + 1}번째 상자 ({len(chunk):,}건) 정상 적재 완료!")
        
    except Exception as e:
        logging.error(f"❌ {i + 1}번째 상자 적재 중 에러 발생! 건너뛰고 다음으로 넘어갑니다.")
        logging.error(f"🔍 에러 원인: {e}")

end_time = time.time()
logging.info(f"🎉 전체 이관 테스트 완벽 종료! 총 소요 시간: {end_time - start_time:.2f}초")