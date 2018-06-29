-- CREATE DATABASE "aquila";
-- CREATE USER "aquila" WITH PASSWORD 'aquila2018';
-- GRANT ALL PRIVILEGES ON DATABASE aquila TO aquila;


CREATE TABLE levels (
	level SMALLINT PRIMARY KEY,
	exp_thru INT
);

CREATE TABLE countries (
	id SMALLINT PRIMARY KEY,
	name VARCHAR
);

CREATE TYPE PLAYER_STATUS AS ENUM ('alive', 'suspended');

CREATE TABLE players (
	id SERIAL PRIMARY KEY,
	username VARCHAR,
	password VARCHAR,
	balance BIGINT,
	demo_balance INT,
	level SMALLINT REFERENCES levels,
	exp INT,
	wagered BIGINT,
	won BIGINT,
	lost BIGINT,
	status PLAYER_STATUS,
	chat_messages_count INT,
	bets_count INT,
	bets_won_count INT,
	country_id SMALLINT REFERENCES countries,
	registered_date TIMESTAMP,
	settings JSON,
	is_online BOOLEAN
);

CREATE TABLE player_blocks (
	id SERIAL PRIMARY KEY,
	player_id INT REFERENCES players,
	block_date TIMESTAMP,
	unblock_date TIMESTAMP,
	reason SMALLINT
);

CREATE TYPE RELATION AS ENUM ('muted', 'voice_muted');

CREATE TABLE player_relations (
	player_id INT REFERENCES players,
	ref_player_id INT REFERENCES players,
	relation RELATION
);

CREATE TABLE feedbacks (
	id SERIAL PRIMARY KEY,
	player_id INT REFERENCES players,
	content VARCHAR,
	date TIMESTAMP,
	answered TIMESTAMP
);

CREATE TYPE ACTION AS ENUM ('login', 'logout');

CREATE TABLE action_log (
	id SERIAL PRIMARY KEY,
	player_id INT REFERENCES players,
	action ACTION,
	ip CIDR,
	date TIMESTAMP
);

CREATE TABLE rooms (
	id SERIAL PRIMARY KEY,
	player_id_list INTEGER ARRAY,
	is_running BOOLEAN
);

CREATE TABLE rounds (
	id SERIAL PRIMARY KEY,
	room_id INT REFERENCES rooms,
	player_id_list INTEGER ARRAY,
	start_date TIMESTAMP,
	end_date TIMESTAMP
);

CREATE TABLE chat_messages (
	id BIGSERIAL PRIMARY KEY,
	sender_id INT REFERENCES players,
	room_id INT REFERENCES rooms,
	content VARCHAR,
	date TIMESTAMP
);

CREATE TABLE room_log (
	room_id INT REFERENCES rooms, 
	player_id INT REFERENCES players,
	joined_date TIMESTAMP,
	left_date TIMESTAMP
);

CREATE TABLE bet_types (
	id SMALLINT PRIMARY KEY,
	payout SMALLINT,
	exp_gain SMALLINT,
	exp_gain_on_win SMALLINT
);

CREATE TYPE OUTCOME AS ENUM ('won', 'lost');

CREATE TABLE bets (
	id BIGSERIAL PRIMARY KEY,
	player_id INT REFERENCES players,
	round_id INT REFERENCES rounds,
	bet_type_id SMALLINT REFERENCES bet_types,
	bet_on INTEGER ARRAY,
	amount BIGINT,
	outcome OUTCOME,
	is_real BOOLEAN
);

CREATE TABLE ip_blocks (
	id SERIAL PRIMARY KEY,
	ip CIDR,
	block_date TIMESTAMP,
	unblock_date TIMESTAMP,
	reason SMALLINT
);
