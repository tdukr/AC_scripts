-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2017-10-27 16:10:12.335

-- tables
-- Table: admin
CREATE TABLE admin (
    admin_id serial  NOT NULL,
    name char(50)  NOT NULL,
    "level" int  NOT NULL,
    koatuu char(20)  NULL,
    population int  NULL,
    geom geometry  NOT NULL,
    CONSTRAINT admin_ak_1 UNIQUE (name, "level") NOT DEFERRABLE  INITIALLY IMMEDIATE,
    CONSTRAINT admin_pk PRIMARY KEY (admin_id)
);

-- Table: admin_category
CREATE TABLE admin_category (
    admin_cat_id serial  NOT NULL,
    name char(30)  NOT NULL,
    CONSTRAINT admin_category_ak_1 UNIQUE (name) NOT DEFERRABLE  INITIALLY IMMEDIATE,
    CONSTRAINT admin_category_pk PRIMARY KEY (admin_cat_id)
);

-- Table: age
CREATE TABLE age (
    age_id serial  NOT NULL,
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
    CONSTRAINT age_ak_1 UNIQUE (admin_fk, date_stamp) NOT DEFERRABLE  INITIALLY IMMEDIATE,
    CONSTRAINT age_pk PRIMARY KEY (age_id)
);

-- Table: category
CREATE TABLE category (
    category_id serial  NOT NULL,
    name char(50)  NOT NULL,
    parent_id int  NULL,
    CONSTRAINT obj_categories_ak_1 UNIQUE (name) NOT DEFERRABLE  INITIALLY IMMEDIATE,
    CONSTRAINT category_pk PRIMARY KEY (category_id)
);

-- Table: dynamics
CREATE TABLE dynamics (
    dyn_id int  NOT NULL,
    admin_fk int  NOT NULL,
    population int  NOT NULL,
    born int  NULL,
    died int  NULL,
    move_in int  NULL,
    move_out int  NULL,
    date_stamp date  NOT NULL,
    CONSTRAINT dynamics_ak_1 UNIQUE (admin_fk, date_stamp) NOT DEFERRABLE  INITIALLY IMMEDIATE,
    CONSTRAINT dynamics_pk PRIMARY KEY (dyn_id)
);

-- Table: empl
CREATE TABLE empl (
    empl_id serial  NOT NULL,
    date_stamp date  NOT NULL,
    admin_fk int  NOT NULL,
    category int  NOT NULL,
    value int  NOT NULL,
    CONSTRAINT empl_ak_1 UNIQUE (admin_fk, category, date_stamp) DEFERRABLE  INITIALLY IMMEDIATE,
    CONSTRAINT empl_pk PRIMARY KEY (empl_id)
);

CREATE INDEX empl_idx_1 on empl (admin_fk ASC);

-- Table: empl_category
CREATE TABLE empl_category (
    empl_cat_id serial  NOT NULL,
    name char(20)  NOT NULL,
    CONSTRAINT empl_category_ak_1 UNIQUE (name) NOT DEFERRABLE  INITIALLY IMMEDIATE,
    CONSTRAINT empl_category_pk PRIMARY KEY (empl_cat_id)
);

-- Table: infrastructure
CREATE TABLE infrastructure (
    infra_id serial  NOT NULL,
    name char(70)  NOT NULL,
    geom_point geometry  NOT NULL,
    geom_polygon geometry  NOT NULL,
    geom_line geometry  NOT NULL,
    geom_mline geometry  NOT NULL,
    geom_mpolygon geometry  NOT NULL,
    CONSTRAINT check_1 CHECK (geom_point IS NOT NULL OR geom_polygon IS NOT NULL OR geom_line IS NOT NULL OR geom_mline IS NOT NULL OR geom_mpolygon IS NOT NULL) NOT DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT infrastructure_pk PRIMARY KEY (infra_id)
);

-- Table: social
CREATE TABLE social (
    social_id serial  NOT NULL,
    geom_point geometry  NOT NULL,
    geom_polygon geometry  NOT NULL,
    geom_line geometry  NOT NULL,
    geom_mline geometry  NOT NULL,
    geom_mpolygon geometry  NOT NULL,
    name char(70)  NOT NULL,
    address char(100)  NULL,
    obj_category int  NOT NULL,
    contact char(50)  NULL,
    hours char(150)  NULL,
    date_establish date  NULL,
    sq_area smallint  NULL,
    quant_staff smallint  NULL,
    quant_other smallint  NULL,
    capacity_max int  NULL,
    capacity_real jsonb  NULL,
    service_area char(100)  NULL,
    area_used smallint  NULL,
    description char(255)  NULL,
    subtype char(70)  NULL,
    status boolean  NULL,
    religion char(70)  NULL,
    add_service char(100)  NULL,
    CONSTRAINT check_1 CHECK (geom_point IS NOT NULL OR geom_polygon IS NOT NULL OR geom_line IS NOT NULL OR geom_mline IS NOT NULL OR geom_mpolygon IS NOT NULL) DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT social_pk PRIMARY KEY (social_id)
);

-- foreign keys
-- Reference: admin_admin_category (table: admin)
ALTER TABLE admin ADD CONSTRAINT admin_admin_category
    FOREIGN KEY ("level")
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
    ON DELETE  CASCADE  
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
    FOREIGN KEY (category)
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

-- End of file.

