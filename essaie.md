# ORM

1.Connexion à la Base de Données

a. Gestionnaire de Connexion

Fonctionnalité : Gérer les connexions à la base de données, gérer les transactions, et maintenir la pool de connexions.
Implémentation :

```python
import sqlite3

class DatabaseConnection:
    def __init__(self, db_url):
        self.db_url = db_url
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_url)

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def get_cursor(self):
        if not self.connection:
            self.connect()
        return self.connection.cursor()
    
    def commit(self):
        if self.connection:
            self.connection.commit()
    
    def rollback(self):
        if self.connection:
            self.connection.rollback()

```

2.Gestion des Modèles

a. Classe de Base des Modèles

Fonctionnalité : Fournir des méthodes CRUD de base, gestion des transactions, et liaison avec les champs.
Implémentation

```python
class BaseModel:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.save()
        return instance

    def save(self):
        if hasattr(self, 'id') and self.id:
            self.update()
        else:
            self.insert()

    def insert(self):
        fields = [f for f in self.__class__.__dict__.keys() if isinstance(getattr(self.__class__, f), Field)]
        values = [getattr(self, f) for f in fields]
        placeholders = ', '.join('?' * len(values))
        query = f"INSERT INTO {self.__class__.__name__.lower()} ({', '.join(fields)}) VALUES ({placeholders})"
        cursor = db.get_cursor()
        cursor.execute(query, values)
        db.commit()
        self.id = cursor.lastrowid

    def update(self):
        fields = [f for f in self.__class__.__dict__.keys() if isinstance(getattr(self.__class__, f), Field)]
        set_clause = ', '.join([f"{f}=?" for f in fields])
        values = [getattr(self, f) for f in fields] + [self.id]
        query = f"UPDATE {self.__class__.__name__.lower()} SET {set_clause} WHERE id=?"
        cursor = db.get_cursor()
        cursor.execute(query, values)
        db.commit()

    def delete(self):
        query = f"DELETE FROM {self.__class__.__name__.lower()} WHERE id=?"
        cursor = db.get_cursor()
        cursor.execute(query, (self.id,))
        db.commit()

    @classmethod
    def filter(cls, **kwargs):
        conditions = ' AND '.join([f"{k}=?" for k in kwargs.keys()])
        values = list(kwargs.values())
        query = f"SELECT * FROM {cls.__name__.lower()} WHERE {conditions}"
        cursor = db.get_cursor()
        cursor.execute(query, values)
        results = cursor.fetchall()
        return [cls(**dict(zip([column[0] for column in cursor.description], row))) for row in results]

    @classmethod
    def all(cls):
        query = f"SELECT * FROM {cls.__name__.lower()}"
        cursor = db.get_cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return [cls(**dict(zip([column[0] for column in cursor.description], row))) for row in results]

```

3.Mappage des Champs

a. Types de Champs

Fonctionnalité : Représenter les différents types de colonnes dans la base de données.
Implémentation :

```python
    class Field:
        def __init__(self, primary_key=False):
            self.primary_key = primary_key

    class IntegerField(Field):
        pass

    class CharField(Field):
        def __init__(self, max_length, primary_key=False):
            super().__init__(primary_key)
            self.max_length = max_length

```

3.Mappage des Champs

a. Types de Champs

Fonctionnalité : Représenter les différents types de colonnes dans la base de données.
Implémentation :

```python
class Field:
    def __init__(self, primary_key=False):
        self.primary_key = primary_key

class IntegerField(Field):
    pass

class CharField(Field):
    def __init__(self, max_length, primary_key=False):
        super().__init__(primary_key)
        self.max_length = max_length

```

6.Gestion des Relations

a. Relations One-to-One, One-to-Many, Many-to-Many

Fonctionnalité : Gérer les relations entre les modèles.
Implémentation

```python
class ForeignKey(Field):
    def __init__(self, to, primary_key=False):
        super().__init__(primary_key)
        self.to = to

class ManyToManyField(Field):
    def __init__(self, to):
        self.to = to

# Gestion des relations dans les modèles
class Post(BaseModel):
    id = IntegerField(primary_key=True)
    title = CharField(max_length=100)
    author = ForeignKey(User)

```

7.Validation et Sérialisation

a. Validation des Données

Fonctionnalité : Valider les données avant de les sauvegarder dans la base de données.
Implémentation : Ajouter des méthodes de validation dans BaseModel ou dans chaque modèle spécifique

```python
class BaseModel:
    def validate(self):
        pass  # Implémenter la logique de validation ici

    def save(self):
        self.validate()
        super().save()

```

b. Sérialisation des Modèles

Fonctionnalité : Convertir les objets en formats compatibles (JSON, XML).
Implémentation

```python
import json

class BaseModel:
    def to_dict(self):
        return {key: getattr(self, key) for key in self.__class__.__dict__.keys() if isinstance(getattr(self.__class__, key), Field)}

    def to_json(self):
        return json.dumps(self.to_dict())

```

8.Gestion des Migrations

a. Génération et Application des Migrations

Fonctionnalité : Gérer les modifications de la structure de la base de données.
Implémentation : Créer un outil de migration pour gérer les changements de schéma

```python
class Migration:
    def __init__(self, db):
        self.db = db

    def create_table(self, model):
        fields = [f"{name} {self.get_sql_type(field)}" for name, field in model.__dict__.items() if isinstance(field, Field)]
        query = f"CREATE TABLE {model.__name__.lower()} ({', '.join(fields)})"
        cursor = self.db.get_cursor()
        cursor.execute(query)
        self.db.commit()

    def get_sql_type(self, field):
        if isinstance(field, IntegerField):
            return "INTEGER"
        elif isinstance(field, CharField):
            return f"VARCHAR({field.max_length})"
        elif isinstance(field, ForeignKey):
            return "INTEGER"
        return "TEXT"

# Usage
migration = Migration(db)
migration.create_table(User)

```

9.Interface de Requêtes de Haut Niveau

a. API de Requêtes

Fonctionnalité : Fournir une API intuitive pour interagir avec la base de données.
Implémentation : Méthodes de requêtes dans BaseModel

```python
class BaseModel:
    @classmethod
    def get(cls, **kwargs):
        results = cls.filter(**kwargs)
        if results:
            return results[0]
        return None

    @classmethod
    def filter(cls, **kwargs):
        conditions = ' AND '.join([f"{k}=?" for k in kwargs.keys()])
        values = list(kwargs.values())
        query = f"SELECT * FROM {cls.__name__.lower()} WHERE {conditions}"
        cursor = db.get_cursor()
        cursor.execute(query, values)
        results = cursor.fetchall()
        return [cls(**dict(zip([column[0] for column in cursor.description], row))) for row in results]

    @classmethod
    def all(cls):
        query = f"SELECT * FROM {cls.__name__.lower()}"
        cursor = db.get_cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return [cls(**dict(zip([column[0] for column in cursor.description], row))) for row in results]

```

10.Transactions

a. Gestion des Transactions

Fonctionnalité : Gérer les transactions pour assurer l'intégrité des données.
Implémentation :

```python
class DatabaseConnection:
    def __init__(self, db_url):
        self.db_url = db_url
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_url)

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def get_cursor(self):
        if not self.connection:
            self.connect()
        return self.connection.cursor()

    def commit(self):
        if self.connection:
            self.connection.commit()

    def rollback(self):
        if self.connection:
            self.connection.rollback()

# Usage
db = DatabaseConnection('sqlite:///mydatabase.db')
try:
    db.connect()
    user = User.create(name='Alice')
    db.commit()
except Exception as e:
    db.rollback()
    print("Transaction failed:", e)
finally:
    db.disconnect()

```

b. Contexte de Transaction

Fonctionnalité : Gérer l'ouverture, la validation et l'annulation des transactions dans un contexte géré.
Implémentation

```python
from contextlib import contextmanager
import sqlite3

class DatabaseConnection:
    def __init__(self, db_url):
        self.db_url = db_url
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_url)

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def get_cursor(self):
        if not self.connection:
            self.connect()
        return self.connection.cursor()

    def commit(self):
        if self.connection:
            self.connection.commit()

    def rollback(self):
        if self.connection:
            self.connection.rollback()

    @contextmanager
    def transaction(self):
        cursor = self.get_cursor()
        try:
            yield cursor
            self.commit()
        except Exception as e:
            self.rollback()
            raise e
        finally:
            cursor.close()

```

c. Utilisation du Contexte de Transaction

Fonctionnalité : Utiliser le gestionnaire de transactions pour garantir des opérations atomiques.
Implémentation :

```python
class BaseModel:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.save()
        return instance

    def save(self):
        if hasattr(self, 'id') and self.id:
            self.update()
        else:
            self.insert()

    def insert(self):
        fields = [f for f in self.__class__.__dict__.keys() if isinstance(getattr(self.__class__, f), Field)]
        values = [getattr(self, f) for f in fields]
        placeholders = ', '.join('?' * len(values))
        query = f"INSERT INTO {self.__class__.__name__.lower()} ({', '.join(fields)}) VALUES ({placeholders})"
        with db.transaction() as cursor:
            cursor.execute(query, values)
            self.id = cursor.lastrowid

    def update(self):
        fields = [f for f in self.__class__.__dict__.keys() if isinstance(getattr(self.__class__, f), Field)]
        set_clause = ', '.join([f"{f}=?" for f in fields])
        values = [getattr(self, f) for f in fields] + [self.id]
        query = f"UPDATE {self.__class__.__name__.lower()} SET {set_clause} WHERE id=?"
        with db.transaction() as cursor:
            cursor.execute(query, values)

    def delete(self):
        query = f"DELETE FROM {self.__class__.__name__.lower()} WHERE id=?"
        with db.transaction() as cursor:
            cursor.execute(query, (self.id,))

    @classmethod
    def filter(cls, **kwargs):
        conditions = ' AND '.join([f"{k}=?" for k in kwargs.keys()])
        values = list(kwargs.values())
        query = f"SELECT * FROM {cls.__name__.lower()} WHERE {conditions}"
        with db.transaction() as cursor:
            cursor.execute(query, values)
            results = cursor.fetchall()
            return [cls(**dict(zip([column[0] for column in cursor.description], row))) for row in results]

    @classmethod
    def all(cls):
        query = f"SELECT * FROM {cls.__name__.lower()}"
        with db.transaction() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            return [cls(**dict(zip([column[0] for column in cursor.description], row))) for row in results]

```

d. Exemple d'Utilisation

Fonctionnalité : Exécuter des opérations en utilisant des transactions atomiques.
Implémentation :

```python
# Connexion à la base de données
db = DatabaseConnection('sqlite:///mydatabase.db')
db.connect()

try:
    with db.transaction() as cursor:
        user = User.create(name='Alice')
        post = Post.create(title='First Post', author=user)
        # D'autres opérations...

except Exception as e:
    print("Transaction échouée:", e)

finally:
    db.disconnect()

```

```python
class IntegerField(Field):
    def __init__(self, min_value=None, max_value=None):
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value):
        if not isinstance(value, int):
            raise ValueError(f"Expected an integer for field {self.__class__.__name__}, got {type(value).__name__}")
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"Value for field {self.__class__.__name__} must be at least {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"Value for field {self.__class__.__name__} must be at most {self.max_value}")

# Exemple d'utilisation
class User(Model):
    age = IntegerField(min_value=0)

# Utilisation
user = User(age=30)

```

```python
import sqlite3

class Model:
    pass  # Votre implémentation de Model

class CharField:
    pass  # Votre implémentation de CharField

class IntegerField:
    pass  # Votre implémentation de IntegerField

class ListField:
    pass  # Votre implémentation de ListField

class User(Model):
    name = CharField()
    age = IntegerField()
    interests = ListField()

# Fonction pour créer la table dans SQLite en utilisant les types de données appropriés
def create_table(model_class):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    columns = []
    for field_name, field_type in model_class.__dict__.items():
        if isinstance(field_type, CharField):
            columns.append(f"{field_name} TEXT")
        elif isinstance(field_type, IntegerField):
            columns.append(f"{field_name} INTEGER")
        elif isinstance(field_type, ListField):
            columns.append(f"{field_name} TEXT")  # Vous pouvez ajuster le type de données selon vos besoins
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {model_class.__name__.lower()} ({', '.join(columns)})")
    conn.commit()
    conn.close()

# Création de la table pour chaque modèle
create_table(User)

```

```python
import sqlite3

class Field:
    def validate(self, value):
        """Méthode de validation des champs."""
        raise NotImplementedError("validate method must be implemented in subclass.")

class IntegerField(Field):
    def validate(self, value):
        if not isinstance(value, int):
            raise ValueError(f"Expected an integer for field {self.__class__.__name__}, got {type(value).__name__}")
        if value < 0:
            raise ValueError(f"Value for field {self.__class__.__name__} must be at least 0")

# Fonction pour créer la table dans SQLite en utilisant les types de données appropriés et les contraintes de vérification
def create_table(model_class):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    columns = []
    for field_name, field_type in model_class.__dict__.items():
        if isinstance(field_type, IntegerField):
            columns.append(f"{field_name} INTEGER CHECK ({field_name} >= 0)")
        # Ajoutez d'autres types de champs ici avec leurs contraintes si nécessaire
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {model_class.__name__.lower()} ({', '.join(columns)})")
    conn.commit()
    conn.close()

# Création de la table pour chaque modèle
create_table(User)

```

```python
import sqlite3

class Field:
    def __init__(self, nullable=True, default=None, primary_key=False, unique=False, editable=True, check=None):
        self.nullable = nullable
        self.default = default
        self.primary_key = primary_key
        self.unique = unique
        self.editable = editable
        self.check = check

    def validate(self, value):
        """Méthode de validation des champs."""
        raise NotImplementedError("validate method must be implemented in subclass.")

class IntegerField(Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, value):
        if not isinstance(value, int):
            raise ValueError(f"Expected an integer for field {self.__class__.__name__}, got {type(value).__name__}")
        if self.check is not None and not self.check(value):
            raise ValueError(f"Value for field {self.__class__.__name__} failed custom validation")

# Fonction pour créer la table dans SQLite en utilisant les types de données appropriés et les contraintes de vérification
def create_table(model_class):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    columns = []
    for field_name, field_type in model_class.__dict__.items():
        if isinstance(field_type, IntegerField):
            column_definition = f"{field_name} INTEGER"
            if not field_type.nullable:
                column_definition += " NOT NULL"
            if field_type.default is not None:
                column_definition += f" DEFAULT {field_type.default}"
            if field_type.primary_key:
                column_definition += " PRIMARY KEY"
            if field_type.unique:
                column_definition += " UNIQUE"
            columns.append(column_definition)
            if field_type.check is not None:
                cursor.execute(f"ALTER TABLE {model_class.__name__.lower()} ADD CONSTRAINT check_{field_name} CHECK ({field_type.check.__name__}({field_name}))")
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {model_class.__name__.lower()} ({', '.join(columns)})")
    conn.commit()
    conn.close()

# Création de la table pour chaque modèle
create_table(User)

```
