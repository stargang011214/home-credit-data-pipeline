# 1. 엑셀을 다루는 파이썬의 핵심 도구 'pandas'를 불러옵니다.
import pandas as pd

# 2. 대장 파일인 application_train.csv 파일을 읽어와서 'df'라는 이름의 데이터 상자에 담습니다.
df = pd.read_csv('application_train.csv')

# 3. 데이터 상자(df)의 뼈대가 어떻게 생겼는지 확인합니다.
print("=== 1. 데이터의 뼈대 (행과 열의 개수) ===")
print(df.shape) 

# 4. 어떤 기둥(컬럼)들이 있는지 목록을 쭉 뽑아봅니다.
print("\n=== 2. 컬럼(기둥) 이름 목록 ===")
print(df.columns.tolist())
# 5. 데이터의 상위 5줄을 엑셀 표처럼 살짝 엿봅니다.
print("\n=== 3. 데이터 미리보기 (상위 5줄) ===")
print(df.head())

# 6. 컬럼들에 빈칸(결측치)이 얼마나 있는지, 숫자/글자 타입은 무엇인지 요약해 봅니다.
print("\n=== 4. 데이터 기본 정보 요약 ===")
df.info()
# 7. 결측치(빈칸)가 많은 컬럼 상위 10개 확인하기
print("\n=== 5. 결측치(빈칸) TOP 10 ===")
missing_values = df.isnull().sum()
print(missing_values[missing_values > 0].sort_values(ascending=False).head(10))
# 8. 'ID' 글자가 포함된 기둥(컬럼) 이름만 쏙 뽑아보기
print("\n=== 6. 테이블 연결고리(Key) 후보 찾기 ===")
id_cols = [col for col in df.columns if 'ID' in col]
print(id_cols)
# 9. 마스터키(SK_ID_CURR)에 중복된 값이 없는지 검증합니다.
print("\n=== 7. 마스터키 중복 검사 ===")
total_rows = len(df)
unique_ids = df['SK_ID_CURR'].nunique()
print(f"전체 데이터(행) 수: {total_rows}")
print(f"고유한 ID의 수: {unique_ids}")

if total_rows == unique_ids:
    print("=> 완벽합니다! 중복된 ID가 하나도 없는 훌륭한 Primary Key입니다.")
else:
    print("=> 앗, 중복된 ID가 존재합니다. 전처리가 필요합니다.")
    # 10. 데이터 사전(설명서) 파일에서 특정 단어의 뜻 검색하기
print("\n=== 8. 데이터 사전 검색: DAYS_ID_PUBLISH ===")

# 설명서 파일은 글자 깨짐 방지를 위해 특별한 옵션(encoding)을 넣어줍니다.
desc_df = pd.read_csv('HomeCredit_columns_description.csv', encoding='cp1252')

# 설명서의 'Row'(컬럼명) 항목에서 우리가 찾는 단어와 똑같은 줄만 쏙 뽑아냅니다.
search_result = desc_df[desc_df['Row'] == 'DAYS_ID_PUBLISH']

# 찾은 뜻(Description)을 화면에 깔끔하게 출력합니다.
for text in search_result['Description']:
    print(f"💡 뜻: {text}")
    # 11. 다른 기관의 대출 기록 파일(bureau.csv)을 읽어옵니다.
print("\n=== 9. bureau.csv (타 기관 대출 기록) 뼈대 확인 ===")
bureau_df = pd.read_csv('bureau.csv')
print("bureau 데이터 크기(행, 열):", bureau_df.shape)

# 12. 두 테이블을 엮어줄 연결 고리가 있는지 확인합니다.
print("\n=== 10. 테이블 연결 고리(Foreign Key) 확인 ===")
bureau_id_cols = [col for col in bureau_df.columns if 'ID' in col]
print(f"bureau.csv에 있는 ID 기둥들: {bureau_id_cols}")

if 'SK_ID_CURR' in bureau_df.columns:
    print("=> 빙고! SK_ID_CURR 기둥이 존재합니다. 메인 테이블과 완벽하게 연결할 수 있습니다!")