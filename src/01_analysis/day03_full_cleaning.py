import pandas as pd

print("=== Day 3: 데이터 전처리 준비 ===")
# 메인 고객 명부 데이터를 불러옵니다.
df = pd.read_csv('application_train.csv')
print("✅ 데이터 불러오기 완료! 현재 데이터 크기:", df.shape)
# 1. 빈칸(결측치)이 너무 많은 부실한 기둥 찾아내기
print("\n=== 1. 빈칸 50% 이상 기둥 쳐내기 ===")

# 각 기둥마다 빈칸이 몇 퍼센트나 되는지 계산합니다.
missing_ratio = df.isnull().sum() / len(df)

# 빈칸이 50%(0.5) 이상인 기둥들의 이름만 쏙 뽑아냅니다.
cols_to_drop = missing_ratio[missing_ratio >= 0.5].index
print(f"삭제될 부실한 기둥 개수: {len(cols_to_drop)}개")

# 해당 기둥들을 데이터 도화지에서 완전히 지워버립니다.
df = df.drop(columns=cols_to_drop)
print("✅ 다이어트 완료! 현재 데이터 크기:", df.shape)
# 2. 남은 빈칸(결측치) 안전하게 채워 넣기
print("\n=== 2. 남은 빈칸 안전하게 메우기 ===")

# 숫자형 기둥과 글자형 기둥의 이름을 각각 따로 모아줍니다.
numeric_cols = df.select_dtypes(include=['number']).columns
text_cols = df.select_dtypes(include=['object']).columns

# 숫자형 기둥의 빈칸은 해당 기둥의 '중간값(median)'으로 쏙쏙 채웁니다.
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

# 글자형 기둥의 빈칸은 'Unknown(미상)'이라는 글자로 통일해서 채웁니다.
df[text_cols] = df[text_cols].fillna('Unknown')

# 빈칸이 정말 하나도 남지 않았는지 최종 확인!
total_missing = df.isnull().sum().sum()
print(f"✅ 남은 빈칸 총 개수: {total_missing}개 (완벽합니다!)")
# 3. DB 입장을 위한 최종 복장(Data Type) 검사
print("\n=== 3. 최종 데이터 타입(Type) 점검 ===")

# 각 기둥의 데이터 타입이 무엇인지 목록을 뽑아봅니다.
print(df.dtypes.value_counts())

# 만약 글자(object) 데이터가 있다면, 나중에 텍스트로 잘 들어가게 변환해 둡니다.
df[text_cols] = df[text_cols].astype(str)
print("✅ DB 적재를 위한 모든 준비가 완료되었습니다!")
# 4. 청소가 끝난 깨끗한 데이터를 새로운 CSV 파일로 영구 저장합니다.
df.to_csv('application_train_cleaned.csv', index=False)
print("💾 청소 완료된 데이터가 'application_train_cleaned.csv'로 저장되었습니다!")