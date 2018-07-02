-- CREATE DATABASE "aquila";
-- CREATE USER "aquila" WITH PASSWORD 'aquila2018';
-- GRANT ALL PRIVILEGES ON DATABASE aquila TO aquila;

/*
Index candidates:
rooms.joined_date
*/

CREATE TABLE levels (
	level SMALLINT PRIMARY KEY,
	exp_thru INT
);

CREATE TABLE countries (
	id SMALLINT PRIMARY KEY,
	name VARCHAR
);

CREATE TABLE rooms (
	id SERIAL PRIMARY KEY,
	player_id_list INTEGER ARRAY
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
	room_id SMALLINT REFERENCES rooms,
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
	id SERIAL PRIMARY KEY,
	room_id INT REFERENCES rooms, 
	player_id INT REFERENCES players,
	entry_date TIMESTAMP,
	leave_date TIMESTAMP
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


-- Static content

-- Insert 1000 rooms
INSERT INTO rooms (player_id_list) VALUES ('{}');
INSERT INTO rooms (player_id_list)
SELECT tmp.player_id_list FROM
(SELECT player_id_list, generate_series(1, 999) FROM rooms) tmp;


INSERT INTO countries VALUES
(1, 'Afghanistan'),
(2, 'Albania'),
(3, 'Algeria'),
(4, 'American Samoa'),
(5, 'Andorra'),
(6, 'Angola'),
(7, 'Anguilla'),
(8, 'Antigua & Barbuda'),
(9, 'Argentina'),
(10, 'Armenia'),
(11, 'Aruba'),
(12, 'Australia'),
(13, 'Austria'),
(14, 'Azerbaijan'),
(15, 'Bahamas, The'),
(16, 'Bahrain'),
(17, 'Bangladesh'),
(18, 'Barbados'),
(19, 'Belarus'),
(20, 'Belgium'),
(21, 'Belize'),
(22, 'Benin'),
(23, 'Bermuda'),
(24, 'Bhutan'),
(25, 'Bolivia'),
(26, 'Bosnia & Herzegovina'),
(27, 'Botswana'),
(28, 'Brazil'),
(29, 'British Virgin Is.'),
(30, 'Brunei'),
(31, 'Bulgaria'),
(32, 'Burkina Faso'),
(33, 'Burma'),
(34, 'Burundi'),
(35, 'Cambodia'),
(36, 'Cameroon'),
(37, 'Canada'),
(38, 'Cape Verde'),
(39, 'Cayman Islands'),
(40, 'Central African Rep.'),
(41, 'Chad'),
(42, 'Chile'),
(43, 'China'),
(44, 'Colombia'),
(45, 'Comoros'),
(46, 'Congo, Dem. Rep.'),
(47, 'Congo, Repub. of the'),
(48, 'Cook Islands'),
(49, 'Costa Rica'),
(50, 'Cote d\'Ivoire'),
(51, 'Croatia'),
(52, 'Cuba'),
(53, 'Cyprus'),
(54, 'Czech Republic'),
(55, 'Denmark'),
(56, 'Djibouti'),
(57, 'Dominica'),
(58, 'Dominican Republic'),
(59, 'East Timor'),
(60, 'Ecuador'),
(61, 'Egypt'),
(62, 'El Salvador'),
(63, 'Equatorial Guinea'),
(64, 'Eritrea'),
(65, 'Estonia'),
(66, 'Ethiopia'),
(67, 'Faroe Islands'),
(68, 'Fiji'),
(69, 'Finland'),
(70, 'France'),
(71, 'French Guiana'),
(72, 'French Polynesia'),
(73, 'Gabon'),
(74, 'Gambia, The'),
(75, 'Gaza Strip'),
(76, 'Georgia'),
(77, 'Germany'),
(78, 'Ghana'),
(79, 'Gibraltar'),
(80, 'Greece'),
(81, 'Greenland'),
(82, 'Grenada'),
(83, 'Guadeloupe'),
(84, 'Guam'),
(85, 'Guatemala'),
(86, 'Guernsey'),
(87, 'Guinea'),
(88, 'Guinea-Bissau'),
(89, 'Guyana'),
(90, 'Haiti'),
(91, 'Honduras'),
(92, 'Hong Kong'),
(93, 'Hungary'),
(94, 'Iceland'),
(95, 'India'),
(96, 'Indonesia'),
(97, 'Iran'),
(98, 'Iraq'),
(99, 'Ireland'),
(100, 'Isle of Man'),
(101, 'Israel'),
(102, 'Italy'),
(103, 'Jamaica'),
(104, 'Japan'),
(105, 'Jersey'),
(106, 'Jordan'),
(107, 'Kazakhstan'),
(108, 'Kenya'),
(109, 'Kiribati'),
(110, 'Korea, North'),
(111, 'Korea, South'),
(112, 'Kuwait'),
(113, 'Kyrgyzstan'),
(114, 'Laos'),
(115, 'Latvia'),
(116, 'Lebanon'),
(117, 'Lesotho'),
(118, 'Liberia'),
(119, 'Libya'),
(120, 'Liechtenstein'),
(121, 'Lithuania'),
(122, 'Luxembourg'),
(123, 'Macau'),
(124, 'Macedonia'),
(125, 'Madagascar'),
(126, 'Malawi'),
(127, 'Malaysia'),
(128, 'Maldives'),
(129, 'Mali'),
(130, 'Malta'),
(131, 'Marshall Islands'),
(132, 'Martinique'),
(133, 'Mauritania'),
(134, 'Mauritius'),
(135, 'Mayotte'),
(136, 'Mexico'),
(137, 'Micronesia, Fed. St.'),
(138, 'Moldova'),
(139, 'Monaco'),
(140, 'Mongolia'),
(141, 'Montserrat'),
(142, 'Morocco'),
(143, 'Mozambique'),
(144, 'Namibia'),
(145, 'Nauru'),
(146, 'Nepal'),
(147, 'Netherlands'),
(148, 'Netherlands Antilles'),
(149, 'New Caledonia'),
(150, 'New Zealand'),
(151, 'Nicaragua'),
(152, 'Niger'),
(153, 'Nigeria'),
(154, 'N. Mariana Islands'),
(155, 'Norway'),
(156, 'Oman'),
(157, 'Pakistan'),
(158, 'Palau'),
(159, 'Panama'),
(160, 'Papua New Guinea'),
(161, 'Paraguay'),
(162, 'Peru'),
(163, 'Philippines'),
(164, 'Poland'),
(165, 'Portugal'),
(166, 'Puerto Rico'),
(167, 'Qatar'),
(168, 'Reunion'),
(169, 'Romania'),
(170, 'Russia'),
(171, 'Rwanda'),
(172, 'Saint Helena'),
(173, 'Saint Kitts & Nevis'),
(174, 'Saint Lucia'),
(175, 'St Pierre & Miquelon'),
(176, 'Saint Vincent and the Grenadines'),
(177, 'Samoa'),
(178, 'San Marino'),
(179, 'Sao Tome & Principe'),
(180, 'Saudi Arabia'),
(181, 'Senegal'),
(182, 'Serbia'),
(183, 'Seychelles'),
(184, 'Sierra Leone'),
(185, 'Singapore'),
(186, 'Slovakia'),
(187, 'Slovenia'),
(188, 'Solomon Islands'),
(189, 'Somalia'),
(190, 'South Africa'),
(191, 'Spain'),
(192, 'Sri Lanka'),
(193, 'Sudan'),
(194, 'Suriname'),
(195, 'Swaziland'),
(196, 'Sweden'),
(197, 'Switzerland'),
(198, 'Syria'),
(199, 'Taiwan'),
(200, 'Tajikistan'),
(201, 'Tanzania'),
(202, 'Thailand'),
(203, 'Togo'),
(204, 'Tonga'),
(205, 'Trinidad & Tobago'),
(206, 'Tunisia'),
(207, 'Turkey'),
(208, 'Turkmenistan'),
(209, 'Turks & Caicos Is'),
(210, 'Tuvalu'),
(211, 'Uganda'),
(212, 'Ukraine'),
(213, 'United Arab Emirates'),
(214, 'United Kingdom'),
(215, 'United States'),
(216, 'Uruguay'),
(217, 'Uzbekistan'),
(218, 'Vanuatu'),
(219, 'Venezuela'),
(220, 'Vietnam'),
(221, 'Virgin Islands'),
(222, 'Wallis and Futuna'),
(223, 'West Bank'),
(224, 'Western Sahara'),
(225, 'Yemen'),
(226, 'Zambia'),
(227, 'Zimbabwe');
