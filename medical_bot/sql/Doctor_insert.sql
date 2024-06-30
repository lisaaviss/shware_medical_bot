
INSERT INTO "Doctor" ("name", "specialization_id")
VALUES
    ('Иванов Иван Иванович', (SELECT "id" FROM "Specialization" WHERE "name" = 'Терапевт')),
    ('Петров Петр Петрович', (SELECT "id" FROM "Specialization" WHERE "name" = 'Хирург')),
    ('Сидоров Сидор Сидорович', (SELECT "id" FROM "Specialization" WHERE "name" = 'Офтальмолог')),
    ('Алексеев Алексей Алексеевич', (SELECT "id" FROM "Specialization" WHERE "name" = 'Гастроэнтеролог')),
    ('Ковалев Константин Константинович', (SELECT "id" FROM "Specialization" WHERE "name" = 'Отоларинголог')),
    ('Смирнова Светлана Сергеевна', (SELECT "id" FROM "Specialization" WHERE "name" = 'Гинеколог')),
    ('Беляева Елена Владимировна', (SELECT "id" FROM "Specialization" WHERE "name" = 'Кардиолог')),
    ('Федорова Екатерина Алексеевна', (SELECT "id" FROM "Specialization" WHERE "name" = 'Дерматолог')),
    ('Попова Анна Анатольевна', (SELECT "id" FROM "Specialization" WHERE "name" = 'Онколог')),
    ('Григорьев Игорь Игоревич', (SELECT "id" FROM "Specialization" WHERE "name" = 'Невролог')),
    ('Антонов Антон Антонович', (SELECT "id" FROM "Specialization" WHERE "name" = 'Уролог')),
    ('Павлов Павел Павлович', (SELECT "id" FROM "Specialization" WHERE "name" = 'Психиатр')),
    ('Михайлова Мария Михайловна', (SELECT "id" FROM "Specialization" WHERE "name" = 'Инфекционист')),
    ('Васильев Василий Васильевич', (SELECT "id" FROM "Specialization" WHERE "name" = 'Рентгенолог')),
    ('Дмитриев Дмитрий Дмитриевич', (SELECT "id" FROM "Specialization" WHERE "name" = 'Физиотерапевт'));
