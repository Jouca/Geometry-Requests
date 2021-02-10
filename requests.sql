-- phpMyAdmin SQL Dump
-- version 4.6.6deb4
-- https://www.phpmyadmin.net/
--
-- Client :  localhost:3306
-- Généré le :  Mer 10 Février 2021 à 14:49
-- Version du serveur :  10.1.41-MariaDB-0+deb9u1
-- Version de PHP :  7.0.33-0+deb9u6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `requests`
--
CREATE DATABASE IF NOT EXISTS `requests` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `requests`;

-- --------------------------------------------------------

--
-- Structure de la table `banned`
--

DROP TABLE IF EXISTS `banned`;
CREATE TABLE `banned` (
  `userid` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `cooldowns`
--

DROP TABLE IF EXISTS `cooldowns`;
CREATE TABLE `cooldowns` (
  `userid` bigint(25) NOT NULL,
  `cooldown` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `GDmoderators`
--

DROP TABLE IF EXISTS `GDmoderators`;
CREATE TABLE `GDmoderators` (
  `moderatorname` varchar(25) DEFAULT NULL,
  `userid` varchar(25) NOT NULL,
  `serverid` varchar(25) NOT NULL,
  `ID` int(255) NOT NULL,
  `Modtype` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `GRmoderators`
--

DROP TABLE IF EXISTS `GRmoderators`;
CREATE TABLE `GRmoderators` (
  `userid` varchar(25) NOT NULL,
  `name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `levels`
--

DROP TABLE IF EXISTS `levels`;
CREATE TABLE `levels` (
  `ID` int(11) NOT NULL,
  `levelid` int(11) NOT NULL,
  `requester` bigint(25) NOT NULL,
  `server` bigint(20) NOT NULL,
  `video` varchar(50) DEFAULT NULL,
  `reviewed` varchar(5) NOT NULL,
  `messageid` bigint(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `maintenance`
--

DROP TABLE IF EXISTS `maintenance`;
CREATE TABLE `maintenance` (
  `reqhelp` int(4) NOT NULL,
  `reqabout` int(4) NOT NULL,
  `reqsetup` int(4) NOT NULL,
  `reqsetconfig` int(4) NOT NULL,
  `reqsearch` int(4) NOT NULL,
  `reqlevel` int(4) NOT NULL,
  `reqqueue` int(4) NOT NULL,
  `reqmyqueue` int(4) NOT NULL,
  `reqreview` int(4) NOT NULL,
  `reqsend` int(4) NOT NULL,
  `reqreport` int(4) NOT NULL,
  `reqmodapprove` int(4) NOT NULL,
  `reqmodunapprove` int(4) NOT NULL,
  `reqmodban` int(4) NOT NULL,
  `reqmodunban` int(4) NOT NULL,
  `reqprofilelink` int(4) NOT NULL,
  `reqprofileunlink` int(4) NOT NULL,
  `reqannouncement` int(4) NOT NULL,
  `reqachievements` int(4) NOT NULL,
  `reqachievementgive` int(4) NOT NULL,
  `reqachievementremove` int(4) NOT NULL,
  `reqprofile` int(4) NOT NULL,
  `reqsettingsprofile` int(4) NOT NULL,
  `reqsetsettingsprofile` int(4) NOT NULL,
  `reqleaderboard` int(4) NOT NULL,
  `reqremove` int(4) NOT NULL,
  `ID` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `modlist`
--

DROP TABLE IF EXISTS `modlist`;
CREATE TABLE `modlist` (
  `username` varchar(26) NOT NULL,
  `accountID` int(11) NOT NULL,
  `playerID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `reports`
--

DROP TABLE IF EXISTS `reports`;
CREATE TABLE `reports` (
  `ID` int(11) NOT NULL,
  `levelid` int(11) NOT NULL,
  `isBlacklist` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `rewards`
--

DROP TABLE IF EXISTS `rewards`;
CREATE TABLE `rewards` (
  `userid` bigint(25) NOT NULL,
  `ship1` bigint(11) NOT NULL DEFAULT '0',
  `ship2` bigint(11) NOT NULL DEFAULT '0',
  `ship3` bigint(11) NOT NULL DEFAULT '0',
  `ship4` bigint(11) NOT NULL DEFAULT '0',
  `ship5` bigint(11) NOT NULL DEFAULT '0',
  `ship6` bigint(11) NOT NULL DEFAULT '0',
  `ship7` bigint(11) NOT NULL DEFAULT '0',
  `ship8` bigint(11) NOT NULL DEFAULT '0',
  `ship9` bigint(11) NOT NULL DEFAULT '0',
  `ship10` bigint(11) NOT NULL DEFAULT '0',
  `ship11` bigint(11) NOT NULL DEFAULT '0',
  `ship12` bigint(11) NOT NULL DEFAULT '0',
  `ship13` bigint(11) NOT NULL DEFAULT '0',
  `ship14` bigint(11) NOT NULL DEFAULT '0',
  `ship15` bigint(11) NOT NULL DEFAULT '0',
  `ship16` bigint(11) NOT NULL DEFAULT '0',
  `ship17` bigint(11) NOT NULL DEFAULT '0',
  `ship18` bigint(11) NOT NULL DEFAULT '0',
  `ship19` bigint(11) NOT NULL DEFAULT '0',
  `ship20` bigint(11) NOT NULL DEFAULT '0',
  `ship21` bigint(11) NOT NULL DEFAULT '0',
  `ship22` bigint(11) NOT NULL DEFAULT '0',
  `ship23` bigint(11) NOT NULL DEFAULT '0',
  `ship24` bigint(11) NOT NULL DEFAULT '0',
  `ship25` bigint(11) NOT NULL DEFAULT '0',
  `ship26` bigint(11) NOT NULL DEFAULT '0',
  `ship27` bigint(11) NOT NULL DEFAULT '0',
  `ship28` bigint(11) NOT NULL DEFAULT '0',
  `ship29` bigint(11) NOT NULL DEFAULT '0',
  `ship30` bigint(11) NOT NULL DEFAULT '0',
  `ship31` bigint(11) NOT NULL DEFAULT '0',
  `ship32` bigint(11) NOT NULL DEFAULT '0',
  `ship33` bigint(11) NOT NULL DEFAULT '0',
  `ship34` bigint(11) NOT NULL DEFAULT '0',
  `ship35` bigint(11) NOT NULL DEFAULT '0',
  `ship36` bigint(11) NOT NULL DEFAULT '0',
  `ship37` bigint(11) NOT NULL DEFAULT '0',
  `ship38` bigint(11) NOT NULL DEFAULT '0',
  `ship39` bigint(11) NOT NULL DEFAULT '0',
  `ship40` bigint(11) NOT NULL DEFAULT '0',
  `ship41` bigint(11) NOT NULL DEFAULT '0',
  `ship42` bigint(11) NOT NULL DEFAULT '0',
  `ship43` bigint(11) NOT NULL DEFAULT '0',
  `ship44` bigint(11) NOT NULL DEFAULT '0',
  `ship45` bigint(11) NOT NULL DEFAULT '0',
  `ship46` bigint(11) NOT NULL DEFAULT '0',
  `ship47` bigint(11) NOT NULL DEFAULT '0',
  `ship48` bigint(11) NOT NULL DEFAULT '0',
  `ship49` bigint(11) NOT NULL DEFAULT '0',
  `ship50` bigint(11) NOT NULL DEFAULT '0',
  `ship51` bigint(11) NOT NULL DEFAULT '0',
  `ball1` bigint(11) NOT NULL DEFAULT '0',
  `ball2` bigint(11) NOT NULL DEFAULT '0',
  `ball3` bigint(11) NOT NULL DEFAULT '0',
  `ball4` bigint(11) NOT NULL DEFAULT '0',
  `ball5` bigint(11) NOT NULL DEFAULT '0',
  `ball6` bigint(11) NOT NULL DEFAULT '0',
  `ball7` bigint(11) NOT NULL DEFAULT '0',
  `ball8` bigint(11) NOT NULL DEFAULT '0',
  `ball9` bigint(11) NOT NULL DEFAULT '0',
  `ball10` bigint(11) NOT NULL DEFAULT '0',
  `ball11` bigint(11) NOT NULL DEFAULT '0',
  `ball12` bigint(11) NOT NULL DEFAULT '0',
  `ball13` bigint(11) NOT NULL DEFAULT '0',
  `ball14` bigint(11) NOT NULL DEFAULT '0',
  `ball15` bigint(11) NOT NULL DEFAULT '0',
  `ball16` bigint(11) NOT NULL DEFAULT '0',
  `ball17` bigint(11) NOT NULL DEFAULT '0',
  `ball18` bigint(11) NOT NULL DEFAULT '0',
  `ball19` bigint(11) NOT NULL DEFAULT '0',
  `ball20` bigint(11) NOT NULL DEFAULT '0',
  `ball21` bigint(11) NOT NULL DEFAULT '0',
  `ball22` bigint(11) NOT NULL DEFAULT '0',
  `ball23` bigint(11) NOT NULL DEFAULT '0',
  `ball24` bigint(11) NOT NULL DEFAULT '0',
  `ball25` bigint(11) NOT NULL DEFAULT '0',
  `ball26` bigint(11) NOT NULL DEFAULT '0',
  `ball27` bigint(11) NOT NULL DEFAULT '0',
  `ball28` bigint(11) NOT NULL DEFAULT '0',
  `ball29` bigint(11) NOT NULL DEFAULT '0',
  `ball30` bigint(11) NOT NULL DEFAULT '0',
  `ball31` bigint(11) NOT NULL DEFAULT '0',
  `ball32` bigint(11) NOT NULL DEFAULT '0',
  `ball33` bigint(11) NOT NULL DEFAULT '0',
  `ball34` bigint(11) NOT NULL DEFAULT '0',
  `ball35` bigint(11) NOT NULL DEFAULT '0',
  `ball36` bigint(11) NOT NULL DEFAULT '0',
  `ball37` bigint(11) NOT NULL DEFAULT '0',
  `ball38` bigint(11) NOT NULL DEFAULT '0',
  `ball39` bigint(11) NOT NULL DEFAULT '0',
  `ball40` bigint(11) NOT NULL DEFAULT '0',
  `ball41` bigint(11) NOT NULL DEFAULT '0',
  `ball42` bigint(11) NOT NULL DEFAULT '0',
  `ball43` bigint(11) NOT NULL DEFAULT '0',
  `ufo1` bigint(11) NOT NULL DEFAULT '0',
  `ufo2` bigint(11) NOT NULL DEFAULT '0',
  `ufo3` bigint(11) NOT NULL DEFAULT '0',
  `ufo4` bigint(11) NOT NULL DEFAULT '0',
  `ufo5` bigint(11) NOT NULL DEFAULT '0',
  `ufo6` bigint(11) NOT NULL DEFAULT '0',
  `ufo7` bigint(11) NOT NULL DEFAULT '0',
  `ufo8` bigint(11) NOT NULL DEFAULT '0',
  `ufo9` bigint(11) NOT NULL DEFAULT '0',
  `ufo10` bigint(11) NOT NULL DEFAULT '0',
  `ufo11` bigint(11) NOT NULL DEFAULT '0',
  `ufo12` bigint(11) NOT NULL DEFAULT '0',
  `ufo13` bigint(11) NOT NULL DEFAULT '0',
  `ufo14` bigint(11) NOT NULL DEFAULT '0',
  `ufo15` bigint(11) NOT NULL DEFAULT '0',
  `ufo16` bigint(11) NOT NULL DEFAULT '0',
  `ufo17` bigint(11) NOT NULL DEFAULT '0',
  `ufo18` bigint(11) NOT NULL DEFAULT '0',
  `ufo19` bigint(11) NOT NULL DEFAULT '0',
  `ufo20` bigint(11) NOT NULL DEFAULT '0',
  `ufo21` bigint(11) NOT NULL DEFAULT '0',
  `ufo22` bigint(11) NOT NULL DEFAULT '0',
  `ufo23` bigint(11) NOT NULL DEFAULT '0',
  `ufo24` bigint(11) NOT NULL DEFAULT '0',
  `ufo25` bigint(11) NOT NULL DEFAULT '0',
  `ufo26` bigint(11) NOT NULL DEFAULT '0',
  `ufo27` bigint(11) NOT NULL DEFAULT '0',
  `ufo28` bigint(11) NOT NULL DEFAULT '0',
  `ufo29` bigint(11) NOT NULL DEFAULT '0',
  `ufo30` bigint(11) NOT NULL DEFAULT '0',
  `ufo31` bigint(11) NOT NULL DEFAULT '0',
  `ufo32` bigint(11) NOT NULL DEFAULT '0',
  `ufo33` bigint(11) NOT NULL DEFAULT '0',
  `ufo34` bigint(11) NOT NULL DEFAULT '0',
  `ufo35` bigint(11) NOT NULL DEFAULT '0',
  `wave1` bigint(11) NOT NULL DEFAULT '0',
  `wave2` bigint(11) NOT NULL DEFAULT '0',
  `wave3` bigint(11) NOT NULL DEFAULT '0',
  `wave4` bigint(11) NOT NULL DEFAULT '0',
  `wave5` bigint(11) NOT NULL DEFAULT '0',
  `wave6` bigint(11) NOT NULL DEFAULT '0',
  `wave7` bigint(11) NOT NULL DEFAULT '0',
  `wave8` bigint(11) NOT NULL DEFAULT '0',
  `wave9` bigint(11) NOT NULL DEFAULT '0',
  `wave10` bigint(11) NOT NULL DEFAULT '0',
  `wave11` bigint(11) NOT NULL DEFAULT '0',
  `wave12` bigint(11) NOT NULL DEFAULT '0',
  `wave13` bigint(11) NOT NULL DEFAULT '0',
  `wave14` bigint(11) NOT NULL DEFAULT '0',
  `wave15` bigint(11) NOT NULL DEFAULT '0',
  `wave16` bigint(11) NOT NULL DEFAULT '0',
  `wave17` bigint(11) NOT NULL DEFAULT '0',
  `wave18` bigint(11) NOT NULL DEFAULT '0',
  `wave19` bigint(11) NOT NULL DEFAULT '0',
  `wave20` bigint(11) NOT NULL DEFAULT '0',
  `wave21` bigint(11) NOT NULL DEFAULT '0',
  `wave22` bigint(11) NOT NULL DEFAULT '0',
  `wave23` bigint(11) NOT NULL DEFAULT '0',
  `wave24` bigint(11) NOT NULL DEFAULT '0',
  `wave25` bigint(11) NOT NULL DEFAULT '0',
  `wave26` bigint(11) NOT NULL DEFAULT '0',
  `wave27` bigint(11) NOT NULL DEFAULT '0',
  `wave28` bigint(11) NOT NULL DEFAULT '0',
  `wave29` bigint(11) NOT NULL DEFAULT '0',
  `wave30` bigint(11) NOT NULL DEFAULT '0',
  `wave31` bigint(11) NOT NULL DEFAULT '0',
  `wave32` bigint(11) NOT NULL DEFAULT '0',
  `wave33` bigint(11) NOT NULL DEFAULT '0',
  `wave34` bigint(11) NOT NULL DEFAULT '0',
  `wave35` bigint(11) NOT NULL DEFAULT '0',
  `robot1` bigint(11) NOT NULL DEFAULT '0',
  `robot2` bigint(11) NOT NULL DEFAULT '0',
  `robot3` bigint(11) NOT NULL DEFAULT '0',
  `robot4` bigint(11) NOT NULL DEFAULT '0',
  `robot5` bigint(11) NOT NULL DEFAULT '0',
  `robot6` bigint(11) NOT NULL DEFAULT '0',
  `robot7` bigint(11) NOT NULL DEFAULT '0',
  `robot8` bigint(11) NOT NULL DEFAULT '0',
  `robot9` bigint(11) NOT NULL DEFAULT '0',
  `robot10` bigint(11) NOT NULL DEFAULT '0',
  `robot11` bigint(11) NOT NULL DEFAULT '0',
  `robot12` bigint(11) NOT NULL DEFAULT '0',
  `robot13` bigint(11) NOT NULL DEFAULT '0',
  `robot14` bigint(11) NOT NULL DEFAULT '0',
  `robot15` bigint(11) NOT NULL DEFAULT '0',
  `robot16` bigint(11) NOT NULL DEFAULT '0',
  `robot17` bigint(11) NOT NULL DEFAULT '0',
  `robot18` bigint(11) NOT NULL DEFAULT '0',
  `robot19` bigint(11) NOT NULL DEFAULT '0',
  `robot20` bigint(11) NOT NULL DEFAULT '0',
  `robot21` bigint(11) NOT NULL DEFAULT '0',
  `robot22` bigint(11) NOT NULL DEFAULT '0',
  `robot23` bigint(11) NOT NULL DEFAULT '0',
  `robot24` bigint(11) NOT NULL DEFAULT '0',
  `robot25` bigint(11) NOT NULL DEFAULT '0',
  `robot26` bigint(11) NOT NULL DEFAULT '0',
  `spider1` bigint(11) NOT NULL DEFAULT '0',
  `spider2` bigint(11) NOT NULL DEFAULT '0',
  `spider3` bigint(11) NOT NULL DEFAULT '0',
  `spider4` bigint(11) NOT NULL DEFAULT '0',
  `spider5` bigint(11) NOT NULL DEFAULT '0',
  `spider6` bigint(11) NOT NULL DEFAULT '0',
  `spider7` bigint(11) NOT NULL DEFAULT '0',
  `spider8` bigint(11) NOT NULL DEFAULT '0',
  `spider9` bigint(11) NOT NULL DEFAULT '0',
  `spider10` bigint(11) NOT NULL DEFAULT '0',
  `spider11` bigint(11) NOT NULL DEFAULT '0',
  `spider12` bigint(11) NOT NULL DEFAULT '0',
  `spider13` bigint(11) NOT NULL DEFAULT '0',
  `spider14` bigint(11) NOT NULL DEFAULT '0',
  `spider15` bigint(11) NOT NULL DEFAULT '0',
  `spider16` bigint(11) NOT NULL DEFAULT '0',
  `spider17` bigint(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `setup`
--

DROP TABLE IF EXISTS `setup`;
CREATE TABLE `setup` (
  `ID` int(11) NOT NULL,
  `serverid` varchar(25) NOT NULL,
  `ReviewerRole` varchar(25) DEFAULT NULL,
  `OwnerRole` varchar(25) DEFAULT NULL,
  `RequestChannel` bigint(20) DEFAULT NULL,
  `ReviewChannel` bigint(20) DEFAULT NULL,
  `CheckedReviewChannel` varchar(25) DEFAULT NULL,
  `AnnouncementBot` bigint(20) DEFAULT NULL,
  `GDModChannel` varchar(25) DEFAULT NULL,
  `TagReviewer` varchar(10) NOT NULL,
  `NeedVideo` varchar(10) NOT NULL,
  `language` varchar(8) NOT NULL,
  `RemoveRated` varchar(10) NOT NULL,
  `GDModCheckedChannel` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `tokenrewards`
--

DROP TABLE IF EXISTS `tokenrewards`;
CREATE TABLE `tokenrewards` (
  `ID` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `amount` int(20) NOT NULL,
  `percentage` decimal(4,2) NOT NULL,
  `rarity` varchar(15) NOT NULL,
  `thumbnail` text NOT NULL,
  `nameid` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `tokens`
--

DROP TABLE IF EXISTS `tokens`;
CREATE TABLE `tokens` (
  `ID` int(10) NOT NULL,
  `token` varchar(10) NOT NULL,
  `client` bigint(25) NOT NULL,
  `timestamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `chesttype` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `ID` int(11) NOT NULL,
  `userid` varchar(25) NOT NULL,
  `levelrequestedcount` int(10) NOT NULL,
  `levelreviewedcount` int(11) NOT NULL,
  `levelreviewapprovedcount` int(11) NOT NULL,
  `levelreviewunapprovedcount` int(11) NOT NULL,
  `requestachievement1` varchar(10) NOT NULL,
  `requestachievement5` varchar(10) NOT NULL,
  `requestachievement10` varchar(10) NOT NULL,
  `requestachievement50` varchar(10) NOT NULL,
  `requestachievement100` varchar(10) NOT NULL,
  `reviewachievement1` varchar(10) NOT NULL,
  `reviewachievement5` varchar(10) NOT NULL,
  `reviewachievement10` varchar(10) NOT NULL,
  `reviewachievement50` varchar(10) NOT NULL,
  `reviewachievement100` varchar(10) NOT NULL,
  `reviewapprovedachievement1` varchar(10) NOT NULL,
  `reviewapprovedachievement5` varchar(10) NOT NULL,
  `reviewapprovedachievement10` varchar(10) NOT NULL,
  `reviewapprovedachievement50` varchar(10) NOT NULL,
  `reviewapprovedachievement100` varchar(10) NOT NULL,
  `reviewunapprovedachievement1` varchar(10) NOT NULL,
  `reviewunapprovedachievement5` varchar(10) NOT NULL,
  `reviewunapprovedachievement10` varchar(10) NOT NULL,
  `reviewunapprovedachievement50` varchar(10) NOT NULL,
  `reviewunapprovedachievement100` varchar(10) NOT NULL,
  `levelsentbygdmod` varchar(10) NOT NULL,
  `firstsync` varchar(10) NOT NULL,
  `suggestidea` varchar(10) NOT NULL,
  `approvedidea` varchar(10) NOT NULL,
  `approvedreport` varchar(10) NOT NULL,
  `language` varchar(6) NOT NULL,
  `isCubeUnlocked` int(2) NOT NULL,
  `cubetype` int(4) NOT NULL,
  `color1` varchar(10) NOT NULL,
  `color2` varchar(10) NOT NULL,
  `glowoutline` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Index pour les tables exportées
--

--
-- Index pour la table `banned`
--
ALTER TABLE `banned`
  ADD UNIQUE KEY `userid` (`userid`);

--
-- Index pour la table `cooldowns`
--
ALTER TABLE `cooldowns`
  ADD UNIQUE KEY `userid_2` (`userid`),
  ADD KEY `userid` (`userid`);

--
-- Index pour la table `GDmoderators`
--
ALTER TABLE `GDmoderators`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `ID` (`ID`);

--
-- Index pour la table `GRmoderators`
--
ALTER TABLE `GRmoderators`
  ADD UNIQUE KEY `userid` (`userid`);

--
-- Index pour la table `levels`
--
ALTER TABLE `levels`
  ADD PRIMARY KEY (`ID`);

--
-- Index pour la table `maintenance`
--
ALTER TABLE `maintenance`
  ADD PRIMARY KEY (`ID`);

--
-- Index pour la table `modlist`
--
ALTER TABLE `modlist`
  ADD PRIMARY KEY (`username`),
  ADD UNIQUE KEY `username` (`username`),
  ADD KEY `username_2` (`username`);

--
-- Index pour la table `reports`
--
ALTER TABLE `reports`
  ADD PRIMARY KEY (`ID`);

--
-- Index pour la table `rewards`
--
ALTER TABLE `rewards`
  ADD UNIQUE KEY `userid` (`userid`),
  ADD KEY `userid_2` (`userid`);

--
-- Index pour la table `setup`
--
ALTER TABLE `setup`
  ADD PRIMARY KEY (`ID`);

--
-- Index pour la table `tokenrewards`
--
ALTER TABLE `tokenrewards`
  ADD PRIMARY KEY (`ID`);

--
-- Index pour la table `tokens`
--
ALTER TABLE `tokens`
  ADD PRIMARY KEY (`ID`);

--
-- Index pour la table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `ID` (`ID`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `levels`
--
ALTER TABLE `levels`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2110;
--
-- AUTO_INCREMENT pour la table `maintenance`
--
ALTER TABLE `maintenance`
  MODIFY `ID` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT pour la table `reports`
--
ALTER TABLE `reports`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT pour la table `setup`
--
ALTER TABLE `setup`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=247;
--
-- AUTO_INCREMENT pour la table `tokenrewards`
--
ALTER TABLE `tokenrewards`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=369;
--
-- AUTO_INCREMENT pour la table `tokens`
--
ALTER TABLE `tokens`
  MODIFY `ID` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT pour la table `users`
--
ALTER TABLE `users`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=570;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
