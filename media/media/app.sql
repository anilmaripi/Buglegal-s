-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 08, 2023 at 02:37 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `app`
--

-- --------------------------------------------------------

--
-- Table structure for table `appfooter_appdown`
--

CREATE TABLE `appfooter_appdown` (
  `id` bigint(20) NOT NULL,
  `heading` varchar(100) NOT NULL,
  `app` varchar(100) NOT NULL,
  `url` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `appfooter_appdown`
--

INSERT INTO `appfooter_appdown` (`id`, `heading`, `app`, `url`) VALUES
(1, 'Download Mobile App', 'googleplay.png', 'https://play.google.com/'),
(2, '', 'ios.png', '\nhttps://www.apple.com/');

-- --------------------------------------------------------

--
-- Table structure for table `appfooter_appfooter`
--

CREATE TABLE `appfooter_appfooter` (
  `id` bigint(20) NOT NULL,
  `name` varchar(200) NOT NULL,
  `url` varchar(100) NOT NULL,
  `icon` varchar(100) NOT NULL,
  `heading` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `appfooter_appfooter`
--

INSERT INTO `appfooter_appfooter` (`id`, `name`, `url`, `icon`, `heading`) VALUES
(1, 'Home', '#', 'fa fa-home', 'Quick links'),
(2, 'Aboutus', '#', 'fa fa-address-book-o', ''),
(3, 'Availability', '#', 'fa fa-check-square-o', ''),
(4, 'Blood Bank Registration', '#', 'fa fa-check-square-o', '');

-- --------------------------------------------------------

--
-- Table structure for table `appfooter_appfooter1`
--

CREATE TABLE `appfooter_appfooter1` (
  `id` bigint(20) NOT NULL,
  `name` varchar(200) NOT NULL,
  `url` varchar(100) NOT NULL,
  `icon` varchar(100) NOT NULL,
  `heading` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `appfooter_appfooter1`
--

INSERT INTO `appfooter_appfooter1` (`id`, `name`, `url`, `icon`, `heading`) VALUES
(1, 'Blood Varients', '#', 'fa fa-check-square-o', 'get engaged'),
(2, 'Upcoming events', '#', 'fa fa-check-square-o', ''),
(3, 'Accessability', '#', 'fa fa-check-square-o', '');

-- --------------------------------------------------------

--
-- Table structure for table `appfooter_gettouch`
--

CREATE TABLE `appfooter_gettouch` (
  `id` bigint(20) NOT NULL,
  `heading` varchar(100) NOT NULL,
  `address` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `appfooter_gettouch`
--

INSERT INTO `appfooter_gettouch` (`id`, `heading`, `address`, `email`) VALUES
(1, 'get in touch', 'fdsjfdkhlkasklkl,\r\nkjdkdsjhlfda,\r\njdsskldhjkasj,\r\njhdkshdksfjkads.', 'bloodbank@gmail.com'),
(2, '', '', ''),
(3, '', '', ''),
(4, '', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `appfooter_socialicon`
--

CREATE TABLE `appfooter_socialicon` (
  `id` bigint(20) NOT NULL,
  `icon1` varchar(100) NOT NULL,
  `url1` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `appfooter_socialicon`
--

INSERT INTO `appfooter_socialicon` (`id`, `icon1`, `url1`) VALUES
(1, 'facebook.png', 'https://www.facebook.com/'),
(2, 'twitter.png', 'https://twitter.com'),
(3, 'instagram.png', 'https://www.instagram.com/'),
(4, 'youtube.png', 'https://youtube.com/');

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add appfooter', 7, 'add_appfooter'),
(26, 'Can change appfooter', 7, 'change_appfooter'),
(27, 'Can delete appfooter', 7, 'delete_appfooter'),
(28, 'Can view appfooter', 7, 'view_appfooter'),
(29, 'Can add appfooter1', 8, 'add_appfooter1'),
(30, 'Can change appfooter1', 8, 'change_appfooter1'),
(31, 'Can delete appfooter1', 8, 'delete_appfooter1'),
(32, 'Can view appfooter1', 8, 'view_appfooter1'),
(33, 'Can add appdown', 9, 'add_appdown'),
(34, 'Can change appdown', 9, 'change_appdown'),
(35, 'Can delete appdown', 9, 'delete_appdown'),
(36, 'Can view appdown', 9, 'view_appdown'),
(37, 'Can add gettouch', 10, 'add_gettouch'),
(38, 'Can change gettouch', 10, 'change_gettouch'),
(39, 'Can delete gettouch', 10, 'delete_gettouch'),
(40, 'Can view gettouch', 10, 'view_gettouch'),
(41, 'Can add socialicon', 11, 'add_socialicon'),
(42, 'Can change socialicon', 11, 'change_socialicon'),
(43, 'Can delete socialicon', 11, 'delete_socialicon'),
(44, 'Can view socialicon', 11, 'view_socialicon');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(9, 'appfooter', 'appdown'),
(7, 'appfooter', 'appfooter'),
(8, 'appfooter', 'appfooter1'),
(10, 'appfooter', 'gettouch'),
(11, 'appfooter', 'socialicon'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2023-08-07 12:51:32.383390'),
(2, 'auth', '0001_initial', '2023-08-07 12:51:32.967913'),
(3, 'admin', '0001_initial', '2023-08-07 12:51:33.176255'),
(4, 'admin', '0002_logentry_remove_auto_add', '2023-08-07 12:51:33.184393'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2023-08-07 12:51:33.200467'),
(6, 'appfooter', '0001_initial', '2023-08-07 12:51:33.292415'),
(7, 'contenttypes', '0002_remove_content_type_name', '2023-08-07 12:51:33.408124'),
(8, 'auth', '0002_alter_permission_name_max_length', '2023-08-07 12:51:33.507468'),
(9, 'auth', '0003_alter_user_email_max_length', '2023-08-07 12:51:33.564612'),
(10, 'auth', '0004_alter_user_username_opts', '2023-08-07 12:51:33.583082'),
(11, 'auth', '0005_alter_user_last_login_null', '2023-08-07 12:51:33.706359'),
(12, 'auth', '0006_require_contenttypes_0002', '2023-08-07 12:51:33.715680'),
(13, 'auth', '0007_alter_validators_add_error_messages', '2023-08-07 12:51:33.731791'),
(14, 'auth', '0008_alter_user_username_max_length', '2023-08-07 12:51:33.766749'),
(15, 'auth', '0009_alter_user_last_name_max_length', '2023-08-07 12:51:33.798747'),
(16, 'auth', '0010_alter_group_name_max_length', '2023-08-07 12:51:33.843852'),
(17, 'auth', '0011_update_proxy_permissions', '2023-08-07 12:51:33.861311'),
(18, 'auth', '0012_alter_user_first_name_max_length', '2023-08-07 12:51:33.922116'),
(19, 'sessions', '0001_initial', '2023-08-07 12:51:34.008030'),
(20, 'appfooter', '0002_appfooter1', '2023-08-07 13:05:39.663555'),
(21, 'appfooter', '0003_appdown', '2023-08-07 13:21:46.984715'),
(22, 'appfooter', '0004_appdown_url', '2023-08-07 13:24:02.497993'),
(23, 'appfooter', '0005_gettouch', '2023-08-08 03:19:18.408120'),
(24, 'appfooter', '0006_socialicon_remove_gettouch_icon1_and_more', '2023-08-08 08:03:09.231622');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `appfooter_appdown`
--
ALTER TABLE `appfooter_appdown`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `appfooter_appfooter`
--
ALTER TABLE `appfooter_appfooter`
  ADD PRIMARY KEY (`id`),
  ADD KEY `appfooter_appfooter_name_f9a2b20e` (`name`);

--
-- Indexes for table `appfooter_appfooter1`
--
ALTER TABLE `appfooter_appfooter1`
  ADD PRIMARY KEY (`id`),
  ADD KEY `appfooter_appfooter1_name_0764faf8` (`name`);

--
-- Indexes for table `appfooter_gettouch`
--
ALTER TABLE `appfooter_gettouch`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `appfooter_socialicon`
--
ALTER TABLE `appfooter_socialicon`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `appfooter_appdown`
--
ALTER TABLE `appfooter_appdown`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `appfooter_appfooter`
--
ALTER TABLE `appfooter_appfooter`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `appfooter_appfooter1`
--
ALTER TABLE `appfooter_appfooter1`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `appfooter_gettouch`
--
ALTER TABLE `appfooter_gettouch`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `appfooter_socialicon`
--
ALTER TABLE `appfooter_socialicon`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
