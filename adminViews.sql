/* Creating Views */

/*Publications by Faculty*/
CREATE OR REPLACE VIEW faculty_publications AS
SELECT 
    f.name AS faculty_name,
    f.department,
    p.title,
    p.category,
    p.status,
    p.published_date
FROM faculty f
JOIN publication_authors pa ON f.faculty_id = pa.author_id
JOIN publication p ON pa.pub_id = p.pub_id
WHERE pa.author_type = 'faculty';

SELECT * FROM faculty_publications;

/* Publications by Student */
CREATE OR REPLACE VIEW student_publications AS
SELECT s.name AS student_name, s.program, p.title, p.category, p.status, p.published_date
FROM student s
JOIN publication_authors pa ON s.student_id = pa.author_id
JOIN publication p ON pa.pub_id = p.pub_id
WHERE pa.author_type = 'student';

-- Total publications by category
SELECT category, COUNT(*) FROM publication GROUP BY category;
-- Publications by faculty
SELECT * FROM faculty_publications WHERE department = 'CSE';
-- Recently updated publications
SELECT title, updated_date FROM publication ORDER BY updated_date DESC;

CREATE OR REPLACE VIEW publications_by_year AS
SELECT 
    EXTRACT(YEAR FROM published_date) AS year,
    COUNT(*) AS total_publications
FROM publication
GROUP BY EXTRACT(YEAR FROM published_date)
ORDER BY year;

SELECT * FROM publications_by_year;

CREATE OR REPLACE VIEW faculty_publications_by_year AS
SELECT 
    f.name AS faculty_name,
    EXTRACT(YEAR FROM p.published_date) AS year,
    COUNT(*) AS total_pubs
FROM faculty f
JOIN publication_authors pa ON f.faculty_id = pa.author_id
JOIN publication p ON pa.pub_id = p.pub_id
WHERE pa.author_type = 'faculty'
GROUP BY f.name, EXTRACT(YEAR FROM p.published_date)
ORDER BY f.name, year;

SELECT * FROM faculty_publications_by_year;
SELECT * FROM publication_status_log;

CREATE OR REPLACE VIEW publications_by_year AS
SELECT EXTRACT(YEAR FROM p.published_date) AS publication_year, COUNT(*) AS publication_count
FROM publication p
WHERE p.published_date IS NOT NULL
GROUP BY EXTRACT(YEAR FROM p.published_date)
ORDER BY publication_year;

-- Views for Enhanced Reporting

-- student_publications_by_year View
CREATE OR REPLACE VIEW student_publications_by_year AS
SELECT 
    s.name AS student_name,
    EXTRACT(YEAR FROM p.published_date) AS year,
    COUNT(*) AS total_pubs
FROM student s
JOIN publication_authors pa ON s.student_id = pa.author_id
JOIN publication p ON pa.pub_id = p.pub_id
WHERE pa.author_type = 'student'
GROUP BY s.name, EXTRACT(YEAR FROM p.published_date)
ORDER BY s.name, year;
SELECT * FROM student_publications_by_year ORDER BY total_pubs DESC;

CREATE OR REPLACE VIEW yearly_faculty_student_pubs AS
SELECT 
    EXTRACT(YEAR FROM p.published_date) AS year,
    SUM(CASE WHEN pa.author_type = 'faculty' THEN 1 ELSE 0 END) AS faculty_count,
    SUM(CASE WHEN pa.author_type = 'student' THEN 1 ELSE 0 END) AS student_count
FROM publication_authors pa
JOIN publication p ON pa.pub_id = p.pub_id
GROUP BY EXTRACT(YEAR FROM p.published_date);

-- top_contributing_faculty View
CREATE OR REPLACE VIEW top_contributing_faculty AS
SELECT 
    f.name AS faculty_name,
    COUNT(*) AS total_publications
FROM faculty f
JOIN publication_authors pa ON f.faculty_id = pa.author_id
WHERE pa.author_type = 'faculty'
GROUP BY f.name
ORDER BY total_publications DESC;
SELECT * from top_contributing_faculty;
-- recent_publications View
CREATE OR REPLACE VIEW recent_publications AS
SELECT 
    p.title,
    p.published_date,
    p.category,
    p.status
FROM publication p
WHERE p.published_date >= SYSDATE - 30
ORDER BY p.published_date DESC;

SELECT view_name FROM user_views;
DESC student_publications_by_year;
DESC top_contributing_faculty;
DESC recent_publications;

SELECT * FROM student_publications_by_year;
SELECT * FROM top_contributing_faculty;
SELECT * FROM recent_publications;
SELECT category, COUNT(*) AS count FROM publication GROUP BY category


