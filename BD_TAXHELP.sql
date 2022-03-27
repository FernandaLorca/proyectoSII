CREATE TABLE CM (
    mes varchar(50) NOT NULL,
    porcentaje FLOAT NOT NULL,
    anio INT NOT NULL
);

ALTER TABLE CM ADD PRIMARY KEY (mes, anio);

insert into CM (mes,  porcentaje, anio) values ('Enero', 6.3, 2021);
insert into CM (mes,  porcentaje, anio) values ('Febrero', 5.6, 2021);
insert into CM (mes,  porcentaje, anio) values ('Marzo', 5.4, 2021);
insert into CM (mes,  porcentaje, anio) values ('Abril', 5.0, 2021);
insert into CM (mes,  porcentaje, anio) values ('Mayo', 4.6, 2021);
insert into CM (mes,  porcentaje, anio) values ('Junio', 4.3, 2021);
insert into CM (mes,  porcentaje, anio) values ('Julio', 4.3, 2021);
insert into CM (mes,  porcentaje, anio) values ('Agosto', 3.4, 2021);
insert into CM (mes,  porcentaje, anio) values ('Septiembre', 3.1, 2021);
insert into CM (mes,  porcentaje, anio) values ('Octubre', 1.8, 2021);
insert into CM (mes,  porcentaje, anio) values ('Noviembre', 0.5, 2021);


CREATE TABLE IA (
    desde FLOAT NOT NULL,
    hasta FLOAT ,
    factor FLOAT NOT NULL ,
    CR FLOAT NOT NULL,
    anio INT NOT NULL
);

ALTER TABLE IA ADD PRIMARY KEY (factor, anio);

insert into IA (desde, hasta, factor, CR, anio) values (0, 8775702, 0, 0, 2022);
insert into IA (desde, hasta, factor, CR, anio) values (8775702.01, 19501560, 0.04, 351028.08, 2022);
insert into IA (desde, hasta, factor, CR, anio) values (19501560.01, 32502600, 0.08, 1131090.48, 2022);
insert into IA (desde, hasta, factor, CR, anio) values (32502600.01, 45503640, 0.135, 2918733.48, 2022);
insert into IA (desde, hasta, factor, CR, anio) values (45503640.01, 58504680, 0.23, 7241579.28, 2022);
insert into IA (desde, hasta, factor, CR, anio) values (58504680.01, 78006240, 0.304, 11570925.6, 2022);
insert into IA (desde, hasta, factor, CR, anio) values (78006240.01, 201516120, 0.35, 15159212.64, 2022);
insert into IA (desde, hasta, factor, CR, anio) values (201516120.01, null, 0.4, 25235018.64, 2022);

insert into IA (desde, hasta, factor, CR, anio) values (0, 8266698, 0, 0, 2021);
insert into IA (desde, hasta, factor, CR, anio) values (8266698.01, 18370440, 0.04, 330667.92, 2021);
insert into IA (desde, hasta, factor, CR, anio) values (18370440.01, 30617400, 0.08, 1065485.52, 2021);
insert into IA (desde, hasta, factor, CR, anio) values (30617400.01, 42864360, 0.135, 2748442.52, 2021);
insert into IA (desde, hasta, factor, CR, anio) values (42864360.01, 55111320, 0.23, 6821556.72, 2021);
insert into IA (desde, hasta, factor, CR, anio) values (55111320.01, 73481760, 0.304, 10899794.40, 2021);
insert into IA (desde, hasta, factor, CR, anio) values (73481760.01, 189827880, 0.35, 14279955.36, 2021);
insert into IA (desde, hasta, factor, CR, anio) values (189827880.01, null, 0.40, 23771349.36, 2021);