PRAGMA journal_mode = MEMORY;
PRAGMA synchronous = OFF;
PRAGMA foreign_keys = OFF;
PRAGMA ignore_check_constraints = OFF;
PRAGMA auto_vacuum = NONE;
PRAGMA secure_delete = OFF;
BEGIN TRANSACTION;

phpMyAdmin SQL Dump
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";
DROP TABLE IF EXISTS `audit_log`;

CREATE TABLE `audit_log` (
`id` int NOT NULL,
`user_id` int NOT NULL,
`action` TEXT NOT NULL,
`action_timestamp` datetime NOT NULL
);
INSERT INTO `audit_log` (`id`, `user_id`, `action`, `action_timestamp`) VALUES
(1, 1, 'Move test', '2025-05-24 16:45:12');
DROP TABLE IF EXISTS `inbound`;

CREATE TABLE `inbound` (
`id` int NOT NULL,
`item_name` TEXT   NOT NULL,
`shipment_type` TEXT NOT NULL,
`shipment_location` TEXT NOT NULL,
`inbound_timestamp` datetime NOT NULL
);
INSERT INTO `inbound` (`id`, `item_name`, `shipment_type`, `shipment_location`, `inbound_timestamp`) VALUES
(15, 'test1', 'regular', 'jkt', '2025-05-24 21:58:04');
DROP TABLE IF EXISTS `items`;

CREATE TABLE `items` (
`id` int NOT NULL,
`weight` int NOT NULL,
`storage_location` int NOT NULL,
`inbound_id` int DEFAULT NULL,
`outbound_id` int DEFAULT NULL
);
INSERT INTO `items` (`id`, `weight`, `storage_location`, `inbound_id`, `outbound_id`) VALUES
(10, 12, 1, 15, 6);
DROP TABLE IF EXISTS `outbound`;

CREATE TABLE `outbound` (
`id` int NOT NULL,
`shipment_type` TEXT NOT NULL,
`shipment_location` TEXT NOT NULL,
`id_item` int NOT NULL,
`outbound_timestamp` datetime NOT NULL
);
INSERT INTO `outbound` (`id`, `shipment_type`, `shipment_location`, `id_item`, `outbound_timestamp`) VALUES
(6, 'regular', 'jkt', 10, '2025-05-26 17:36:50');
DROP TABLE IF EXISTS `storage`;

CREATE TABLE `storage` (
`id` int NOT NULL,
`rack_id` TEXT NOT NULL
);
INSERT INTO `storage` (`id`, `rack_id`) VALUES
(1, 'rack01'),
(2, 'rack02');
DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
`id` int NOT NULL,
`username` TEXT NOT NULL,
`password` TEXT NOT NULL
);
INSERT INTO `user` (`id`, `username`, `password`) VALUES
(1, 'admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'),
(2, 'registUser', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9');
ALTER TABLE `audit_log`
ADD PRIMARY KEY (`id`),
ADD KEY `user_id` (`user_id`);
ALTER TABLE `inbound`
ADD PRIMARY KEY (`id`);
ALTER TABLE `items`
ADD PRIMARY KEY (`id`),
ADD KEY `storage_location` (`storage_location`),
ADD KEY `inbound_id` (`inbound_id`,`outbound_id`),
ADD KEY `outbound_id` (`outbound_id`);
ALTER TABLE `outbound`
ADD PRIMARY KEY (`id`),
ADD KEY `id_item` (`id_item`);
ALTER TABLE `storage`
ADD PRIMARY KEY (`id`),
ADD UNIQUE KEY `rack_id` (`rack_id`),
ADD KEY `rack_id_2` (`rack_id`);
ALTER TABLE `user`
ADD PRIMARY KEY (`id`);
ALTER TABLE `audit_log`
MODIFY `id` int NOT NULL , =2;
ALTER TABLE `inbound`
MODIFY `id` int NOT NULL , =16;
ALTER TABLE `items`
MODIFY `id` int NOT NULL , =11;
ALTER TABLE `outbound`
MODIFY `id` int NOT NULL , =7;
ALTER TABLE `storage`
MODIFY `id` int NOT NULL , =3;
ALTER TABLE `user`
MODIFY `id` int NOT NULL , =3;
ALTER TABLE `audit_log`
ADD CONSTRAINT `audit_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `items`
ADD CONSTRAINT `items_ibfk_1` FOREIGN KEY (`storage_location`) REFERENCES `storage` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT `items_ibfk_2` FOREIGN KEY (`outbound_id`) REFERENCES `outbound` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT `items_ibfk_3` FOREIGN KEY (`inbound_id`) REFERENCES `inbound` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `outbound`
ADD CONSTRAINT `outbound_ibfk_1` FOREIGN KEY (`id_item`) REFERENCES `items` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;





COMMIT;
PRAGMA ignore_check_constraints = ON;
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
