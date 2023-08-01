CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `roles` json NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE `ECG` (
  `id` varchar(200) NOT NULL,
  `user` int NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_ecg__user` (`user`),
  CONSTRAINT `fk_ecg__user` FOREIGN KEY (`user`) REFERENCES `USERS` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB CHARSET=utf8;

CREATE TABLE `ECG_leads` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ecg` varchar(200) NOT NULL,
  `name` varchar(255) NOT NULL,
  `num_samples` int DEFAULT NULL,
  `signal` json DEFAULT NULL,
  `count_zero_crossings` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_ecg_leads__ecg` (`ecg`),
  CONSTRAINT `fk_ecg_leads__ecg` FOREIGN KEY (`ecg`) REFERENCES `ECG` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB CHARSET=utf8;

INSERT INTO `USERS` (`id`, `name`, `password`, `roles`) VALUES
(1, 'admin', '$6$rounds=656000$xNxQr23LR67zebev$Q2dDxuvgb4GywZ7Wqp4Fsgd/BxQ1Ozyi8A4fF1.iuzWEJJQJ06GXCWZjqD9dKwE7PJKw4jN1Jt.qUyZ.OmExr1', '[\"admin\"]'),
(2, 'user', '$6$rounds=656000$/Gk1UFbJ9iMzq17s$kK7n8wv/smuhBcK2SzMo2P2N6eigFBQJ22XEp09tNIiiMEz7wYZTTsHCJ9uigzC4TLlpeOddFGNxcBqBUUVxJ.', '[\"user\"]');