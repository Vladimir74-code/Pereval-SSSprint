-- Создание индексов для оптимизации запросов
CREATE INDEX idx_pereval_user ON pereval_added(user_email);
CREATE INDEX idx_pereval_coord ON pereval_added(coord_id);