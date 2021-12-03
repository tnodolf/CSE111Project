--creating sport table
CREATE TABLE Sport (
    s_name          varchar(25),
    s_numteams      unsigned int,
    s_numleagues    unsigned int
);

--creating league table
CREATE TABLE League (
    l_sportsname    varchar(25),
    l_name          varchar(50),
    l_numteams      unsigned int,
    l_leaguekey     unsigned int
);

--creating referee table
CREATE TABLE Referee (
    r_sportsname    varchar(25),
    r_name          varchar(50),
    r_phonenumber   varchar(15),
    r_leaguekey     unsigned int
);

--creating matches table
CREATE TABLE Match (
    m_refname       varchar(50),
    m_teamone       varchar(50),
    m_teamtwo       varchar(50),
    m_teamonescore  unsigned int,
    m_teamtwoscore  unsigned int,
    m_date          date
);

--creating record table
CREATE TABLE Record (
    r_teamname      varchar(50),
    r_wins          unsigned int,
    r_losses        unsigned int
);

--creating teams table
CREATE TABLE Team (
    t_leaguekey     unsigned int,
    t_numplayers    unsigned int,
    t_name          varchar(50)
);

--creating player table
CREATE TABLE Player (
    p_name          varchar(50),
    p_heightin      unsigned int,
    p_weight        unsigned int,
    p_team          varchar(50),
    p_captain       unsigned int, --sqlite has no boolean data type so 0 corresponds to player, 1 corresponds to captain
    p_sport         varchar(25)
);

--populating sport table
INSERT INTO Sport
VALUES 
    ('Flag Football', 4, 1),
    ('Basketball'   , 8, 2);

--populating league table
INSERT INTO League 
VALUES 
    ('Fall 2021 Intramural', 'Flag Football', 4, 1),
    ('Fall 2021 Mens'      , 'Basketball'   , 4, 2);

--populating referee table
INSERT INTO Referee
VALUES
    ('Flag Football', 'Football Ref 1', '1112223333', 1),
    ('Flag Football', 'Football Ref 2', '2223334444', 1),
    ('Basketball', 'Basketball Ref 1', '1092389083', 2),
    ('Basketball', 'Basketball Ref 2', '2992328308', 2);
    
--populating match table
INSERT INTO Match
VALUES
    ('Football Ref 1'  , 'Team1', 'Team4', 0 , 60, '2021-11-14'),
    ('Football Ref 2'  , 'Team2', 'Team3', 20, 24, '2021-11-15'),
    ('Basketball Ref 1', 'Team5', 'Team8', 40, 55, '2021-11-15'),
    ('Basketball Ref 2', 'Team6', 'Team7', 50, 28, '2021-11-16');

--populating record table
INSERT INTO Record
VALUES 
    --basketball teams
    ('Team1', 0, 1),
    ('Team2', 0, 1),
    ('Team3', 1, 0),
    ('Team4', 1, 0),
    --football teams
    ('Team5', 0, 1),
    ('Team6', 1, 0),
    ('Team7', 0, 1),
    ('Team8', 1, 0);

--populating team table
INSERT INTO Team 
VALUES
    ('Fall 2021 Intramural', 8, 'Team1'),
    ('Fall 2021 Intramural', 8, 'Team2'),
    ('Fall 2021 Intramural', 7, 'Team3'),
    ('Fall 2021 Intramural', 7, 'Team4'),
    ('Fall 2021 Mens'      , 6, 'Team5'),
    ('Fall 2021 Mens'      , 6, 'Team6'),
    ('Fall 2021 Mens'      , 5, 'Team7'),
    ('Fall 2021 Mens'      , 5, 'Team8');

--populating player table
INSERT INTO Player
VALUES
    --Team1
    ('Player1' , 68, 150, 'Team1', 1, 'Flag Football'),
    ('Player2' , 67, 140, 'Team1', 0, 'Flag Football'),
    ('Player3' , 66, 140, 'Team1', 0, 'Flag Football'),
    ('Player4' , 69, 150, 'Team1', 0, 'Flag Football'),
    ('Player5' , 69, 160, 'Team1', 0, 'Flag Football'),
    ('Player6' , 70, 180, 'Team1', 0, 'Flag Football'),
    ('Player7' , 72, 165, 'Team1', 0, 'Flag Football'),
    ('Player8' , 65, 135, 'Team1', 0, 'Flag Football'),
    --Team2
    ('Player9' , 69, 165, 'Team2', 1, 'Flag Football'),
    ('Player10', 70, 170, 'Team2', 0, 'Flag Football'),
    ('Player11', 68, 180, 'Team2', 0, 'Flag Football'),
    ('Player12', 69, 170, 'Team2', 0, 'Flag Football'),
    ('Player13', 71, 185, 'Team2', 0, 'Flag Football'),
    ('Player14', 67, 145, 'Team2', 0, 'Flag Football'),
    ('Player15', 70, 175, 'Team2', 0, 'Flag Football'),
    ('Player16', 73, 170, 'Team2', 0, 'Flag Football'),

    --Team3
    ('Player17', 75, 200, 'Team3', 1, 'Flag Football'),
    ('Player18', 74, 190, 'Team3', 0, 'Flag Football'),
    ('Player19', 72, 230, 'Team3', 0, 'Flag Football'),
    ('Player20', 73, 245, 'Team3', 0, 'Flag Football'),
    ('Player21', 71, 200, 'Team3', 0, 'Flag Football'),
    ('Player22', 68, 190, 'Team3', 0, 'Flag Football'),
    ('Player23', 69, 210, 'Team3', 0, 'Flag Football'),

    --Team4
    ('Player24', 72, 176, 'Team4', 1, 'Flag Football'),
    ('Player25', 71, 167, 'Team4', 0, 'Flag Football'),
    ('Player26', 68, 170, 'Team4', 0, 'Flag Football'),
    ('Player27', 70, 180, 'Team4', 0, 'Flag Football'),
    ('Player28', 66, 190, 'Team4', 0, 'Flag Football'),
    ('Player29', 69, 160, 'Team4', 0, 'Flag Football'),
    ('Player30', 60, 165, 'Team4', 0, 'Flag Football'),
    
    --Team5
    ('Player31', 70, 140, 'Team5', 1, 'Basketball'),
    ('Player32', 67, 165, 'Team5', 0, 'Basketball'),
    ('Player33', 71, 185, 'Team5', 0, 'Basketball'),
    ('Player34', 76, 185, 'Team5', 0, 'Basketball'),
    ('Player35', 68, 150, 'Team5', 0, 'Basketball'),
    ('Player36', 68, 150, 'Team5', 0, 'Basketball'),

    --Team6
    ('Player37', 50, 135, 'Team6', 1, 'Basketball'),
    ('Player38', 59, 125, 'Team6', 0, 'Basketball'),
    ('Player39', 61, 157, 'Team6', 0, 'Basketball'),
    ('Player40', 58, 175, 'Team6', 0, 'Basketball'),
    ('Player41', 62, 126, 'Team6', 0, 'Basketball'),
    ('Player42', 56, 122, 'Team6', 0, 'Basketball'),
    
    --Team7
    ('Player43', 72, 144, 'Team7', 1, 'Basketball'),
    ('Player44', 89, 180, 'Team7', 0, 'Basketball'),
    ('Player45', 43, 150, 'Team7', 0, 'Basketball'),
    ('Player46', 65, 155, 'Team7', 0, 'Basketball'),
    ('Player47', 78, 130, 'Team7', 0, 'Basketball'),

    --Team8
    ('Player48', 43, 170, 'Team8', 1, 'Basketball'),
    ('Player49', 65, 90 , 'Team8', 0, 'Basketball'),
    ('Player50', 78, 160, 'Team8', 0, 'Basketball'),
    ('Player51', 39, 380, 'Team8', 0, 'Basketball'),
    ('Player52', 23, 120, 'Team8', 0, 'Basketball');

.headers on
select * from Sport;

--CLEANUP STATEMENT HERE
DROP TABLE IF EXISTS Sport;
DROP TABLE IF EXISTS League;
DROP TABLE IF EXISTS Referee;
DROP TABLE IF EXISTS Match;
DROP TABLE IF EXISTS Record;
DROP TABLE IF EXISTS Team;
DROP TABLE IF EXISTS Player;
