CREATE TABLE publication (
    pub_id VARCHAR2(30) PRIMARY KEY,
    title VARCHAR2(500),
    summary CLOB,
    category VARCHAR2(100),
    publication_type VARCHAR2(50),
    published_date DATE,
    updated_date DATE,
    first_author VARCHAR2(100)
);
SELECT COUNT(*) FROM publication;
SELECT * FROM publication FETCH FIRST 5 ROWS ONLY;

CREATE TABLE faculty (
    faculty_id NUMBER PRIMARY KEY,
    name VARCHAR2(100),
    email VARCHAR2(100),
    department VARCHAR2(50)
);
SELECT COUNT(*) FROM faculty;
SELECT * FROM faculty FETCH FIRST 5 ROWS ONLY;

CREATE TABLE student (
    student_id NUMBER PRIMARY KEY,
    name VARCHAR2(100),
    email VARCHAR2(100),
    program VARCHAR2(50)
);
SELECT COUNT(*) FROM student;
SELECT * FROM student FETCH FIRST 5 ROWS ONLY;

CREATE TABLE publication_authors (
    pub_id VARCHAR2(20),
    author_id NUMBER,
    author_type VARCHAR2(10) CHECK (author_type IN ('faculty', 'student')),
    PRIMARY KEY (pub_id, author_id),
    FOREIGN KEY (pub_id) REFERENCES publication(pub_id)
);
SELECT COUNT(*) FROM publication_authors;
SELECT * FROM publication_authors FETCH FIRST 5 ROWS ONLY;


CREATE TABLE users (
    user_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR2(50) UNIQUE NOT NULL,
    role VARCHAR2(10) CHECK (role IN ('student', 'faculty')),
    email VARCHAR2(100) UNIQUE NOT NULL
);

-- Faculty users
INSERT INTO users (username, role, email) VALUES ('akumar', 'faculty', 'akumar@univ.edu');
INSERT INTO users (username, role, email) VALUES ('lmehta', 'faculty', 'lmehta@univ.edu');

-- Student users
INSERT INTO users (username, role, email) VALUES ('rjain', 'student', 'rohit.j@univ.edu');
INSERT INTO users (username, role, email) VALUES ('nverma', 'student', 'neha.v@univ.edu');

COMMIT;

SELECT COUNT(*) FROM users;
SELECT * FROM users;

-- Link users to faculty and student tables

ALTER TABLE faculty ADD user_id NUMBER REFERENCES users(user_id);
ALTER TABLE student ADD user_id NUMBER REFERENCES users(user_id);

UPDATE faculty SET user_id = (SELECT user_id FROM users WHERE username = 'akumar') WHERE name = 'Dr. A. Kumar';
UPDATE student SET user_id = (SELECT user_id FROM users WHERE username = 'rjain') WHERE name = 'Rohit Jain';

SELECT u.username, p.title
FROM users u
JOIN publication_authors pa ON u.user_id = pa.author_id
JOIN publication p ON pa.pub_id = p.pub_id
WHERE u.role = 'faculty';


CREATE TABLE publication_status_log (
    log_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    pub_id VARCHAR2(30),
    old_status VARCHAR2(20),
    new_status VARCHAR2(20),
    changed_on DATE DEFAULT SYSDATE
);

SELECT COUNT(*) FROM publication_status_log;
SELECT * FROM publication_status_log FETCH FIRST 2 ROWS ONLY;

/* add_publication — Insert New Publication */

CREATE OR REPLACE PROCEDURE add_publication (
    p_pub_id VARCHAR2,
    p_title VARCHAR2,
    p_summary VARCHAR2,
    p_category VARCHAR2,
    p_type VARCHAR2,
    p_pub_date DATE
)
IS
BEGIN
    INSERT INTO publication (
        pub_id, title, summary, category, publication_type, published_date, updated_date
    )
    VALUES (
        p_pub_id, p_title, p_summary, p_category, p_type, p_pub_date, SYSDATE
    );

    DBMS_OUTPUT.PUT_LINE('✔️ Publication added successfully');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('❌ Error: ' || SQLERRM);
END;
/
/* assign_author — Link Author to a Publication */

CREATE OR REPLACE PROCEDURE assign_author (
    p_pub_id VARCHAR2,
    p_author_id NUMBER,
    p_author_type VARCHAR2
)
IS
BEGIN
    INSERT INTO publication_authors (pub_id, author_id, author_type)
    VALUES (p_pub_id, p_author_id, p_author_type);

    DBMS_OUTPUT.PUT_LINE('✔️ Author linked to publication');
EXCEPTION
    WHEN DUP_VAL_ON_INDEX THEN
        DBMS_OUTPUT.PUT_LINE('⚠️ Author already assigned');
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('❌ Error: ' || SQLERRM);
END;
/
DESC assign_author;
DESC publication;
ALTER TABLE publication ADD status VARCHAR2(20);

/* update_publication_status — Change Submission Status */

CREATE OR REPLACE PROCEDURE update_publication_status (
    p_pub_id VARCHAR2,
    p_status VARCHAR2
)
IS
    v_old_status VARCHAR2(20);
BEGIN
    -- 1. Get the current status before update
    SELECT status INTO v_old_status
    FROM publication
    WHERE pub_id = p_pub_id;

    -- 2. Update the publication status
    UPDATE publication
    SET status = p_status
    WHERE pub_id = p_pub_id;

    -- 3. Log the change
    INSERT INTO publication_status_log (pub_id, old_status, new_status)
    VALUES (p_pub_id, v_old_status, p_status);

    DBMS_OUTPUT.PUT_LINE('✔️ Status updated and logged successfully.');
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('❌ Error: Publication ID not found.');
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('❌ Unexpected Error: ' || SQLERRM);
END;
/
DESC update_publication_status;
BEGIN
    update_publication_status('cs-0011v1', 'Published');
END;
DESC update_publication_status;
/* Trigger for Auto-updating updated_date */

CREATE OR REPLACE TRIGGER trg_auto_update
BEFORE UPDATE ON publication
FOR EACH ROW
BEGIN
    :NEW.updated_date := SYSDATE;
END;
/
/* Function — Get Publications by Author */

CREATE OR REPLACE FUNCTION get_publications_by_author (
    p_author_id NUMBER
)
RETURN SYS_REFCURSOR
IS
    pub_cursor SYS_REFCURSOR;
BEGIN
    OPEN pub_cursor FOR
    SELECT p.pub_id, p.title, p.category, p.status
    FROM publication p
    JOIN publication_authors pa ON p.pub_id = pa.pub_id
    WHERE pa.author_id = p_author_id;

    RETURN pub_cursor;
END;
/
/* Testing */

BEGIN
    add_publication('cs-0011v1', 'Quantum NLP', 'AI meets quantum.', 'AI', 'Journal', TO_DATE('2024-01-15', 'YYYY-MM-DD'));
    assign_author('cs-0011v1', 2, 'faculty');
    update_publication_status('cs-0011v1', 'Accepted');
END;
