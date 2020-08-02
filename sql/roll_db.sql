CREATE TYPE bird_color AS ENUM (
    'black',
    'white',
    'black & white',
    'grey',
    'red',
    'red & white'
);

CREATE TYPE bird_species AS ENUM (
    'pigeon',
    'sparrow',
    'magpie',
    'crow',
    'titmouse'
);

CREATE TABLE birds (
    species bird_species,
    name varchar,
    color bird_color,
    body_length int,
    wingspan int,
    PRIMARY KEY (name)
);

INSERT INTO birds (species, name, color, body_length, wingspan) VALUES
('pigeon', 'Ptichek', 'red & white', 29, 50),
('sparrow', 'Tima', 'black & white', 14, 23),
('magpie', 'Belka', 'black', 44, 52),
('pigeon', 'Kadu', 'grey', 30, 56),
('pigeon', 'Ptusha', 'red & white', 31, 63),
('crow', 'Cown', 'black & white', 56, 100),
('crow', 'Koul', 'red & white', 78, 95),
('sparrow', 'Like', 'black', 18, 24),
('magpie', 'Clod', 'red & white', 45, 54),
('titmouse', 'Birdy', 'red', 12, 22),
('crow', 'Nord', 'black', 72, 110),
('crow', 'Aska', 'red & white', 68, 120),
('titmouse', 'Hloya', 'white', 14, 24),
('pigeon', 'Taimy', 'red & white', 32, 67),
('titmouse', 'Klod', 'black & white', 13, 26),
('titmouse', 'Mikky', 'black', 15, 23),
('crow', 'Fanny', 'grey', 61, 98),
('pigeon', 'Loyd', 'black & white', 33, 60),
('magpie', 'Jim', 'red & white', 46, 56),
('magpie', 'Point', 'black & white', 46, 59),
('sparrow', 'Fleyk', 'red', 17, 26),
('sparrow', 'Viola', 'red & white', 16, 24),
('pigeon', 'Monika', 'black', 34, 55),
('pigeon', 'Hope', 'grey', 35, 53),
('crow', 'Sun', 'black & white', 65, 127),
('magpie', 'Moon', 'red & white', 44, 62),
('sparrow', 'Reyna', 'red', 15, 25)
;

CREATE TABLE bird_colors_info (
    color bird_color UNIQUE,
    count int
);

CREATE TABLE bird_species_info (
    species bird_species UNIQUE,
    count int
);

CREATE TABLE birds_stat (
    body_length_mean numeric,
    body_length_median numeric,
    body_length_mode integer[],
    wingspan_mean numeric,
    wingspan_median numeric,
    wingspan_mode integer[]
);
