-- DDL MarIA_pa Database.
-- Tabla usuarios: Registra a los usuarios de MarIA, con el telegram_user_id. Solo accede desde Telegram.
-- Tabla activities: Registra las actividades de los usuarios, con título, fecha de vencimiento, prioridad y estado. 
-- Stored Procedure sp_cleanup_completed_tasks: Elimina las actividades completadas de un usuario específico.
create database maria_pa;

CREATE TABLE users (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    telegram_user_id BIGINT UNSIGNED NOT NULL,
    `name` VARCHAR(100) NOT NULL,
    `role` ENUM(
        'ADMIN',
        'USER'
    ) NOT NULL DEFAULT 'USER',
    `status` ENUM(
        'PENDING',
        'ACTIVE',
        'DISABLED'
    ) NOT NULL DEFAULT 'PENDING',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uk_users_telegram (telegram_user_id)
);


CREATE TABLE activities (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id INT UNSIGNED NOT NULL,
    `title` VARCHAR(250) NOT NULL,
    `due_date` DATE NULL,
    `priority` ENUM('LOW', 'MEDIUM', 'URGENT') NOT NULL DEFAULT 'MEDIUM',
    `status` ENUM('PENDING','IN_PROGRESS','DONE') NOT NULL DEFAULT 'IN_PROGRESS',
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_activity_user(user_id),
    KEY idx_activity_status(status),
    KEY idx_activity_due(due_date),
    CONSTRAINT fk_activity_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);


DELIMITER $$

CREATE PROCEDURE sp_cleanup_completed_tasks()
BEGIN
    DELETE FROM activities
    WHERE status = 'DONE';
END$$

DELIMITER ;

--CALL sp_cleanup_completed_tasks(1);



INSERT INTO maria_pa.users (telegram_user_id,name,`role`,status,created_at,updated_at) VALUES
	 (5117008703,'Ernesto Cantu','ADMIN','ACTIVE','2026-07-31 16:57:22','2026-07-31 16:57:22'),
	 (6554118716,'danonina','USER','ACTIVE','2026-08-04 21:27:04','2026-08-04 21:27:41');


INSERT INTO maria_pa.activities (user_id,title,due_date,priority,status,created_at,updated_at) VALUES
	 (1,'cita visa de las chicas','2026-08-18','URGENT','IN_PROGRESS','2026-08-02 14:35:08','2026-08-04 21:42:23'),
	 (2,'Eres hermosa ❤️... att el admin','2026-08-05','URGENT','IN_PROGRESS','2026-08-02 20:51:53','2026-08-04 21:29:05'),
	 (2,'Prueba actividad adicional','2026-08-05','MEDIUM','IN_PROGRESS','2026-08-02 20:51:53','2026-08-04 21:43:04'),
	 (1,'Preparar demo SPD','2026-08-05','URGENT','IN_PROGRESS','2026-08-04 22:47:43','2026-08-04 22:56:55'),
	 (1,'Avanzar con curso cyber','2026-08-05','LOW','IN_PROGRESS','2026-08-04 22:47:43','2026-08-04 22:56:55'),
	 (1,'Continuar con SLR','2026-08-05','URGENT','IN_PROGRESS','2026-08-04 22:47:43','2026-08-04 22:56:55'),
	 (1,'Activar el server Ubuntu','2026-08-05','MEDIUM','IN_PROGRESS','2026-08-04 22:50:37','2026-08-04 22:56:55'),
	 (2,'Cumpleaños de Exa González','2026-10-22','MEDIUM','IN_PROGRESS','2026-08-05 10:31:32','2026-08-05 10:31:32'),
	 (2,'Cumpleaños de Claudia Escamilla','2026-08-08','MEDIUM','IN_PROGRESS','2026-08-05 10:33:06','2026-08-05 10:33:06');


ALTER TABLE activities
ADD COLUMN due_time TIME NULL
AFTER due_date;


ALTER TABLE activities
    ADD KEY idx_activity_scheduler (
        user_id,
        status,
        due_date
    );

CREATE TABLE reminders (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id INT UNSIGNED NOT NULL,
    activity_id INT UNSIGNED NULL,
    title VARCHAR(250) NULL,
    reminder_type ENUM(
        'TASK',
        'ONE_SHOT',
        'RECURRING'
    ) NOT NULL,
    frequency ENUM(
        'DAILY',
        'WEEKLY',
        'MONTHLY',
        'YEARLY'
    ) NULL,
    -- Solo para ONE_SHOT
    trigger_date DATE NULL,
    -- Hora del recordatorio
    trigger_time TIME NULL,
    -- Solo para TASK
    remind_before_minutes SMALLINT UNSIGNED NULL,
    -- Solo MONTHLY y YEARLY
    day_of_month TINYINT UNSIGNED NULL,
    -- Solo YEARLY
    month_of_year TINYINT UNSIGNED NULL,
    `enabled` BOOLEAN NOT NULL DEFAULT TRUE,
    last_sent_at DATETIME NULL,
    created_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_reminder_user (user_id),
    KEY idx_reminder_activity (activity_id),
    KEY idx_reminder_scheduler (
        `enabled`,
        frequency,
        trigger_time
    ),
    KEY idx_trigger_date (
        trigger_date,
        trigger_time
    ),
    CONSTRAINT fk_reminder_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_reminder_activity
        FOREIGN KEY (activity_id)
        REFERENCES activities(id)
        ON DELETE CASCADE

);


CREATE TABLE reminder_weekdays (
    reminder_id INT UNSIGNED NOT NULL,
    `weekday` TINYINT UNSIGNED NOT NULL,
    PRIMARY KEY (
        reminder_id,
        `weekday`
    ),
    KEY idx_weekday (`weekday`),
    CONSTRAINT fk_reminder_weekday
        FOREIGN KEY (reminder_id)
        REFERENCES reminders(id)
        ON DELETE CASCADE

);