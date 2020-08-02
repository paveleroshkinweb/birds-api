DELETE FROM bird_colors_info;
INSERT INTO bird_colors_info (color, count) SELECT color, COUNT(color) from birds GROUP BY color;