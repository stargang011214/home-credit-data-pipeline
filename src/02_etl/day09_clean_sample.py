import pandas as pd

# 1. 어제 썼던 절대 경로 그대로 사용 (경로 앞에 r 붙이기!)
file_path = r'C:\Users\User\Downloads\home-credit-default-risk\application_train.csv'

# 1만 건만 잘라서 가져오기
df = next(pd.read_csv(file_path, chunksize=10000))
print("✨ 데이터 정제(Cleaning) 시작!\n")

# 데이터 중에서 글자(문자열)가 들어있는 기둥(컬럼)들만 골라내기
str_cols = df.select_dtypes(include=['object']).columns

# 2. 결측치(빈칸) 처리 로직
# 데이터에 텅 비어있는 칸(NaN)이 있다면 'Unknown(알수없음)'이라는 글자로 예쁘게 채워넣기
df[str_cols] = df[str_cols].fillna('Unknown')

# 3. 공백 제거 로직
# 글자 앞뒤에 실수로 들어간 띄어쓰기(스페이스바) 싹둑 자르기 (strip 기능)
for col in str_cols:
    df[col] = df[col].astype(str).str.strip()

print("🧹 1단계 정제 완료! 텍스트 데이터의 빈칸과 공백 처리가 끝났습니다.")
print("\n[정제된 텍스트 데이터 첫 5줄 미리보기]")
print(df[str_cols].head())

# 4. 날짜/시간 데이터 표준화 (Home Credit 데이터 특성 반영)
# 태어난 날(DAYS_BIRTH)이 마이너스(-) 일수로 되어 있는 것을 '나이(연도)'로 변환
df['AGE'] = (df['DAYS_BIRTH'] / -365).astype(int)

print("\n📅 2단계 정제 완료! 마이너스 일수 데이터를 알아보기 쉬운 '나이(AGE)'로 변환했습니다.")
print("[변환된 나이 데이터 첫 5줄 확인]")
print(df[['DAYS_BIRTH', 'AGE']].head())