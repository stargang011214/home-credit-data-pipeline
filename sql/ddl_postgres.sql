-- ============================================================
-- PostgreSQL 정규화 스키마 (Day 5~7: 로컬 DB 구축 · DDL 작성 · 테이블 생성 점검)
-- 환경: PostgreSQL (localhost:5432) / DBeaver
-- 목적: 학력 컬럼을 코드 테이블로 분리한 제3정규화(3NF) 구조를
--       PK·FK 제약조건으로 실제 DB에 구현해 검증
-- 참고: 구조 검증용으로 핵심 컬럼만 정의했으며, 대용량 적재는 SQLite에서 수행
-- ============================================================

-- 부모 테이블: 학력 코드
CREATE TABLE education_type (
    EDUCATION_TYPE_ID INTEGER PRIMARY KEY,
    EDUCATION_NAME    VARCHAR(255)
);

-- 자식 테이블: 대출 신청 (학력은 코드 번호로 참조)
CREATE TABLE application_train (
    SK_ID_CURR             INTEGER PRIMARY KEY,
    TARGET                 INTEGER,
    AMT_INCOME_TOTAL       NUMERIC,
    NAME_EDUCATION_TYPE_ID INTEGER,
    FOREIGN KEY (NAME_EDUCATION_TYPE_ID) REFERENCES education_type(EDUCATION_TYPE_ID)
);
