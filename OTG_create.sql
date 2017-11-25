-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2017-11-23 16:48:41.534

-- tables
-- Table: admin
CREATE TABLE admin (
    admin_id serial  NOT NULL,
    name varchar(50)  NOT NULL,
    parent_fk int  NULL,
    center_fk int  NULL,
    admin_cat_fk int  NOT NULL,
    koatuu char(20)  NULL,
    population int  NOT NULL,
    descript jsonb  NULL,
    geom geometry  NULL,
    CONSTRAINT admin_pk PRIMARY KEY (admin_id)
);

-- Table: admin_category
CREATE TABLE admin_category (
    admin_cat_id serial  NOT NULL,
    name varchar(50)  NOT NULL,
    parent_id int  NULL,
    CONSTRAINT admin_category_ak_1 UNIQUE (name, parent_id) NOT DEFERRABLE  INITIALLY IMMEDIATE,
    CONSTRAINT admin_category_pk PRIMARY KEY (admin_cat_id)
);

-- Table: age
CREATE TABLE age (
    admin_fk int  NOT NULL,
    date_stamp date  NOT NULL,
    age_0 int  NOT NULL,
    age_1_2 int  NOT NULL,
    age_3 int  NOT NULL,
    age_4 int  NOT NULL,
    age_5 int  NOT NULL,
    age_6 int  NOT NULL,
    age_7_14 int  NOT NULL,
    age_15 int  NOT NULL,
    age_16 int  NOT NULL,
    age_17 int  NOT NULL,
    age_18 int  NOT NULL,
    age_19_54_w int  NOT NULL,
    age_19_59_m int  NOT NULL,
    age_after int  NOT NULL,
    age_general int  NOT NULL,
    CONSTRAINT age_pk PRIMARY KEY (admin_fk,date_stamp)
);

-- Table: category
CREATE TABLE category (
    category_id serial  NOT NULL,
    name varchar(50)  NOT NULL,
    parent_id int  NOT NULL,
    CONSTRAINT obj_categories_ak_1 UNIQUE (name, parent_id) NOT DEFERRABLE  INITIALLY IMMEDIATE,
    CONSTRAINT category_pk PRIMARY KEY (category_id)
);

-- Table: dynamics
CREATE TABLE dynamics (
    admin_fk int  NOT NULL,
    date_stamp date  NOT NULL,
    population int  NOT NULL,
    born int  NOT NULL,
    died int  NOT NULL,
    move_in int  NOT NULL,
    move_out int  NOT NULL,
    CONSTRAINT dynamics_pk PRIMARY KEY (admin_fk,date_stamp)
);

-- Table: empl
CREATE TABLE empl (
    admin_fk int  NOT NULL,
    date_stamp date  NOT NULL,
    category_fk int  NOT NULL,
    value int  NOT NULL,
    CONSTRAINT empl_ak_1 UNIQUE (admin_fk, category_fk, date_stamp) NOT DEFERRABLE  INITIALLY IMMEDIATE,
    CONSTRAINT empl_pk PRIMARY KEY (admin_fk,date_stamp)
);

CREATE INDEX empl_idx_1 on empl (admin_fk ASC);

-- Table: empl_category
CREATE TABLE empl_category (
    empl_cat_id serial  NOT NULL,
    name varchar(30)  NOT NULL,
    CONSTRAINT empl_category_ak_1 UNIQUE (name) NOT DEFERRABLE  INITIALLY IMMEDIATE,
    CONSTRAINT empl_category_pk PRIMARY KEY (empl_cat_id)
);

-- Table: owner
CREATE TABLE owner (
    edrpou int  NOT NULL,
    name varchar(100)  NOT NULL,
    quant_staff int  NULL,
    budget boolean  NOT NULL,
    kved char(5)  NULL,
    CONSTRAINT owner_pk PRIMARY KEY (edrpou)
);

-- Table: social
CREATE TABLE social (
    social_id serial  NOT NULL,
    name varchar(70)  NOT NULL,
    address char(100)  NULL,
    obj_category int  NOT NULL,
    contact varchar(50)  NULL,
    hours varchar(150)  NULL,
    date_establish date  NULL,
    sq_area int  NULL,
    quant_staff int  NULL,
    quant_other int  NULL,
    capacity_max int  NULL,
    capacity_real jsonb  NULL,
    service_area varchar(100)  NULL,
    area_used int  NULL,
    description varchar(255)  NULL,
    add_service varchar(150)  NULL,
    status boolean  NULL,
    geom geometry  NULL,
    owner_fk int  NOT NULL,
    CONSTRAINT social_pk PRIMARY KEY (social_id)
);

-- foreign keys
-- Reference: admin_admin1 (table: admin)
ALTER TABLE admin ADD CONSTRAINT admin_admin1
    FOREIGN KEY (parent_fk)
    REFERENCES admin (admin_id)
    ON DELETE  RESTRICT  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: admin_admin2 (table: admin)
ALTER TABLE admin ADD CONSTRAINT admin_admin2
    FOREIGN KEY (center_fk)
    REFERENCES admin (admin_id)
    ON DELETE  RESTRICT  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: admin_admin_category (table: admin)
ALTER TABLE admin ADD CONSTRAINT admin_admin_category
    FOREIGN KEY (admin_cat_fk)
    REFERENCES admin_category (admin_cat_id)
    ON DELETE  RESTRICT  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: admin_age (table: age)
ALTER TABLE age ADD CONSTRAINT admin_age
    FOREIGN KEY (admin_fk)
    REFERENCES admin (admin_id)
    ON DELETE  CASCADE  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: dynamics_admin (table: dynamics)
ALTER TABLE dynamics ADD CONSTRAINT dynamics_admin
    FOREIGN KEY (admin_fk)
    REFERENCES admin (admin_id)
    ON DELETE  RESTRICT  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: empl_admin (table: empl)
ALTER TABLE empl ADD CONSTRAINT empl_admin
    FOREIGN KEY (admin_fk)
    REFERENCES admin (admin_id)
    ON DELETE  CASCADE  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: empl_empl_cat (table: empl)
ALTER TABLE empl ADD CONSTRAINT empl_empl_cat
    FOREIGN KEY (category_fk)
    REFERENCES empl_category (empl_cat_id)
    ON DELETE  RESTRICT  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: social_category (table: social)
ALTER TABLE social ADD CONSTRAINT social_category
    FOREIGN KEY (obj_category)
    REFERENCES category (category_id)
    ON DELETE  RESTRICT  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: social_owner (table: social)
ALTER TABLE social ADD CONSTRAINT social_owner
    FOREIGN KEY (owner_fk)
    REFERENCES owner (edrpou)
    ON DELETE  RESTRICT  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

