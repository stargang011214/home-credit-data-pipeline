import pandas as pd

# 1. 파일 경로 설정 (어제 사용했던 절대 경로)
file_path = r'C:\Users\User\Downloads\home-credit-default-risk\application_train.csv'

# 1만 건만 잘라서 가져오기
df = next(pd.read_csv(file_path, chunksize=10000))
print("✨ Day 10: 데이터 매핑(Mapping) 시작!\n")

# [매핑 전] 원본 데이터 확인
print("1. [매핑 전] 차량 소유 여부(FLAG_OWN_CAR) 첫 5줄:")
print(df['FLAG_OWN_CAR'].head())

# 2. 비즈니스 규칙에 따른 사전(Dictionary) 만들기
# 'Y'는 1로, 'N'은 0으로 번역하라는 규칙서(매핑 테이블) 작성
mapping_rule = {'Y': 1, 'N': 0}

# 3. map() 함수를 이용해 규칙대로 한 번에 싹 변환하기
df['FLAG_OWN_CAR_MAPPED'] = df['FLAG_OWN_CAR'].map(mapping_rule)

print("\n--------------------------------------------------\n")
print("🔄 맵핑 완료! Y/N 문자가 1/0 숫자로 즉시 변환되었습니다.\n")

# [매핑 후] 변환된 데이터 비교 확인
print("2. [매핑 후] 원본과 변환된 결과 비교:")
print(df[['FLAG_OWN_CAR', 'FLAG_OWN_CAR_MAPPED']].head())