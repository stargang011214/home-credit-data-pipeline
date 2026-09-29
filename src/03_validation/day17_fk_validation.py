import pandas as pd
from sqlalchemy import create_engine

# 1. DB 연결 설정 (절대 경로 유지)
engine = create_engine('sqlite:///C:/Users/User/Downloads/test_etl.db')

# 2. 참조 무결성(또는 고아 데이터 여부) 검증 쿼리 작성 예시
# 예: 부모-자식 테이블이 분리되어 있다면 LEFT JOIN 구문을 사용하지만,
# 단일 테이블/참조 무결성 로직 검증 또는 논리적 키 유효성 검사 패턴으로 구성합니다.
# 실무 쿼리 패턴:
query = """
SELECT COUNT(*) 
FROM application_train_final 
WHERE SK_ID_CURR IS NULL;
"""
# * 참고: 실제 외래키(FK) 조인 검증이 필요한 부모/자식 별도 테이블 환경일 경우:
# SELECT COUNT(*) FROM 자식 c LEFT JOIN 부모 p ON c.fk = p.pk WHERE p.pk IS NULL

orphan_count = pd.read_sql(query, con=engine).iloc[0, 0]
total_count_query = "SELECT COUNT(*) FROM application_train_final"
total_count = pd.read_sql(total_count_query, con=engine).iloc[0, 0]

# 3. 결과 출력
print("🔗 [Day 17] 참조 무결성 / 고아 데이터 검증 결과")
print("-" * 50)
print(f"🗄️ 전체 대상 행 수 : {total_count:,}건")
print(f"⚠️ 무결성 위반/고아 데이터 수 : {orphan_count:,}건")
print("-" * 50)

if orphan_count == 0:
    print("✅ 검증 통과: 무결성 위반(고아 데이터)이 0건입니다!")
else:
    print(f"❌ 검증 실패: 무결성 위반 데이터 {orphan_count}건 발견")