import pandas as pd

# 파일 이름 (컴퓨터가 헤매지 않도록 정확한 전체 주소 입력)
file_path = r'C:\Users\User\Downloads\home-credit-default-risk\application_train.csv'

# 1. 한 번에 다 부르지 않고, 1만 건씩 썰어서 읽어올 준비 (chunksize)
chunk_size = 10000
chunk_iterator = pd.read_csv(file_path, chunksize=chunk_size)

# 2. 썰어둔 조각 중 맨 첫 번째 조각(1만 건)만 가져오기
first_chunk = next(chunk_iterator)

# 3. 데이터가 무사히 들어왔는지 크기와 형태 확인
print("성공! 첫 번째 조각의 데이터 크기(행, 열):", first_chunk.shape)
print("\n데이터 첫 5줄 미리보기:")
print(first_chunk.head())