import pandas as pd
from sqlalchemy import create_engine
import time
import logging

# 1. 로깅(Logging) 설정: print 대신 전문적인 기록장(Log)을 사용하기 위한 세팅
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

file_path = r'C:\Users\User\Downloads\home-credit-default-risk\application_train.csv'
engine = create_engine('sqlite:///test_etl.db')
table_name = 'application_train_safe' # 안전하게 넣을 새로운 테이블

logging.info("🚀 안전한 대용량 Batch 적재(방어막 가동)를 시작합니다...")
start_time = time.time()

chunk_size = 50000
chunk_iter = pd.read_csv(file_path, chunksize=chunk_size)

# 2. 데이터를 5만 건씩 밀어 넣는 반복문
for i, chunk in enumerate(chunk_iter):
    try:
        # [Try 블록] 일단 평소처럼 DB에 적재를 '시도'해 봅니다.
        if i == 0:
            chunk.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
        else:
            chunk.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        
        # 성공하면 INFO 로그를 남깁니다.
        logging.info(f"✔️ {i + 1}번째 상자 ({len(chunk)}건) 정상 적재 완료!")
        
    except Exception as e:
        # [Except 블록] 만약 위 과정에서 에러가 터지면 프로그램이 꺼지는 대신 여기로 빠집니다!
        logging.error(f"❌ {i + 1}번째 상자 적재 중 에러 발생! 건너뛰고 다음으로 넘어갑니다.")
        logging.error(f"🔍 에러 원인: {e}")
        # (실무에서는 여기서 에러가 난 chunk만 따로 '에러_데이터.csv' 파일로 저장해두고 나중에 분석합니다.)

end_time = time.time()
logging.info(f"🎉 전체 데이터 적재(안전 모드)가 완료되었습니다! 총 소요 시간: {end_time - start_time:.2f}초")