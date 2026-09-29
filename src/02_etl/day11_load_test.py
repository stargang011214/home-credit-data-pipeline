import pandas as pd
from sqlalchemy import create_engine

# 1. 파일에서 소량의 데이터(10건)만 잘라서 가져오기
file_path = r'C:\Users\User\Downloads\home-credit-default-risk\application_train.csv'
df = next(pd.read_csv(file_path, chunksize=10))
print("1. 데이터 10건 추출 완료")

# 2. DB 연결 (커넥션) 설정
# (가벼운 테스트를 위해 파이썬 내장 가상 DB인 SQLite를 사용해 통로를 뚫습니다)
db_url = 'sqlite:///test_etl.db'
engine = create_engine(db_url)
print("2. 🔌 DB 커넥션(통로) 연결 완료!")

# 3. DB에 데이터 적재 (Insert)
# 판다스의 to_sql 기능을 쓰면 10건의 데이터가 한 번에 DB 테이블로 쏙 들어갑니다.
table_name = 'application_train_test'
df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

print(f"3. 🚀 성공적으로 {len(df)}건의 데이터를 '{table_name}' 테이블에 적재했습니다!")