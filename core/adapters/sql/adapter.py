""""""

from typing import List
from adapters import interface






class Rows:
    
    def __init__(self, adapter: interface.SQLAdapterInterface, tablename: str) -> None:
        self.adapter = adapter
        self.tablename: str = tablename
    
    ## create
    def insert(self, values: List[str]):
        query = f"""INSERT INTO {self.tablename} VALUES ({', '.join(["?"] * len(values))})"""
        self.adapter.execute(query, values, fetch=True, commit=True)

    ## read
    def select(self, limit: int=-1, where: str=None, sort: str=None, join: str=None):
        """
        """
        query = f"""
            SELECT * FROM {self.tablename}
            {f"JOIN {join.split('::')[0]} ON {join.split('::')[1]}" if join else ""}
            {f"LIMIT {limit}" if limit > 0 else ""}
            {f"WHERE {where}" if where else ""}
            {f"ORDER BY {sort[1:] if sort[0] == '-' else {sort}} {'ASC' if sort[0] != '-' else 'DES'} " if sort else ""}
        """
        results = self.adapter.execute(query, fetch=True)
        return results
    
    def update(self, values: List, where=None):
        query = f"""
            UPDATE {self.tablename}
            SET {', '.join([f"{column} = ?" for column in values])}
            {f"WHERE {where}" if where else ""}
        """
        self.adapter.execute(query, values, commit=True)
    
    ## delete
    def delete(self, where=None):
        query = f"""
            DELETE FROM {self.tablename}
            {f"WHERE {where}" if where else ""}
        """
        self.adapter.execute(query, commit=True)
        
    ## count
    def count(self):
        query = f"SELECT COUNT(*) FROM {self.tablename}"
        result = self.adapter.execute(query, fetch=True)
        return result[0][0]




class DataTable:
    """"""
    
    def __init__(self, adapter: interface.SQLAdapterInterface, tablename: str) -> None:
        self.adapter = adapter
        self.tablename: str = tablename
        self.rows = Rows(adapter, tablename)
    
    # add : drop : rename column
    def column(self, column: str, new: str, migrate: str):
        """
        migrate: add drop rename
        """
        action = {
            'add': 'ADD COLUMN',
            'drop': 'DROP COLUMN',
            'rename': 'RENAME COLUMN' 
        }
        query = f"""
            ALTER TABLE {self.tablename}
            {action[migrate]} {column} {f'TO {new}' if migrate == 'rename' and new else ''}
        """
        self.adapter.execute(query, commit=True)
    
    ## drop table
    def drop(self):
        query = f"DROP TABLE IF EXISTS {self.tablename}"
        self.adapter.execute(query, commit=True)
    
    ## truncate table
    def truncate(self):
        query = f"TRUNCATE TABLE {self.tablename}"
        self.adapter.execute(query, commit=True)
    
    ## exists
    def exists(self):
        query = f"""SELECT name FROM sqlite_master WHERE type='table' AND name='{self.tablename}'"""
        result = self.adapter.execute(query, fetch=True)
        return True if result else False
    
    ## create table
    def create(self, columns: List[str]):
        query = f"""
            CREATE TABLE IF NOT EXISTS {self.tablename} (
            {', '.join(columns)}
        )
        """
        self.adapter.execute(query, commit=True)
    
    def __repr__(self) -> str:
        return f"<DataTable {self.tablename}>"




# SELECT {attribute}+
#   FROM {table}+
#   [ WHERE {boolean predicate to pick rows} ]
#   [ ORDER BY {attribute}+ ];



# CREATE TABLE orders (
#    first_name VARCHAR(20),
#    last_name  VARCHAR(20),
#    phone      VARCHAR(20),
#    order_date  TIMESTAMP, -- stores both date and time
#    sold_by     VARCHAR(20),
#    CONSTRAINT orders_pk PRIMARY KEY (first_name, last_name, phone, order_date),
#    CONSTRAINT orders_customers_fk FOREIGN KEY (first_name, last_name, phone)
#       REFERENCES customers (first_name, last_name, phone)
# );

# (SELECT f.species_name,
#         AVG(f.height) AS average_height, AVG(f.diameter) AS average_diameter
#    FROM flora AS f
#   WHERE f.species_name = 'Banksia'
#      OR f.species_name = 'Sheoak'
#      OR f.species_name = 'Wattle'
#   GROUP BY f.species_name, f.observation_date)

#   UNION ALL

# (SELECT b.species_name,
#         AVG(b.height) AS average_height, AVG(b.diameter) AS average_diameter
#    FROM botanic_garden_flora AS b
#   WHERE b.species_name = 'Banksia'
#      OR b.species_name = 'Sheoak'
#      OR b.species_name = 'Wattle'
#   GROUP BY b.species_name, b.observation_date);


# SELECT r.last_name
#   FROM riders AS r
#        INNER JOIN bikes AS b
#        ON r.bike_vin_num = b.vin_num
#           AND b.engine_tally > 2

#        INNER JOIN crew AS c
#        ON r.crew_chief_last_name = c.last_name
#           AND c.chief = 'Y';


# SELECT r.last_name,
#        (SELECT MAX(YEAR(championship_date))
#           FROM champions AS c
#          WHERE c.last_name = r.last_name
#            AND c.confirmed = 'Y') AS last_championship_year
#   FROM riders AS r
#  WHERE r.last_name IN
#        (SELECT c.last_name
#           FROM champions AS c
#          WHERE YEAR(championship_date) > '2008'
#            AND c.confirmed = 'Y');


# SELECT CASE postcode
#        WHEN 'BN1' THEN 'Brighton'
#        WHEN 'EH1' THEN 'Edinburgh'
#        END AS city
#   FROM office_locations
#  WHERE country = 'United Kingdom'
#    AND opening_time BETWEEN 8 AND 9
#    AND postcode IN ('EH1', 'BN1', 'NN1', 'KW1');


# CREATE TABLE staff (
#     PRIMARY KEY (staff_num),
#     staff_num      INT(5)       NOT NULL,
#     first_name     VARCHAR(100) NOT NULL,
#     pens_in_drawer INT(2)       NOT NULL,
#                    CONSTRAINT pens_in_drawer_range
#                    CHECK(pens_in_drawer BETWEEN 1 AND 99)
# );


