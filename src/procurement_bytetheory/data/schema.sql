drop table Business;
drop table Temp_Business;
drop table Market;
drop table Temp_Market;
drop table Item;
drop table Temp_Item;
drop table Inventory;
drop table Temp_Inventory;

create table Business(
	id INT PRIMARY KEY NOT NULL,
	name TEXT NOT NULL,
	money_amount REAL NOT NULL,
	market_id INT,
	inventory_id INT
);

create table Temp_Business(
	id INT PRIMARY KEY NOT NULL,
	name TEXT NOT NULL,
	money_amount REAL NOT NULL,
	market_id INT,
	inventory_id INT
);

create table Market(
	id INT PRIMARY KEY NOT NULL,
	name TEXT NOT NULL
);

create table Temp_Market(
	id INT PRIMARY KEY NOT NULL,
	name TEXT NOT NULL
);

create table Item(
	id INT PRIMARY KEY NOT NULL,
	name TEXT NOT NULL,
	value REAL NOT NULL,
	market_id INT,
	inventory_id INT
);

create table Temp_Item(
	id INT PRIMARY KEY NOT NULL,
	name TEXT NOT NULL,
	value REAL NOT NULL,
	market_id INT,
	inventory_id INT
);

create table Inventory(
	id INT PRIMARY KEY NOT NULL,
	name TEXT NOT NULL
);

create table Temp_Inventory(
	id INT PRIMARY KEY NOT NULL,
	name TEXT NOT NULL
);

