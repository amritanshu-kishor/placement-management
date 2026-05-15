-- Placement Management System (MySQL / MariaDB)
-- Create the database once in your client, then run this file against it:
--   CREATE DATABASE placement_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
--   USE placement_db;

SET NAMES utf8mb4;

CREATE TABLE IF NOT EXISTS students (
    student_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    roll_no VARCHAR(32) NOT NULL,
    full_name VARCHAR(160) NOT NULL,
    email VARCHAR(160) NOT NULL,
    department VARCHAR(120) NOT NULL,
    cgpa DECIMAL(4,2) NOT NULL,
    phone VARCHAR(32) NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (student_id),
    UNIQUE KEY uq_students_roll (roll_no),
    UNIQUE KEY uq_students_email (email),
    CONSTRAINT chk_students_cgpa CHECK (cgpa >= 0 AND cgpa <= 10)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS companies (
    company_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(160) NOT NULL,
    sector VARCHAR(120) NULL,
    headquarters VARCHAR(160) NULL,
    website VARCHAR(255) NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (company_id),
    UNIQUE KEY uq_companies_name (name)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS jobs (
    job_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    company_id INT UNSIGNED NOT NULL,
    role_title VARCHAR(160) NOT NULL,
    job_type VARCHAR(40) NOT NULL DEFAULT 'Full-time',
    package_lpa DECIMAL(8,2) NOT NULL,
    min_cgpa DECIMAL(4,2) NOT NULL DEFAULT 0,
    openings INT UNSIGNED NOT NULL DEFAULT 1,
    deadline DATE NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (job_id),
    CONSTRAINT fk_jobs_company FOREIGN KEY (company_id)
        REFERENCES companies (company_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT chk_jobs_package CHECK (package_lpa >= 0),
    CONSTRAINT chk_jobs_min_cgpa CHECK (min_cgpa >= 0 AND min_cgpa <= 10),
    CONSTRAINT chk_jobs_openings CHECK (openings >= 0)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS applications (
    application_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    student_id INT UNSIGNED NOT NULL,
    job_id INT UNSIGNED NOT NULL,
    status ENUM('Applied','Shortlisted','Interview','Offer','Rejected') NOT NULL DEFAULT 'Applied',
    applied_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (application_id),
    UNIQUE KEY uq_app_student_job (student_id, job_id),
    KEY idx_apps_status (status),
    CONSTRAINT fk_apps_student FOREIGN KEY (student_id)
        REFERENCES students (student_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_apps_job FOREIGN KEY (job_id)
        REFERENCES jobs (job_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- InnoDB already maintains indexes required by foreign keys (e.g. jobs.company_id,
-- applications.job_id). Extra CREATE INDEX on those columns duplicates names on
-- re-run and cannot be dropped (Error 1553) while the FK exists.
