-- CREATE DATABASE "aquila";
-- CREATE USER "aquila" WITH PASSWORD 'aquila2018';
-- GRANT ALL PRIVILEGES ON DATABASE aquila TO aquila;

/*
Index candidates:
rooms.joined_date
*/

CREATE TABLE levels (
	id SMALLINT PRIMARY KEY,
	exp_thru INT
);

CREATE TABLE countries (
	name TEXT,
	iso_2 CHAR(2) PRIMARY KEY,
	iso_3 CHAR(3),
	iso_num CHAR(3)
);

CREATE TABLE rooms (
	id SERIAL PRIMARY KEY,
	player_id_list INTEGER ARRAY,
	is_running BOOLEAN
);

CREATE TYPE PLAYER_STATUS AS ENUM ('alive', 'suspended');

CREATE TABLE players (
	id SERIAL PRIMARY KEY,
	username TEXT,
	password TEXT,
	token TEXT,
	balance BIGINT,
	demo_balance INT,
	level_id SMALLINT REFERENCES levels,
	exp INT,
	wagered BIGINT,
	won BIGINT,
	lost BIGINT,
	status PLAYER_STATUS,
	chat_messages_count INT,
	bets_count INT,
	bets_won_count INT,
	country_id CHAR(2) REFERENCES countries,
	registered_date TIMESTAMP,
	settings JSON,
	room_id SMALLINT REFERENCES rooms,
	last_checkup TIMESTAMP,
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
	content TEXT,
	date TIMESTAMP,
	answered TIMESTAMP
);

CREATE TYPE ACTION AS ENUM ('login', 'logout');

CREATE TABLE login_log (
	id SERIAL PRIMARY KEY,
	player_id INT REFERENCES players,
	action ACTION,
	ip CIDR,
	date TIMESTAMP
);

CREATE TABLE rounds (
	id SERIAL PRIMARY KEY,
	room_id INT REFERENCES rooms,
	player_id_list INTEGER ARRAY,
	outcome SMALLINT,
	start_date TIMESTAMP,
	end_date TIMESTAMP
);

CREATE TABLE chat_messages (
	id BIGSERIAL PRIMARY KEY,
	sender_id INT REFERENCES players,
	room_id INT REFERENCES rooms,
	content TEXT,
	date TIMESTAMP
);

CREATE TABLE room_log (
	id SERIAL PRIMARY KEY,
	room_id INT REFERENCES rooms, 
	player_id INT REFERENCES players,
	entry_date TIMESTAMP,
	leave_date TIMESTAMP
);

CREATE TABLE bets (
	id BIGSERIAL PRIMARY KEY,
	player_id INT REFERENCES players,
	round_id INT REFERENCES rounds,
	bet_on TEXT,
	amount BIGINT,
	is_real BOOLEAN
);

CREATE TABLE ip_blocks (
	id SERIAL PRIMARY KEY,
	ip CIDR,
	block_date TIMESTAMP,
	unblock_date TIMESTAMP,
	reason SMALLINT
);

-- Indices
CREATE INDEX rooms_is_running
ON rooms (is_running);


-- Static content

-- Insert 1000 rooms
INSERT INTO rooms (player_id_list, is_running) VALUES ('{}', FALSE);
INSERT INTO rooms (player_id_list, is_running)
SELECT tmp.player_id_list, tmp.is_running FROM
(SELECT player_id_list, is_running, generate_series(1, 999) FROM rooms) tmp;

INSERT INTO countries VALUES
('Afghanistan', 'AF', 'AFG', 004),
('Aland Islands', 'AX', 'ALA', 248),
('Albania', 'AL', 'ALB', 008),
('Algeria', 'DZ', 'DZA', 012),
('American Samo', 'AS', 'ASM', 016),
('Andorra', 'AD', 'AND', 020),
('Angol', 'AO', 'AGO', 024),
('Anguill', 'AI', 'AIA', 660),
('Antarctic', 'AQ', 'ATA', 010),
('Antigua and Barbuda', 'AG', 'ATG', 028),
('Argentin', 'AR', 'ARG', 032),
('Armenia', 'AM', 'ARM', 051),
('Arub', 'AW', 'ABW', 533),
('Australi', 'AU', 'AUS', 036),
('Austria', 'AT', 'AUT', 040),
('Azerbaija', 'AZ', 'AZE', 031),
('Bahamas', 'BS', 'BHS', 044),
('Bahrain', 'BH', 'BHR', 048),
('Banglades', 'BD', 'BGD', 050),
('Barbado', 'BB', 'BRB', 052),
('Belarus', 'BY', 'BLR', 112),
('Belgium', 'BE', 'BEL', 056),
('Beliz', 'BZ', 'BLZ', 084),
('Beni', 'BJ', 'BEN', 204),
('Bermuda', 'BM', 'BMU', 060),
('Bhuta', 'BT', 'BTN', 064),
('Bolivia', 'BO', 'BOL', 068),
('Bosnia and Herzegovin', 'BA', 'BIH', 070),
('Botswan', 'BW', 'BWA', 072),
('Bouvet Islan', 'BV', 'BVT', 074),
('Brazi', 'BR', 'BRA', 076),
('British Virgin Island', 'VG', 'VGB', 092),
('British Indian Ocean Territor', 'IO', 'IOT', 086),
('Brunei Darussala', 'BN', 'BRN', 096),
('Bulgari', 'BG', 'BGR', 100),
('Burkina Fas', 'BF', 'BFA', 854),
('Burundi', 'BI', 'BDI', 108),
('Cambodi', 'KH', 'KHM', 116),
('Cameroo', 'CM', 'CMR', 120),
('Canad', 'CA', 'CAN', 124),
('Cape Verd', 'CV', 'CPV', 132),
('Cayman Island', 'KY', 'CYM', 136),
('Central African Republi', 'CF', 'CAF', 140),
('Cha', 'TD', 'TCD', 148),
('Chil', 'CL', 'CHL', 152),
('Chin', 'CN', 'CHN', 156),
('Hong Kong, SAR Chin', 'HK', 'HKG', 344),
('Macao, SAR Chin', 'MO', 'MAC', 446),
('Christmas Islan', 'CX', 'CXR', 162),
('Cocos (Keeling) Islands', 'CC', 'CCK', 166),
('Colombi', 'CO', 'COL', 170),
('Comoros', 'KM', 'COM', 174),
('Congo (Brazzaville)', 'CG', 'COG', 178),
('Congo, (Kinshasa', 'CD', 'COD', 180),
('Cook Island', 'CK', 'COK', 184),
('Costa Ric', 'CR', 'CRI', 188),
('Côte d"Ivoir', 'CI', 'CIV', 384),
('Croatia', 'HR', 'HRV', 191),
('Cub', 'CU', 'CUB', 192),
('Cypru', 'CY', 'CYP', 196),
('Czech Republi', 'CZ', 'CZE', 203),
('Denmark', 'DK', 'DNK', 208),
('Djibout', 'DJ', 'DJI', 262),
('Dominic', 'DM', 'DMA', 212),
('Dominican Republi', 'DO', 'DOM', 214),
('Ecuador', 'EC', 'ECU', 218),
('Egyp', 'EG', 'EGY', 818),
('El Salvador', 'SV', 'SLV', 222),
('Equatorial Guine', 'GQ', 'GNQ', 226),
('Eritrea', 'ER', 'ERI', 232),
('Estonia', 'EE', 'EST', 233),
('Ethiopi', 'ET', 'ETH', 231),
('Falkland Islands (Malvinas)', 'FK', 'FLK', 238),
('Faroe Island', 'FO', 'FRO', 234),
('Fij', 'FJ', 'FJI', 242),
('Finland', 'FI', 'FIN', 246),
('Franc', 'FR', 'FRA', 250),
('French Guian', 'GF', 'GUF', 254),
('French Polynesi', 'PF', 'PYF', 258),
('French Southern Territories', 'TF', 'ATF', 260),
('Gabo', 'GA', 'GAB', 266),
('Gambi', 'GM', 'GMB', 270),
('Georgia', 'GE', 'GEO', 268),
('Germany', 'DE', 'DEU', 276),
('Ghan', 'GH', 'GHA', 288),
('Gibralta', 'GI', 'GIB', 292),
('Greec', 'GR', 'GRC', 300),
('Greenlan', 'GL', 'GRL', 304),
('Grenada', 'GD', 'GRD', 308),
('Guadeloup', 'GP', 'GLP', 312),
('Gua', 'GU', 'GUM', 316),
('Guatemal', 'GT', 'GTM', 320),
('Guernse', 'GG', 'GGY', 831),
('Guine', 'GN', 'GIN', 324),
('Guinea-Bissa', 'GW', 'GNB', 624),
('Guyan', 'GY', 'GUY', 328),
('Hait', 'HT', 'HTI', 332),
('Heard and Mcdonald Island', 'HM', 'HMD', 334),
('Holy See (Vatican City State', 'VA', 'VAT', 336),
('Hondura', 'HN', 'HND', 340),
('Hungary', 'HU', 'HUN', 348),
('Iceland', 'IS', 'ISL', 352),
('Indi', 'IN', 'IND', 356),
('Indonesi', 'ID', 'IDN', 360),
('Iran, Islamic Republic o', 'IR', 'IRN', 364),
('Ira', 'IQ', 'IRQ', 368),
('Ireland', 'IE', 'IRL', 372),
('Isle of Man', 'IM', 'IMN', 833),
('Israe', 'IL', 'ISR', 376),
('Ital', 'IT', 'ITA', 380),
('Jamaica', 'JM', 'JAM', 388),
('Japa', 'JP', 'JPN', 392),
('Jerse', 'JE', 'JEY', 832),
('Jorda', 'JO', 'JOR', 400),
('Kazakhsta', 'KZ', 'KAZ', 398),
('Keny', 'KE', 'KEN', 404),
('Kiribat', 'KI', 'KIR', 296),
('Korea (North', 'KP', 'PRK', 408),
('Korea (South', 'KR', 'KOR', 410),
('Kuwai', 'KW', 'KWT', 414),
('Kyrgyzsta', 'KG', 'KGZ', 417),
('Lao PDR', 'LA', 'LAO', 418),
('Latvi', 'LV', 'LVA', 428),
('Lebanon', 'LB', 'LBN', 422),
('Lesotho', 'LS', 'LSO', 426),
('Liberia', 'LR', 'LBR', 430),
('Liby', 'LY', 'LBY', 434),
('Liechtenstei', 'LI', 'LIE', 438),
('Lithuani', 'LT', 'LTU', 440),
('Luxembour', 'LU', 'LUX', 442),
('Macedonia, Republic o', 'MK', 'MKD', 807),
('Madagasca', 'MG', 'MDG', 450),
('Malaw', 'MW', 'MWI', 454),
('Malaysi', 'MY', 'MYS', 458),
('Maldive', 'MV', 'MDV', 462),
('Mal', 'ML', 'MLI', 466),
('Malt', 'MT', 'MLT', 470),
('Marshall Island', 'MH', 'MHL', 584),
('Martiniqu', 'MQ', 'MTQ', 474),
('Mauritani', 'MR', 'MRT', 478),
('Mauritiu', 'MU', 'MUS', 480),
('Mayotte', 'YT', 'MYT', 175),
('Mexic', 'MX', 'MEX', 484),
('Micronesia, Federated States of', 'FM', 'FSM', 583),
('Moldova', 'MD', 'MDA', 498),
('Monac', 'MC', 'MCO', 492),
('Mongoli', 'MN', 'MNG', 496),
('Montenegr', 'ME', 'MNE', 499),
('Montserra', 'MS', 'MSR', 500),
('Morocco', 'MA', 'MAR', 504),
('Mozambiqu', 'MZ', 'MOZ', 508),
('Myanmar', 'MM', 'MMR', 104),
('Namibia', 'NA', 'NAM', 516),
('Naur', 'NR', 'NRU', 520),
('Nepa', 'NP', 'NPL', 524),
('Netherlands', 'NL', 'NLD', 528),
('Netherlands Antille', 'AN', 'ANT', 530),
('New Caledoni', 'NC', 'NCL', 540),
('New Zealand', 'NZ', 'NZL', 554),
('Nicaragu', 'NI', 'NIC', 558),
('Nige', 'NE', 'NER', 562),
('Nigeria', 'NG', 'NGA', 566),
('Niu', 'NU', 'NIU', 570),
('Norfolk Islan', 'NF', 'NFK', 574),
('Northern Mariana Island', 'MP', 'MNP', 580),
('Norwa', 'NO', 'NOR', 578),
('Oma', 'OM', 'OMN', 512),
('Pakista', 'PK', 'PAK', 586),
('Pala', 'PW', 'PLW', 585),
('Palestinian Territor', 'PS', 'PSE', 275),
('Panam', 'PA', 'PAN', 591),
('Papua New Guine', 'PG', 'PNG', 598),
('Paragua', 'PY', 'PRY', 600),
('Per', 'PE', 'PER', 604),
('Philippines', 'PH', 'PHL', 608),
('Pitcair', 'PN', 'PCN', 612),
('Polan', 'PL', 'POL', 616),
('Portuga', 'PT', 'PRT', 620),
('Puerto Rico', 'PR', 'PRI', 630),
('Qata', 'QA', 'QAT', 634),
('Réunion', 'RE', 'REU', 638),
('Romania', 'RO', 'ROU', 642),
('Russian Federatio', 'RU', 'RUS', 643),
('Rwand', 'RW', 'RWA', 646),
('Saint-Barthélem', 'BL', 'BLM', 652),
('Saint Helen', 'SH', 'SHN', 654),
('Saint Kitts and Nevi', 'KN', 'KNA', 659),
('Saint Lucia', 'LC', 'LCA', 662),
('Saint-Martin (French part', 'MF', 'MAF', 663),
('Saint Pierre and Miquelo', 'PM', 'SPM', 666),
('Saint Vincent and Grenadine', 'VC', 'VCT', 670),
('Samo', 'WS', 'WSM', 882),
('San Marin', 'SM', 'SMR', 674),
('Sao Tome and Princip', 'ST', 'STP', 678),
('Saudi Arabi', 'SA', 'SAU', 682),
('Senegal', 'SN', 'SEN', 686),
('Serbi', 'RS', 'SRB', 688),
('Seychelle', 'SC', 'SYC', 690),
('Sierra Leon', 'SL', 'SLE', 694),
('Singapor', 'SG', 'SGP', 702),
('Slovaki', 'SK', 'SVK', 703),
('Sloveni', 'SI', 'SVN', 705),
('Solomon Islands', 'SB', 'SLB', 090),
('Somalia', 'SO', 'SOM', 706),
('South Afric', 'ZA', 'ZAF', 710),
('South Georgia and the South Sandwich Island', 'GS', 'SGS', 239),
('South Sudan', 'SS', 'SSD', 728),
('Spai', 'ES', 'ESP', 724),
('Sri Lank', 'LK', 'LKA', 144),
('Suda', 'SD', 'SDN', 736),
('Surinam', 'SR', 'SUR', 740),
('Svalbard and Jan Mayen Island', 'SJ', 'SJM', 744),
('Swazilan', 'SZ', 'SWZ', 748),
('Swede', 'SE', 'SWE', 752),
('Switzerland', 'CH', 'CHE', 756),
('Syrian Arab Republic (Syria', 'SY', 'SYR', 760),
('Taiwan, Republic of Chin', 'TW', 'TWN', 158),
('Tajikista', 'TJ', 'TJK', 762),
('Tanzania, United Republic o', 'TZ', 'TZA', 834),
('Thailan', 'TH', 'THA', 764),
('Timor-Leste', 'TL', 'TLS', 626),
('Tog', 'TG', 'TGO', 768),
('Tokelau', 'TK', 'TKL', 772),
('Tong', 'TO', 'TON', 776),
('Trinidad and Tobago', 'TT', 'TTO', 780),
('Tunisia', 'TN', 'TUN', 788),
('Turke', 'TR', 'TUR', 792),
('Turkmenista', 'TM', 'TKM', 795),
('Turks and Caicos Island', 'TC', 'TCA', 796),
('Tuval', 'TV', 'TUV', 798),
('Ugand', 'UG', 'UGA', 800),
('Ukraine', 'UA', 'UKR', 804),
('United Arab Emirate', 'AE', 'ARE', 784),
('United Kingdo', 'GB', 'GBR', 826),
('United States of Americ', 'US', 'USA', 840),
('US Minor Outlying Island', 'UM', 'UMI', 581),
('Uruguay', 'UY', 'URY', 858),
('Uzbekista', 'UZ', 'UZB', 860),
('Vanuatu', 'VU', 'VUT', 548),
('Venezuela (Bolivarian Republic)', 'VE', 'VEN', 862),
('Viet Na', 'VN', 'VNM', 704),
('Virgin Islands, U', 'VI', 'VIR', 850),
('Wallis and Futuna Island', 'WF', 'WLF', 876),
('Western Sahar', 'EH', 'ESH', 732),
('Yeme', 'YE', 'YEM', 887),
('Zambi', 'ZM', 'ZMB', 894),
('Zimbabwe', 'ZW', 'ZWE', 716);
