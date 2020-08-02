DELETE FROM birds_stat;
INSERT into birds_stat (body_length_mean, body_length_median, body_length_mode, wingspan_mean, wingspan_median)
SELECT AVG(body_length) FROM birds;