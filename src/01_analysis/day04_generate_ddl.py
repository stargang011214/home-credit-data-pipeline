import pandas as pd

print("=== Day 4: 데이터베이스 설계도(SQL) 뼈대 만들기 ===")

# 1. Day 3에서 정성껏 청소한 깨끗한 데이터를 불러옵니다.
df = pd.read_csv('application_train_cleaned.csv')
print("✅ 깨끗한 데이터 불러오기 완료!\n")

# 2. 파이썬의 데이터 타입을 DB(PostgreSQL) 언어로 번역해 주는 사전(Dictionary)입니다.
type_mapping = {
    'int64': 'INTEGER',
    'float64': 'NUMERIC',
    'object': 'VARCHAR(255)',
    'str': 'VARCHAR(255)'
}

# 3. SQL 설계도(CREATE TABLE) 작성을 시작합니다!
table_name = "application_train"
sql_lines = [f"CREATE TABLE {table_name} ("]

# 4. 81개의 기둥(컬럼)을 하나씩 돌면서 SQL 문장으로 조립합니다.
for col_name, dtype in df.dtypes.items():
    # 파이썬 타입을 DB 타입으로 번역
    sql_type = type_mapping.get(str(dtype), 'VARCHAR(255)')
    
    # Day 2에서 찾은 마스터키(Primary Key)에 왕관을 씌워줍니다!
    if col_name == 'SK_ID_CURR':
        sql_lines.append(f"    {col_name} {sql_type} PRIMARY KEY,")
    else:
        sql_lines.append(f"    {col_name} {sql_type},")

# 맨 마지막 줄의 쉼표(,)를 없애고 괄호를 닫아줍니다.
sql_lines[-1] = sql_lines[-1].rstrip(',')
sql_lines.append(");")

# 5. 완성된 도면의 상위 10줄만 살짝 엿보기
print("[ 🏗️ 완성된 SQL 설계도 미리보기 (상위 10줄) ]")
for line in sql_lines[:10]:
    print(line)
print("    ... (이하 생략) ...")
# 6. 완성된 도면을 실제 SQL 파일로 저장합니다.
with open('schema.sql', 'w') as f:
    f.write("\n".join(sql_lines))
print("💾 완벽한 DB 설계도가 'schema.sql' 파일로 저장되었습니다! (Day 4 미션 클리어!)")
# ==========================================
# 💎 [보너스] 제3정규화(3NF) 맛보기: 학력(Education) 테이블 분리하기
print("\n=== 💎 [보너스] 제3정규화(3NF) 테이블 쪼개기 ===")

# 1. 메인 테이블에서 '학력' 종류만 중복 없이 쏙 뽑아냅니다.
edu_types = df['NAME_EDUCATION_TYPE'].unique()

# 2. 뽑아낸 학력들에 1번, 2번, 3번... ID(PK) 번호를 붙여서 '새로운 코드 테이블'을 만듭니다.
edu_table = pd.DataFrame({
    'EDU_ID': range(1, len(edu_types) + 1), # 1부터 번호 매기기 (새로운 PK)
    'EDUCATION_NAME': edu_types             # 원래 텍스트 (대졸, 고졸 등)
})

print("\n[ 쪼개져 나온 '학력 코드' 테이블 (부모) ]")
print(edu_table)

# 3. 이제 30만 줄짜리 메인 테이블의 글자들을 ID 번호(FK)로 싹 바꿔치기 합니다.
# (edu_table을 딕셔너리로 만들어서 메인 테이블에 매핑 적용)
edu_mapping = dict(zip(edu_table['EDUCATION_NAME'], edu_table['EDU_ID']))
df['NAME_EDUCATION_TYPE'] = df['NAME_EDUCATION_TYPE'].map(edu_mapping)

print("\n[ 글자가 번호(FK)로 바뀐 메인 테이블 (상위 5명) ]")
print(df[['SK_ID_CURR', 'NAME_EDUCATION_TYPE']].head())
print("=> 텍스트가 사라지고 숫자로 맵핑된 완벽한 제3정규화 상태입니다!")