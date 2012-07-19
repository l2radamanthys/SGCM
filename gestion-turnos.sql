BEGIN;
CREATE TABLE "UsersInformation" (
    "id" serial NOT NULL PRIMARY KEY,
    "type_doc" varchar(6) NOT NULL,
    "nro_doc" varchar(12) NOT NULL,
    "gender" varchar(1) NOT NULL,
    "phone" varchar(20) NOT NULL,
    "address" varchar(120) NOT NULL,
    "matricula" varchar(30) NOT NULL,
    "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "MedicalSpecialties" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(60) NOT NULL,
    "description" text NOT NULL
)
;
CREATE TABLE "MedicalSpecialtiesFor" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "speciality_id" integer NOT NULL REFERENCES "MedicalSpecialties" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE INDEX "MedicalSpecialtiesFor_user_id" ON "MedicalSpecialtiesFor" ("user_id");
CREATE INDEX "MedicalSpecialtiesFor_speciality_id" ON "MedicalSpecialtiesFor" ("speciality_id");
COMMIT;
