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