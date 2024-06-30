
CREATE TABLE "Patient" (
	"id" serial NOT NULL,
	"name" varchar(255),
	"date_of_birth" date,
	"number" varchar(255),
	"chat_id" varchar(255),
	PRIMARY KEY("id")
);

CREATE TABLE "Doctor" (
	"id" serial NOT NULL,
	"name" varchar(255),
	"specialization_id" int,
	PRIMARY KEY("id")
);

CREATE TABLE "Specialization" (
	"id" serial NOT NULL,
	"name" varchar(255),
	PRIMARY KEY("id")
);

CREATE TABLE "Doctor_offices" (
	"id" serial NOT NULL,
	"office_number" varchar(255),
	PRIMARY KEY("id")
);

CREATE TABLE "Appointments" (
	"id" serial NOT NULL,
	"patient_id" int,
	"doctor_id" int,
	"specialization_id" int,
	"doctor_offices_id" int,
	"appointment_time" time,
	"appointment_date" date,
	PRIMARY KEY("id")
);

CREATE TABLE "Home_address" (
	"id" serial NOT NULL,
	"patient_id" int,
	"city_name" varchar(255),
	"street_name" varchar(255),
	"house_number" varchar(255),
	"building_number" varchar(255),
	"building_letter" varchar(255),
	"entrance" varchar(255),
	"floor" varchar(255),
	"apartment_number" varchar(255),
	PRIMARY KEY("id")
);

CREATE TABLE "Doctor_house_calls" (
	"id" serial NOT NULL,
	"patient_id" int,
	"home_address_id" int,
	"call_date" date,
	PRIMARY KEY("id")
);

CREATE TABLE "Medical_record" (
	"id" serial NOT NULL,
	"patient_id" int,
	"doctor_id" int,
	"creation_date" date,
	"symptoms" varchar(255),
	"diagnosis" varchar(255),
	"treatment_plans" varchar(255),
	"notes" varchar(255),
	"checkup_id" int,
	"appointment_id" int,
	PRIMARY KEY("id")
);

CREATE TABLE "Medical_examination" (
	"id" serial NOT NULL,
	"name" varchar(255),
	"patient_id" int,
	"doctor_id" int,
	"result" varchar(255),
	"examination_date" date,
	"medical_record_id" int,
	PRIMARY KEY("id")
);

CREATE TABLE "Medical_objects" (
	"id" serial NOT NULL,
	"record_id" int,
	"examination_id" int,
	"name" varchar(255),
	"link" varchar(255),
	PRIMARY KEY("id")
);

CREATE TABLE "Allergies_types" (
	"id" serial NOT NULL,
	"name" varchar(255),
	PRIMARY KEY("id")
);

CREATE TABLE "Allergies" (
	"id" serial NOT NULL,
	"allergy_type_id" int,
	"allergen" varchar(255),
	"reaction_id" int,
	"patient_id" int,
	PRIMARY KEY("id")
);

CREATE TABLE "Reaction_type" (
	"id" serial NOT NULL,
	"name" varchar(255),
	PRIMARY KEY("id")
);

CREATE TABLE "Taken_medications" (
	"id" serial NOT NULL,
	"patient_id" int,
	"start_date" date,
	"end_date" date,
	PRIMARY KEY("id")
);

CREATE TABLE "Patient_vaccinations" (
	"id" serial NOT NULL,
	"patient_id" int,
	"date_of_vaccination" date,
	"vaccination_type_id" int,
	PRIMARY KEY("id")
);

CREATE TABLE "Vaccination_types" (
	"id" serial NOT NULL,
	"name" varchar(255),
	"frequency" int,
	PRIMARY KEY("id")
);

CREATE TABLE "Medical_check_up" (
	"id" serial NOT NULL,
	"patient_id" int,
	"doctor_id" int,
	"name" varchar(255),
	PRIMARY KEY("id")
);

CREATE TABLE "Messages" (
	"id" serial NOT NULL,
	"patient_id" int,
	"command" varchar(255),
	"msg1" varchar(255),
	"msg2" varchar(255),
	"msg3" varchar(255),
	"msg4" varchar(255),
	"msg5" varchar(255),
	"msg6" varchar(255),
	"msg7" varchar(255),
	"msg8" varchar(255),
	"msg9" varchar(255),
	"msg10" varchar(255),
	PRIMARY KEY("id")
);

ALTER TABLE "Doctor"
ADD FOREIGN KEY("specialization_id") REFERENCES "Specialization"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Appointments"
ADD FOREIGN KEY("patient_id") REFERENCES "Patient"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Appointments"
ADD FOREIGN KEY("doctor_id") REFERENCES "Doctor"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Appointments"
ADD FOREIGN KEY("specialization_id") REFERENCES "Specialization"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Appointments"
ADD FOREIGN KEY("doctor_offices_id") REFERENCES "Doctor_offices"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Home_address"
ADD FOREIGN KEY("patient_id") REFERENCES "Patient"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Doctor_house_calls"
ADD FOREIGN KEY("patient_id") REFERENCES "Patient"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Doctor_house_calls"
ADD FOREIGN KEY("home_address_id") REFERENCES "Home_address"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Medical_record"
ADD FOREIGN KEY("patient_id") REFERENCES "Patient"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Medical_examination"
ADD FOREIGN KEY("doctor_id") REFERENCES "Doctor"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Medical_record"
ADD FOREIGN KEY("appointment_id") REFERENCES "Appointments"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Medical_examination"
ADD FOREIGN KEY("patient_id") REFERENCES "Patient"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Medical_objects"
ADD FOREIGN KEY("examination_id") REFERENCES "Medical_examination"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Medical_objects"
ADD FOREIGN KEY("record_id") REFERENCES "Medical_record"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Taken_medications"
ADD FOREIGN KEY("patient_id") REFERENCES "Patient"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Allergies"
ADD FOREIGN KEY("patient_id") REFERENCES "Patient"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Allergies"
ADD FOREIGN KEY("allergy_type_id") REFERENCES "Allergies_types"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Allergies"
ADD FOREIGN KEY("reaction_id") REFERENCES "Reaction_type"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Medical_examination"
ADD FOREIGN KEY("medical_record_id") REFERENCES "Medical_record"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Patient_vaccinations"
ADD FOREIGN KEY("patient_id") REFERENCES "Patient"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Patient_vaccinations"
ADD FOREIGN KEY("vaccination_type_id") REFERENCES "Vaccination_types"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Medical_record"
ADD FOREIGN KEY("checkup_id") REFERENCES "Medical_check_up"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Medical_record"
ADD FOREIGN KEY("doctor_id") REFERENCES "Doctor"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Medical_check_up"
ADD FOREIGN KEY("patient_id") REFERENCES "Patient"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Medical_check_up"
ADD FOREIGN KEY("doctor_id") REFERENCES "Doctor"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Messages"
ADD FOREIGN KEY("patient_id") REFERENCES "Patient"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;