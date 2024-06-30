INSERT INTO "Appointments" ("doctor_id", "specialization_id", "doctor_offices_id", "appointment_time", "appointment_date")
SELECT
    1,
    1,
    1,
    "time"."time",
    "date"."date"
FROM
    generate_series(
        TIMESTAMP '2024-05-13 09:00',
        TIMESTAMP '2024-05-13 11:45',
        INTERVAL '15 minutes'
    ) AS "time"
JOIN
    (VALUES
        (DATE '2024-05-13'),
        (DATE '2024-05-15'),
        (DATE '2024-05-17'),
        (DATE '2024-05-20'),
        (DATE '2024-05-22'),
        (DATE '2024-05-24'),
        (DATE '2024-05-27'),
        (DATE '2024-05-29'),
        (DATE '2024-05-31')
    ) AS "date"("date") ON TRUE;

INSERT INTO "Appointments" ("doctor_id", "specialization_id", "doctor_offices_id", "appointment_time", "appointment_date")
SELECT
    2,
    2,
    2,
    "time"."time",
    "date"."date"
FROM

    generate_series(
        TIMESTAMP '2024-05-14 11:00',
        TIMESTAMP '2024-05-14 13:45',
        INTERVAL '15 minutes'
    ) AS "time"
JOIN
    (VALUES
        (DATE '2024-05-14'),
        (DATE '2024-05-21'),
        (DATE '2024-05-28')
    ) AS "date"("date") ON TRUE;


INSERT INTO "Appointments" ("doctor_id", "specialization_id", "doctor_offices_id", "appointment_time", "appointment_date")
SELECT
    3,
    3,
    3,
    "time"."time",
    "date"."date"
FROM
    generate_series(
        TIMESTAMP '2024-05-13 15:00',
        TIMESTAMP '2024-05-13 17:45',
        INTERVAL '15 minutes'
    ) AS "time"
JOIN
    (VALUES
        (DATE '2024-05-13'),
        (DATE '2024-05-20'),
        (DATE '2024-05-27')
    ) AS "date"("date") ON TRUE;


INSERT INTO "Appointments" ("doctor_id", "specialization_id", "doctor_offices_id", "appointment_time", "appointment_date")
SELECT
    4,
    4,
    4,
    "time"."time",
    "date"."date"
FROM
    generate_series(
        TIMESTAMP '2024-05-14 14:00',
        TIMESTAMP '2024-05-14 16:45',
        INTERVAL '15 minutes'
    ) AS "time"
JOIN
    (VALUES
        (DATE '2024-05-14'),
        (DATE '2024-05-21'),
        (DATE '2024-05-28')
    ) AS "date"("date") ON TRUE;


INSERT INTO "Appointments" ("doctor_id", "specialization_id", "doctor_offices_id", "appointment_time", "appointment_date")
SELECT
    5,
    5,
    5,
    "time"."time",
    "date"."date"
FROM
    generate_series(
        TIMESTAMP '2024-05-15 14:00',
        TIMESTAMP '2024-05-15 16:45',
        INTERVAL '15 minutes'
    ) AS "time"
JOIN
    (VALUES
        (DATE '2024-05-15'),
        (DATE '2024-05-22'),
        (DATE '2024-05-29')
    ) AS "date"("date") ON TRUE;


INSERT INTO "Appointments" ("doctor_id", "specialization_id", "doctor_offices_id", "appointment_time", "appointment_date")
SELECT
    6,
    6,
    6,
    "time"."time",
    "date"."date"
FROM

    generate_series(
        TIMESTAMP '2024-05-13 15:00',
        TIMESTAMP '2024-05-13 17:45',
        INTERVAL '15 minutes'
    ) AS "time"
JOIN
    (VALUES
        (DATE '2024-05-13'),
        (DATE '2024-05-20'),
        (DATE '2024-05-27')
    ) AS "date"("date") ON TRUE;


INSERT INTO "Appointments" ("doctor_id", "specialization_id", "doctor_offices_id", "appointment_time", "appointment_date")
SELECT
    7,
    7,
    7,
    "time"."time",
    "date"."date"
FROM
    generate_series(
        TIMESTAMP '2024-05-14 17:00',
        TIMESTAMP '2024-05-14 18:45',
        INTERVAL '15 minutes'
    ) AS "time"
JOIN
    generate_series(
        DATE '2024-05-14',
        DATE '2024-05-31',
        INTERVAL '1 day'
    ) AS "date" ON EXTRACT(ISODOW FROM "date"."date") = 2;


INSERT INTO "Appointments" ("doctor_id", "specialization_id", "doctor_offices_id", "appointment_time", "appointment_date")
SELECT
    8,
    8,
    8,
    "time"."time",
    "date"."date"
FROM
    generate_series(
        TIMESTAMP '2024-05-15 08:00',
        TIMESTAMP '2024-05-15 10:45',
        INTERVAL '15 minutes'
    ) AS "time"
JOIN
    generate_series(
        DATE '2024-05-15',
        DATE '2024-05-31',
        INTERVAL '1 day'
    ) AS "date" ON EXTRACT(ISODOW FROM "date"."date") = 4;


INSERT INTO "Appointments" ("doctor_id", "specialization_id", "doctor_offices_id", "appointment_time", "appointment_date")
SELECT
    9,
    9,
    9,
    "time"."time",
    "date"."date"
FROM
    generate_series(
        TIMESTAMP '2024-05-14 12:00',
        TIMESTAMP '2024-05-14 14:45',
        INTERVAL '15 minutes'
    ) AS "time"
JOIN
    generate_series(
        DATE '2024-05-14',
        DATE '2024-05-31',
        INTERVAL '1 day'
    ) AS "date" ON EXTRACT(ISODOW FROM "date"."date") = 3;


INSERT INTO "Appointments" ("doctor_id", "specialization_id", "doctor_offices_id", "appointment_time", "appointment_date")
SELECT
    10,
    10,
    10,
    "time"."time",
    "date"."date"
FROM
    generate_series(
        TIMESTAMP '2024-05-14 15:00',
        TIMESTAMP '2024-05-14 17:45',
        INTERVAL '15 minutes'
    ) AS "time"
JOIN
    generate_series(
        DATE '2024-05-14',
        DATE '2024-05-31',
        INTERVAL '1 day'
    ) AS "date" ON EXTRACT(ISODOW FROM "date"."date") = 3;


INSERT INTO "Appointments" ("doctor_id", "specialization_id", "doctor_offices_id", "appointment_time", "appointment_date")
SELECT
    11,
    11,
    11,
    "time"."time",
    "date"."date"
FROM
    generate_series(
        TIMESTAMP '2024-05-14 08:00',
        TIMESTAMP '2024-05-14 10:45',
        INTERVAL '15 minutes'
    ) AS "time"
JOIN
    generate_series(
        DATE '2024-05-14',
        DATE '2024-05-31',
        INTERVAL '1 day'
    ) AS "date" ON EXTRACT(ISODOW FROM "date"."date") = 2;


INSERT INTO "Appointments" ("doctor_id", "specialization_id", "doctor_offices_id", "appointment_time", "appointment_date")
SELECT
    12,
    12,
    12,
    "time"."time",
    "date"."date"
FROM
    generate_series(
        TIMESTAMP '2024-05-12 17:00',
        TIMESTAMP '2024-05-12 18:45',
        INTERVAL '15 minutes'
    ) AS "time"
JOIN
    generate_series(
        DATE '2024-05-13',
        DATE '2024-05-31',
        INTERVAL '1 day'
    ) AS "date" ON EXTRACT(ISODOW FROM "date"."date") = 4;


INSERT INTO "Appointments" ("doctor_id", "specialization_id", "doctor_offices_id", "appointment_time", "appointment_date")
SELECT
    13,
    13,
    13,
    "time"."time",
    "date"."date"
FROM
    generate_series(
        TIMESTAMP '2024-05-13 08:00',
        TIMESTAMP '2024-05-13 08:45',
        INTERVAL '15 minutes'
    ) AS "time"
JOIN
    generate_series(
        DATE '2024-05-13',
        DATE '2024-05-31',
        INTERVAL '1 day'
    ) AS "date" ON EXTRACT(ISODOW FROM "date"."date") = 1;


INSERT INTO "Appointments" ("doctor_id", "specialization_id", "doctor_offices_id", "appointment_time", "appointment_date")
SELECT
    14,
    14,
    14,
    "time"."time",
    "date"."date"
FROM
    generate_series(
        TIMESTAMP '2024-05-13 08:00',
        TIMESTAMP '2024-05-13 08:45',
        INTERVAL '15 minutes'
    ) AS "time"
JOIN
    generate_series(
        DATE '2024-05-13',
        DATE '2024-05-31',
        INTERVAL '1 day'
    ) AS "date" ON EXTRACT(ISODOW FROM "date"."date") = 5;

INSERT INTO "Appointments" ("doctor_id", "specialization_id", "doctor_offices_id", "appointment_time", "appointment_date")
SELECT
    15,
    15,
    15,
    "time"."time",
    "date"."date"
FROM
    generate_series(
        TIMESTAMP '2024-05-13 08:00',
        TIMESTAMP '2024-05-13 08:45',
        INTERVAL '15 minutes'
    ) AS "time"
JOIN
    generate_series(
        DATE '2024-05-13',
        DATE '2024-05-31',
        INTERVAL '1 day'
    ) AS "date" ON EXTRACT(ISODOW FROM "date"."date") = 3;
