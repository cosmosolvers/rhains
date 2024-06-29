# RHAINS ARCHITECTURE

rhains/
├── core/
|   ├── root/
|   ├── config/
|   ├── models/
|   |   ├── field/
|   |   |   ├── date/
|   |   |   |   ├── datefield.py
|   |   |   |   ├── datetimefield.py
|   |   |   |   ├── timefield.py
|   |   |   ├── file/
|   |   |   |   ├── audiofield.py
|   |   |   |   ├── filefield.py
|   |   |   |   ├── imagefield.py
|   |   |   |   ├── mediafield.py
|   |   |   ├── mapping/
|   |   |   |   ├── aggregationfield.py
|   |   |   |   ├── arrayfield.py
|   |   |   |   ├── geographicalfield.py
|   |   |   |   ├── matrixfield.py
|   |   |   ├── nbase/
|   |   |   |   ├── base32field.py
|   |   |   |   ├── base64field.py
|   |   |   |   ├── basenfield.py
|   |   |   |   ├── baseurlfield.py
|   |   |   |   ├── binaryfield.py
|   |   |   |   ├── hexadecimalfield.py
|   |   |   ├── numeric/
|   |   |   |   ├── booleanfield.py
|   |   |   |   ├── counterfield.py
|   |   |   |   ├── decimalfield.py
|   |   |   |   ├── integerfield.py
|   |   |   |   ├── percentfield.py
|   |   |   ├── object/
|   |   |   |   ├── callablefield.py
|   |   |   |   ├── geometryfield.py
|   |   |   |   ├── graphfield.py
|   |   |   |   ├── objectfield.py
|   |   |   |   ├── uuidfield.py
|   |   |   ├── ship/
|   |   |   |   ├── foreignkeyfield.py
|   |   |   |   ├── foreignship.py
|   |   |   |   ├── manytomanyfield.py
|   |   |   |   ├── manytomanyship.py
|   |   |   |   ├── onetoonefield.py
|   |   |   |   ├── onetooneship.py
|   |   |   |   ├── reference.py
|   |   |   |   ├── relationship.py
|   |   |   ├── string/
|   |   |   |   ├── bytefield.py
|   |   |   |   ├── charfield.py
|   |   |   |   ├── colorfield.py
|   |   |   |   ├── emailfield.py
|   |   |   |   ├── filepathfield.py
|   |   |   |   ├── genomicfield.py
|   |   |   |   ├── ipaddressfield.py
|   |   |   |   ├── passwordfield.py
|   |   |   |   ├── phonefield.py
|   |   |   |   ├── textfield.py
|   |   |   |   ├── unityfield.py
|   |   |   |   ├── urlfield.py
|   |   |   ├── field.py
|   |   ├── model.py
|   ├── router/
|   ├── viewer/
|   |   ├── view/
|   |   ├── viewmodel/
|   ├── middleware/
|   ├── rh/
├── httpserver/
|   ├── request/
|   ├── response/
├── utils/
|   ├── bin.py
|   ├── color.py
|   ├── condition.py
|   ├── const.py
|   ├── context.py
|   ├── validefunc.py
├── exceptions/
|   ├── core/
|   |   ├── models/
|   |   ├── rh
|   ├── httpserver/
|   ├── utils/
|   ├── security/
|   ├── services/
|   ├── rhains.py
├── security/
|   ├── encrypter/
|   ├── validator/
|   ├── auth/
|   |   ├── authentication.py
|   |   ├── authorization.py
├── services/
|   ├── logger.py
├── public/
├── tests/
|   ├── unittest
|   ├── integration
├── docs/

## core

c'est le composant moteur de tous

### root

initilise le framework, configure les services et demare le server

### config

gere les configurations du framework

### models

gere les models

### router

gere les routes

### viewer

gere les vue

#### view

class de base pour les vue

#### viewmodel

class de base pour les viewmodel

### middleware

gere les middelwares

### rh

## httpserver

gere les rquetes http

### request

gestion des requests entrantes

### response

gestion des requests sortantes

## utils

gere les codes intermediaire utiles

## exceptions

gere les exceptions

## security

gere la securite

### encrypter

Fournit des fonctionnalités de chiffrement et de déchiffrement

### validator

 Fournit des fonctionnalités de validation des données

### auth

gere l'authentification et les authorization des utilisateurs

## services

fournir les services tierces

### logger

Fournit des fonctionnalités de journalisation

## public

## tests

gere les tests

## docs

gere la documentation
