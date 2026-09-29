-- ============================================================
-- 데이터 정합성 검증 쿼리 모음
-- 대상 테이블: application_train_final (SQLite / test_etl.db)
-- 기준 데이터: application_train.csv (307,511건)
-- ============================================================


-- ------------------------------------------------------------
-- [Day 15] 건수 검증
-- 목적: 적재 과정에서 데이터가 유실되거나 중복 적재되지 않았는지 확인
-- 기대값: 원본 CSV 건수(307,511)와 동일
-- 실제결과: 307,511건 (일치)
-- ------------------------------------------------------------
SELECT COUNT(*) AS db_row_count
FROM application_train_final;


-- ------------------------------------------------------------
-- [Day 16] 수치 합계 검증
-- 목적: 건수는 일치하더라도 값이 절삭·변조되지 않았는지 확인
--       (타입 변환 과정의 반올림·소수점 손실 탐지)
-- 기대값: 원본 CSV의 AMT_CREDIT 합계와 동일
-- 실제결과: 184,207,084,195.50 (일치)
-- ------------------------------------------------------------
SELECT ROUND(SUM(AMT_CREDIT), 2) AS total_amt_credit
FROM application_train_final;


-- ------------------------------------------------------------
-- [Day 17] 참조 무결성 / 고아 데이터 검증
-- 목적: 식별자가 비어 있는 행(부모 없는 데이터)이 존재하는지 확인
-- 기대값: 0건
-- 실제결과: 0건
-- ------------------------------------------------------------
SELECT COUNT(*) AS orphan_count
FROM application_train_final
WHERE SK_ID_CURR IS NULL;

-- 참고: 부모/자식 테이블이 분리된 환경에서의 일반적인 FK 검증 패턴
-- SELECT COUNT(*)
-- FROM   child  c
-- LEFT   JOIN parent p ON c.fk = p.pk
-- WHERE  p.pk IS NULL;


-- ------------------------------------------------------------
-- [Day 18-1] PK 중복 검증
-- 목적: 기본키로 사용할 SK_ID_CURR에 중복 값이 없는지 확인
-- 기대값: 0건
-- 실제결과: 0건
-- ------------------------------------------------------------
SELECT COUNT(*) AS duplicate_pk_count
FROM (
    SELECT SK_ID_CURR
    FROM   application_train_final
    GROUP  BY SK_ID_CURR
    HAVING COUNT(SK_ID_CURR) > 1
);


-- ------------------------------------------------------------
-- [Day 18-2] 필수 컬럼(Not Null) 누락 검증
-- 목적: 필수값인 식별자에 NULL이 존재하는지 확인
-- 기대값: 0건
-- 실제결과: 0건
-- ------------------------------------------------------------
SELECT COUNT(*) AS null_pk_count
FROM application_train_final
WHERE SK_ID_CURR IS NULL;


-- ------------------------------------------------------------
-- [Day 19] 행 단위 전수 대조 (원본 CSV ↔ DB)
-- 목적: 집계 검증으로는 잡히지 않는 '값 뒤바뀜'까지 탐지
--       (두 레코드의 값이 서로 교환되면 건수·합계는 동일하게 유지됨)
-- 방식: 원본 CSV를 pandas로 읽어 SK_ID_CURR 기준 outer merge 후
--       AMT_CREDIT 값까지 1:1 비교 → src/03_validation/day19_troubleshooting.py 참고
-- 실제결과: 307,511건 전수 일치, 불일치 0건
--
-- 아래는 원본 데이터를 스테이징 테이블(application_train_source)로
-- 적재했을 경우 동일한 검증을 SQL만으로 수행하는 쿼리입니다.
-- ------------------------------------------------------------
-- SELECT COUNT(*) AS mismatch_count
-- FROM        application_train_source s
-- FULL OUTER  JOIN application_train_final f ON s.SK_ID_CURR = f.SK_ID_CURR
-- WHERE       s.SK_ID_CURR IS NULL
--          OR f.SK_ID_CURR IS NULL
--          OR ROUND(s.AMT_CREDIT, 2) <> ROUND(f.AMT_CREDIT, 2);


-- ------------------------------------------------------------
-- [참고] 컬럼별 결측치 현황 조회 (테이블 정의서 작성에 사용)
-- ------------------------------------------------------------
SELECT
    COUNT(*)                                                   AS total_rows,
    SUM(CASE WHEN OWN_CAR_AGE   IS NULL THEN 1 ELSE 0 END)     AS null_own_car_age,
    SUM(CASE WHEN EXT_SOURCE_1  IS NULL THEN 1 ELSE 0 END)     AS null_ext_source_1,
    SUM(CASE WHEN OCCUPATION_TYPE IS NULL THEN 1 ELSE 0 END)   AS null_occupation_type
FROM application_train_final;


-- ------------------------------------------------------------
-- [참고] DAYS_EMPLOYED 이상치 현황 (미처리 상태로 문서에 기록)
-- 결과: 365243 값이 55,374건 (전체의 약 18%)
-- ------------------------------------------------------------
SELECT
    DAYS_EMPLOYED,
    COUNT(*) AS cnt
FROM   application_train_final
WHERE  DAYS_EMPLOYED = 365243
GROUP  BY DAYS_EMPLOYED;
