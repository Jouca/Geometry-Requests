-- phpMyAdmin SQL Dump
-- version 4.6.6deb4
-- https://www.phpmyadmin.net/
--
-- Client :  localhost:3306
-- Généré le :  Mer 12 Août 2020 à 18:50
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

-- --------------------------------------------------------

--
-- Structure de la table `banned`
--

CREATE TABLE `banned` (
  `userid` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `GDmoderators`
--

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

CREATE TABLE `GRmoderators` (
  `userid` varchar(25) NOT NULL,
  `name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `levels`
--

CREATE TABLE `levels` (
  `ID` int(11) NOT NULL,
  `levelid` int(11) NOT NULL,
  `requester` bigint(25) NOT NULL,
  `server` bigint(20) NOT NULL,
  `video` varchar(50) DEFAULT NULL,
  `reviewed` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `reports`
--

CREATE TABLE `reports` (
  `ID` int(11) NOT NULL,
  `levelid` int(11) NOT NULL,
  `isBlacklist` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `setup`
--

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
  `language` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

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
-- Index pour la table `reports`
--
ALTER TABLE `reports`
  ADD PRIMARY KEY (`ID`);

--
-- Index pour la table `setup`
--
ALTER TABLE `setup`
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
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=521;
--
-- AUTO_INCREMENT pour la table `reports`
--
ALTER TABLE `reports`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT pour la table `setup`
--
ALTER TABLE `setup`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=121;
--
-- AUTO_INCREMENT pour la table `users`
--
ALTER TABLE `users`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=169;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
