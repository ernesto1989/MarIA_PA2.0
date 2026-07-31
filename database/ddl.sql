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

CREATE PROCEDURE sp_cleanup_completed_tasks(
    IN p_user_id INT UNSIGNED
)
BEGIN
    DELETE FROM activities
    WHERE user_id = p_user_id
      AND status = 'DONE';
END$$

DELIMITER ;

CALL sp_cleanup_completed_tasks(1);