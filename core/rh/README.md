# DATABASES

sql and nosql

## SQL

base de donnees relationel

### I- DATABASE

#### 23. BACKUP DATABASE

L'instruction BACKUP DATABASE est utilisée dans SQL Server pour créer une sauvegarde complète d'une base de données SQL existante.

```sql
BACKUP DATABASE databasename
TO DISK = 'filepath';
```

Une sauvegarde différentielle ne sauvegarde que les parties de la base de données qui ont été modifiées depuis la dernière sauvegarde complète de la base de données.

```sql
BACKUP DATABASE databasename
TO DISK = 'filepath'
WITH DIFFERENTIAL;

BACKUP DATABASE testDB
TO DISK = 'D:\backups\testDB.bak';

BACKUP DATABASE testDB
TO DISK = 'D:\backups\testDB.bak'
WITH DIFFERENTIAL;
```

#### 15. CREATE DATABASE

La création d’une base de données en SQL est possible en ligne de commande. Même si les systèmes de gestion de base de données (SGBD) sont souvent utilisés pour créer une base, il convient de connaître la commande à utiliser, qui est très simple.

```sql
CREATE DATABASE ma_base

CREATE DATABASE IF NOT EXISTS ma_base
```

#### 16. DROP DATABASE

En SQL, la commande DROP DATABASE permet de supprimer totalement une base de données et tout ce qu’elle contient. Cette commande est à utiliser avec beaucoup d’attention car elle permet de supprimer tout ce qui est inclus dans une base: les tables, les données, les index …

```sql
DROP DATABASE ma_base

DROP DATABASE IF EXISTS ma_base
```

### II- TABLE

#### 17. CREATE TABLE

La commande CREATE TABLE permet de créer une table en SQL. Un tableau est une entité qui est contenu dans une base de données pour stocker des données ordonnées dans des colonnes. La création d’une table sert à définir les colonnes et le type de données qui seront contenus dans chacun des colonne (entier, chaîne de caractères, date, valeur binaire …).

```sql
CREATE TABLE nom_de_la_table
(
    colonne1 type_donnees,
    colonne2 type_donnees,
    colonne3 type_donnees,
    colonne4 type_donnees
)

CREATE TABLE utilisateur
(
    id INT PRIMARY KEY NOT NULL,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    email VARCHAR(255),
    date_naissance DATE,
    pays VARCHAR(255),
    ville VARCHAR(255),
    code_postal VARCHAR(5),
    nombre_achat INT
)

CREATE TABLE `nom_de_la_table` (
  id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  [...]
);

CREATE TABLE `nom_de_la_table` (
  `id` INT NOT NULL AUTO_INCREMENT,
  [...],
  PRIMARY KEY (`id`)
);

CREATE TABLE `nom_de__la_table` (
  id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  [...]
);

ALTER TABLE `nom_de__la_table` AUTO_INCREMENT=50;
```

#### 18. ALTER TABLE

La commande ALTER TABLE en SQL permet de modifier une table existante. Idéal pour ajouter une colonne, supprimer une colonne ou modifier une colonne existante, par exemple pour changer le type.

```sql
ALTER TABLE nom_table
instruction

ALTER TABLE nom_table
ADD nom_colonne type_donnees

ALTER TABLE utilisateur
ADD adresse_rue VARCHAR(255)

ALTER TABLE nom_table
DROP nom_colonne

MySQL
ALTER TABLE nom_table
MODIFY nom_colonne type_donnees

ALTER TABLE nom_table
CHANGE colonne_ancien_nom colonne_nouveau_nom type_donnees

PostgreSQL
ALTER TABLE nom_table
ALTER COLUMN nom_colonne TYPE type_donnees

TER TABLE nom_table
RENAME COLUMN colonne_ancien_nom TO colonne_nouveau_nom
```

#### 19. DROP TABLE

La commande DROP TABLE en SQL permet de supprimer définitivement une table d’une base de données. Cela supprime en même temps les éventuels index, trigger, contraintes et permissions associées à cette table.

```sql
DROP TABLE nom_table

```

### III- ROWS

#### 1. SELECT

SELECT nom_du_champ FROM nom_du_tableau

```sql
SELECT * FROM tablename
```

##### 1.1 DISTINCT

L’utilisation de la commande SELECT en SQL permet de lire toutes les données d’une ou plusieurs colonnes. Cette commande peut potentiellement afficher des lignes en doubles. Pour éviter des redondances dans les résultats il faut simplement ajouter DISTINCT après le mot SELECT.

```sql
SELECT DISTINCT ma_colonne
FROM nom_du_tableau
```

#### 2. WHERE

La commande WHERE dans une requête SQL permet d’extraire les lignes d’une base de données qui respectent une condition. Cela permet d’obtenir uniquement les informations désirées.

```sql
SELECT nom_colonnes FROM nom_table WHERE condition
```

operator:

- =                 Égale
- <>                Pas égale
- !=                Pas égale

- <                 Inférieur à
- >=                Supérieur ou égale à
- <=                Inférieur ou égale à
- IN                Liste de plusieurs valeurs possibles
- BETWEEN           Valeur comprise dans un intervalle donnée (utile pour les nombres ou dates)
- LIKE              Recherche en spécifiant le début, milieu ou fin d'un mot.
- IS NULL           Valeur est nulle
- IS NOT NULL       Valeur n'est pas nulle

##### 2.1 AND & OR

```sql
SELECT nom_colonnes
FROM nom_table
WHERE condition1 AND condition2

SELECT nom_colonnes FROM nom_table
WHERE condition1 OR condition2

SELECT nom_colonnes FROM nom_table
WHERE condition1 AND (condition2 OR condition3)

SELECT * FROM produit
WHERE categorie = 'informatique' AND stock < 20

SELECT * FROM produit
WHERE nom = 'ordinateur' OR nom = 'clavier'

SELECT * FROM produit
WHERE ( categorie = 'informatique' AND stock < 20 )
OR ( categorie = 'fourniture' AND stock < 200 )
```

##### 2.2 IN

```sql
SELECT nom_colonne
FROM table
WHERE nom_colonne IN ( valeur1, valeur2, valeur3, ... )
```

##### 2.3 BETWEEN

L’opérateur BETWEEN est utilisé dans une requête SQL pour sélectionner un intervalle de données dans une requête utilisant WHERE

```sql
SELECT *
FROM table
WHERE nom_colonne BETWEEN 'valeur1' AND 'valeur2'

SELECT *
FROM utilisateur
WHERE date_inscription BETWEEN ‘2012-04-01’ AND ‘2012-04-20’

SELECT *
FROM utilisateur
WHERE id NOT BETWEEN 4 AND 10
```

##### 2.3 LIKE

L’opérateur LIKE est utilisé dans la clause WHERE des requêtes SQL. Ce mot-clé permet d’effectuer une recherche sur un modèle particulier. Il est par exemple possible de rechercher les enregistrements dont la valeur d’une colonne commence par telle ou telle lettre. Les modèles de recherches sont multiple.

```sql
SELECT *
FROM table
WHERE colonne LIKE modele

SELECT *
FROM client
WHERE ville LIKE 'N%'

SELECT *
FROM client
WHERE ville LIKE '%e'
```

- LIKE ‘%a’ : le caractère “%” est un caractère joker qui remplace tous les autres caractères. Ainsi, ce modèle permet de rechercher toutes les chaines de caractère qui se termine par un “a”.
- LIKE ‘a%’ : ce modèle permet de rechercher toutes les lignes de “colonne” qui commence par un “a”.
- LIKE ‘%a%’ : ce modèle est utilisé pour rechercher tous les enregistrement qui utilisent le caractère “a”.
- LIKE ‘pa%on’ : ce modèle permet de rechercher les chaines qui commence par “pa” et qui se terminent par “on”, comme “pantalon” ou “pardon”.
- LIKE ‘a_c’ : peu utilisé, le caractère “_” (underscore) peut être remplacé par n’importe quel caractère, mais un seul caractère uniquement (alors que le symbole pourcentage “%” peut être remplacé par un nombre incalculable de caractères . Ainsi, ce modèle permet de retourner les lignes “aac”, “abc” ou même “azc”.

##### 2.4 IS NULL / IS NOT NULL

Dans le langage SQL, l’opérateur IS permet de filtrer les résultats qui contiennent la valeur NULL. Cet opérateur est indispensable car la valeur NULL est une valeur inconnue et ne peut par conséquent pas être filtrée par les opérateurs de comparaison (cf. égal, inférieur, supérieur ou différent).

```sql
SELECT *
FROM `table`
WHERE nom_colonne IS NULL

SELECT *
FROM `table`
WHERE nom_colonne IS NOT NULL

```

#### 3. GROUP BY

La commande GROUP BY est utilisée en SQL pour grouper plusieurs résultats et utiliser une fonction de totaux sur un groupe de résultat. Sur une table qui contient toutes les ventes d’un magasin, il est par exemple possible de liste regrouper les ventes par clients identiques et d’obtenir le coût total des achats pour chaque client.

```sql
SELECT colonne1, fonction(colonne2)
FROM table
GROUP BY colonne1

SELECT client, SUM(tarif)
FROM achat
GROUP BY client
```

##### 3.1 GROUP BY WITH ROLLUP

La commande GROUP BY est utilisée en SQL pour grouper plusieurs résultats et utiliser des fonctions sur le groupement. L’ajout de la commande WITH ROLLUP permet quant à elle d’ajouter une ligne supplémentaire qui fonctionne tel qu’un système de “super-agrégateur” sur l’ensemble des résultats.

```sql
SELECT colonne1, fonction(colonne2)
FROM table
GROUP BY colonne1 WITH ROLLUP

SELECT `code_postal`, COUNT(*), SUM(`commande`), MIN(`date_inscription`), MAX(`date_inscription`)
FROM `client`
GROUP BY code_postal WITH ROLLUP
```

#### 4. HAVING

La condition HAVING en SQL est presque similaire à WHERE à la seule différence que HAVING permet de filtrer en utilisant des fonctions telles que SUM(), COUNT(), AVG(), MIN() ou MAX().

```sql
SELECT colonne1, SUM(colonne2)
FROM nom_table
GROUP BY colonne1
HAVING fonction(colonne2) operateur valeur

SELECT client, SUM(tarif)
FROM achat
GROUP BY client
HAVING SUM(tarif) > 40
```

#### 5. ORDER BY

La commande ORDER BY permet de trier les lignes dans un résultat d’une requête SQL. Il est possible de trier les données sur une ou plusieurs colonnes, par ordre ascendant ou descendant.

```sql
SELECT colonne1, colonne2
FROM table
ORDER BY colonne1

SELECT colonne1, colonne2, colonne3
FROM table
ORDER BY colonne1 DESC, colonne2 ASC

SELECT *
FROM utilisateur
ORDER BY nom
```

#### 6. AS (alias)

Dans le langage SQL il est possible d’utiliser des alias pour renommer temporairement une colonne ou une table dans une requête. Cette astuce est particulièrement utile pour faciliter la lecture des requêtes.

```sql
SELECT colonne1 AS c1, colonne2
FROM `table`

SELECT colonne1 c1, colonne2
FROM `table`
```

#### 7. LIMIT

La clause LIMIT est à utiliser dans une requête SQL pour spécifier le nombre maximum de résultats que l’ont souhaite obtenir. Cette clause est souvent associé à un OFFSET, c’est-à-dire effectuer un décalage sur le jeu de résultat.

```sql
SELECT *
FROM table
LIMIT 10
```

#### 8. Limit et Offset avec PostgreSQL

L’offset est une méthode simple de décaler les lignes à obtenir. La syntaxe pour utiliser une limite et un offset est la suivante

```sql
SELECT *
FROM table
LIMIT 10 OFFSET 5
```

#### 9. CASE

Dans le langage SQL, la commande “CASE … WHEN …” permet d’utiliser des conditions de type “si / sinon” (cf. if / else) similaire à un langage de programmation pour retourner un résultat disponible entre plusieurs possibilités. Le CASE peut être utilisé dans n’importe quelle instruction ou clause, telle que SELECT, UPDATE, DELETE, WHERE, ORDER BY ou HAVING.

```sql
CASE a 
       WHEN 1 THEN 'un'
       WHEN 2 THEN 'deux'
       WHEN 3 THEN 'trois'
       ELSE 'autre'
END

SELECT id, nom, marge_pourcentage, prix_unitaire, quantite, 
    CASE 
      WHEN marge_pourcentage=1 THEN 'Prix ordinaire'
      WHEN marge_pourcentage>1 THEN 'Prix supérieur à la normale'
      ELSE 'Prix inférieur à la normale'
    END
FROM `achat`
```

#### 10. UNION

La commande UNION de SQL permet de mettre bout-à-bout les résultats de plusieurs requêtes utilisant elles-même la commande SELECT. C’est donc une commande qui permet de concaténer les résultats de 2 requêtes ou plus. Pour l’utiliser il est nécessaire que chacune des requêtes à concaténer retournes le même nombre de colonnes, avec les mêmes types de données et dans le même ordre

```sql
SELECT * FROM table1
UNION
SELECT * FROM table2

```

#### 11. INSERT INTO

L’insertion de données dans une table s’effectue à l’aide de la commande INSERT INTO. Cette commande permet au choix d’inclure une seule ligne à la base existante ou plusieurs lignes d’un coup.

```sql
INSERT INTO table VALUES ('valeur 1', 'valeur 2', ...)
```

#### 12. ON DUPLICATE KEY UPDATE

L’instruction ON DUPLICATE KEY UPDATE est une fonctionnalité de MySQL qui permet de mettre à jour des données lorsqu’un enregistrement existe déjà dans une table. Cela permet d’avoir qu’une seule requête SQL pour effectuer selon la convenance un INSERT ou un UPDATE

```sql
INSERT INTO table (a, b, c)
VALUES (1, 20, 68)
ON DUPLICATE KEY UPDATE a=a+1

INSERT INTO table (a, b, c, date_insert)
VALUES (1, 20, 1, NOW())
ON DUPLICATE KEY UPDATE date_update=NOW
WHERE c=1
```

#### 13. UPDATE

La commande UPDATE permet d’effectuer des modifications sur des lignes existantes. Très souvent cette commande est utilisée avec WHERE pour spécifier sur quelles lignes doivent porter la ou les modifications.

```sql
UPDATE table
SET nom_colonne_1 = 'nouvelle valeur'
WHERE condition

UPDATE client
SET rue = '49 Rue Ameline',
  ville = 'Saint-Eustache-la-Forêt',
  code_postal = '76210'
WHERE id = 2
```

#### 14. DELETE

La commande DELETE en SQL permet de supprimer des lignes dans une table. En utilisant cette commande associé à WHERE il est possible de sélectionner les lignes concernées qui seront supprimées.

```sql
DELETE FROM `table`
WHERE condition

DELETE FROM `utilisateur`
WHERE `id` = 1

DELETE FROM `utilisateur`
WHERE `date_inscription` < '2012-04-10'

DELETE FROM `utilisateur`
```

#### 20. INNER JOIN

Dans le langage SQL la commande INNER JOIN, aussi appelée EQUIJOIN, est un type de jointures très communes pour lier plusieurs tables entre-elles. Cette commande retourne les enregistrements lorsqu’il y a au moins une ligne dans chaque colonne qui correspond à la condition.

```sql
SELECT *
FROM table1
INNER JOIN table2 ON table1.id = table2.fk_id

SELECT *
FROM table1
INNER JOIN table2
WHERE table1.id = table2.fk_id
```

#### 21. EXISTS

Dans le langage SQL, la commande EXISTS s’utilise dans une clause conditionnelle pour savoir s’il y a une présence ou non de lignes lors de l’utilisation d’une sous-requête.

```sql
SELECT nom_colonne1
FROM `table1`
WHERE EXISTS (
    SELECT nom_colonne2
    FROM `table2`
    WHERE nom_colonne3 = 10
    ```
  )

SELECT *
FROM commande
WHERE EXISTS (
    SELECT * 
    FROM produit 
    WHERE c_produit_id = p_id
)
```

#### 22. CREATE INDEX

En SQL, la commande CREATE INDEX permet de créer un index. L’index est utile pour accélérer l’exécution d’une requête SQL qui lit des données et ainsi améliorer les performances d’une application utilisant une base de données.

```sql
CREATE INDEX `index_nom` ON `table`;

CREATE INDEX `index_nom` ON `table` (`colonne1`);

CREATE INDEX `index_nom` ON `table` (`colonne1`, `colonne2`);

```

Un index unique permet de spécifier qu’une ou plusieurs colonnes doivent contenir des valeurs uniques à chaque enregistrement. Le système de base de données retournera une erreur si une requête tente d’insérer des données qui feront doublons sur la clé d’unicité. Pour insérer un tel index il suffit d’exécuter une requête SQL respectant la syntaxe suivante :

```sql
CREATE UNIQUE INDEX `index_nom` ON `table` (`colonne1`);

CREATE UNIQUE INDEX `index_nom` ON `table` (`colonne1`, `colonne2`);
```

#### 24. Create Constraints

Les contraintes peuvent être spécifiées lors de la création de la table avec l'instruction CREATE TABLE, ou après la création de la table avec l'instruction ALTER TABLE.

- NOT NULL - Ensures that a column cannot have a NULL value
- UNIQUE - Ensures that all values in a column are different
- PRIMARY KEY - A combination of a NOT NULL and UNIQUE. Uniquely identifies each row in a table
- FOREIGN KEY - Prevents actions that would destroy links between tables
- CHECK - Ensures that the values in a column satisfies a specific condition
- DEFAULT - Sets a default value for a column if no value is specified
- CREATE INDEX - Used to create and retrieve data from the database very quickly

```sql
CREATE TABLE table_name (
    column1 datatype constraint,
    column2 datatype constraint,
    column3 datatype constraint,
    ....
);

CREATE TABLE Orders (
    OrderID int NOT NULL,
    OrderNumber int NOT NULL,
    PersonID int,
    PRIMARY KEY (OrderID),
    FOREIGN KEY (PersonID) REFERENCES Persons(PersonID)
);

CREATE TABLE Persons (
    ID int NOT NULL,
    LastName varchar(255) NOT NULL,
    FirstName varchar(255),
    Age int,
    CHECK (Age>=18)
);

CREATE TABLE Persons (
    ID int NOT NULL,
    LastName varchar(255) NOT NULL,
    FirstName varchar(255),
    Age int,
    City varchar(255) DEFAULT 'Sandnes'
);

```

#### 25. VIEWS

En SQL, une vue est une table virtuelle basée sur l'ensemble des résultats d'une instruction SQL.

Une vue contient des lignes et des colonnes, tout comme une table réelle. Les champs d'une vue sont des champs d'une ou plusieurs tables réelles de la base de données.

Vous pouvez ajouter des instructions et des fonctions SQL à une vue et présenter les données comme si elles provenaient d'une seule table.

Une vue est créée à l'aide de l'instruction CREATE VIEW.

```sql
CREATE VIEW view_name AS
SELECT column1, column2, ...
FROM table_name
WHERE condition;

CREATE VIEW [Brazil Customers] AS
SELECT CustomerName, ContactName
FROM Customers
WHERE Country = 'Brazil';

CREATE VIEW [Products Above Average Price] AS
SELECT ProductName, Price
FROM Products
WHERE Price > (SELECT AVG(Price) FROM Products);
```
