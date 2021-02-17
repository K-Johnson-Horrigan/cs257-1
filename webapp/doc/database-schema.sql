CREATE TABLE countries(
  id int,
  country text
);

CREATE TABLE crops(
  id int,
  crop text
);

CREATE TABLE years(
  id int,
  year int
);

CREATE TABLE country_crop_year(
  country_id int,
  crop_id int,
  year_id int,
  yield int
);
