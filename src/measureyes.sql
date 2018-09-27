
/* Create web backend master db */
CREATE TABLE rekmaster (
  video VARCHAR,
  source_file VARCHAR,
  timestamp INT, -- video timestamp in milliseconds from start
  person_index INT,
  face_yaw FLOAT(4),
  face_pitch FLOAT(4),
  face_box_top FLOAT(4),
  face_box_left FLOAT(4)
);
