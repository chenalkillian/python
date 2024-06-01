-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : dim. 03 mars 2024 à 16:57
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `python`
--

-- --------------------------------------------------------

--
-- Structure de la table `liste_url`
--

CREATE TABLE `liste_url` (
  `id` int(11) NOT NULL,
  `nom_site` varchar(255) NOT NULL,
  `url` varchar(255) NOT NULL,
  `nom_user` varchar(255) NOT NULL,
  `count_elyes` mediumtext NOT NULL,
  `count_karim` mediumtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `liste_url`
--

INSERT INTO `liste_url` (`id`, `nom_site`, `url`, `nom_user`, `count_elyes`, `count_karim`) VALUES
(21, 'wikipedia', 'https://fr.wikipedia.org/', 'kiki', '{\'Contenu de la balise <h1> : \': \'Bienvenue sur Wikipédia\', \'Contenu de la balise <h2> : \': \'Wikipédia\', \'Contenu de la balise <h3> : \': \'Aucune balise <h3> trouvée.\', \'Nombre de balises <h2> : \': 8, \'Nombre de balises <h3> : \': 0, \'Nombre de balises <nav> : \': 9, \'nombre de nav : \': 9, \"Contenu de l\'attribut alt : \": \'Wikipédia\', \"Nombre total d\'imbrications de div : \": 179, \'Avertissement : \': \"Nombre d\'imbrications de div trop élevé.\", \'Nombre de liens de type ancre interne et externes : \': (214, 396)}', '{\'internal_links et external linls\': (216, 394)}'),
(22, 'gymshark', 'https://fr.gymshark.com/', 'kiki', '{\'Contenu de la balise <h1> : \': \'LES NOUVELLES TENUES DU MOIS\', \'Contenu de la balise <h2> : \': \'en savoir plus sur Gymshark\', \'Contenu de la balise <h3> : \': \'SHOP\', \'Nombre de balises <h2> : \': 1, \'Nombre de balises <h3> : \': 12, \'Nombre de balises <nav> : \': 1, \'nombre de nav : \': 1, \"Contenu de l\'attribut alt : \": \'Gymshark\', \"Nombre total d\'imbrications de div : \": 1171, \'Avertissement : \': \"Nombre d\'imbrications de div trop élevé.\", \'Nombre de liens de type ancre interne et externes : \': (17, 342)}', '{\'internal_links et external linls\': (320, 39)}'),
(23, 'apple.com', 'https://www.apple.com/', 'elyes', '{\'Contenu de la balise <h1> : \': \'Apple\', \'Contenu de la balise <h2> : \': \'iPhone 15 Pro\', \'Contenu de la balise <h3> : \': \'Titanium. So strong. So light. So Pro.\', \'Nombre de balises <h2> : \': 4, \'Nombre de balises <h3> : \': 14, \'Nombre de balises <nav> : \': 2, \'nombre de nav : \': 2, \"Contenu de l\'attribut alt : \": None, \"Nombre total d\'imbrications de div : \": 111, \'Avertissement : \': \"Nombre d\'imbrications de div trop élevé.\", \'Nombre de liens de type ancre interne et externes : \': (105, 9)}', '{\'internal_links et external linls\': (105, 9)}');

-- --------------------------------------------------------

--
-- Structure de la table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `mot_de_passe` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `user`
--

INSERT INTO `user` (`id`, `email`, `mot_de_passe`) VALUES
(5, 'elyes', 'pbkdf2:sha256:600000$0ca4m6FTKbFEs51h$1794a4bd7a2fdbaee15d85403ff49e5995811839472b576440c9d224d724aff3'),
(6, 'kiki', 'pbkdf2:sha256:600000$vTvWyxPVNjFNWO5p$889a338f0c8fac1a193954bd4b974712d2b6a648be2a5f7fb6187b63a2298ca0'),
(16, 'françois', 'pbkdf2:sha256:600000$f13M7n2R0Xxy5rHo$19eb5dc526d35c7d22a2ea7aedcfaa52f07fb5d670511c538a99d74b81cb27f5');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `liste_url`
--
ALTER TABLE `liste_url`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nom_site` (`nom_site`);

--
-- Index pour la table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `liste_url`
--
ALTER TABLE `liste_url`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT pour la table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
