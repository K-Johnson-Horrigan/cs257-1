CREATE TABLE countries(
  id int,
  country text
);

CREATE TABLE crops(
  id int,
  crop text
);

CREATE TABLE country_crop(
  country_id int,
  crop_id int,
  year int,
  yield int
);
