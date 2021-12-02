-- Create 2 new players
SELECT "CREATES NEW PLAYERS-------------------";

INSERT INTO Player 
VALUES
    ('Kevin Durant' , 68, 150, '', 0, 'Underwater Basket Weaving');

INSERT INTO Player 
VALUES
    ('Giannis Antetokounmpo' , 71, 242, '', 0, 'Underwater Basket Weaving');

-- Create new sport
SELECT "CREATES NEW SPORT-------------------------------";

INSERT INTO Sport
VALUES
    ('Underwater Basket Weaving', 0, 0);

-- Create new league (1)
    --create the new league name within the sport, init # teams at 0, init leaguekey to whatever our max is +1
    --increment number of leagues under the sport by 1
SELECT "CREATES NEW LEAGUE------------------------------";

INSERT INTO League
VALUES
    ('Underwater Basket Weaving', 'UWBW League 1', 0, IFNULL( ((SELECT MAX(l_leaguekey) from league) + 1), 0));
    
UPDATE Sport
SET s_numleagues = s_numleagues + 1
WHERE
    s_name = 'Underwater Basket Weaving';

-- Create new team (and new record)
    --create new row within table
    --create new row within record
    --increment numteams for the league
    --increment numteams for the sport
SELECT "CREATES NEW TEAMS-------------------------------";

INSERT INTO Team
VALUES
    ( (SELECT l_leaguekey from league where l_name = 'UWBW League 1'), 0, 'Basket Gods');

INSERT INTO Record
VALUES
    ('Basket Gods', 0, 0);

UPDATE League
SET l_numteams = l_numteams + 1
WHERE
    l_name = 'UWBW League 1';

UPDATE Sport
SET s_numteams = s_numteams + 1
WHERE
    s_name = 'Underwater Basket Weaving';

    --inserting second team

INSERT INTO Team
VALUES
    ((SELECT l_leaguekey from league where l_name = 'UWBW League 1'), 0, 'Weavin Demons');

INSERT INTO Record
VALUES
    ('Weavin Demons', 0, 0);

UPDATE League
SET l_numteams = l_numteams + 1
WHERE
    l_name = 'UWBW League 1';

UPDATE Sport
SET s_numteams = s_numteams + 1
WHERE
    s_name = 'Underwater Basket Weaving';

-- Create new referee
SELECT "CREATES REFEREE-------------------------------";

INSERT INTO Referee
VALUES
    ('Underwater Basket Weaving', 'Sargune Kalsi', 5555555555, 3);

-- Create new match
SELECT "CREATES A MATCH ------------------------------";

INSERT INTO Match
VALUES
    ('Sargune Kalsi', 'Basket Gods', 'Weavin Demons', 15, 30, '1950-04-20');

-- Insert player into team
    --update the players team name based on name and sport
    --update t_numplayers row of team 
SELECT "ADDS KD PLAYER TO A TEAM ----------------------";
UPDATE Player
SET p_team ='Basket Gods' 
WHERE
    p_name = "Kevin Durant" and p_sport = "Underwater Basket Weaving";

UPDATE Team
SET t_numplayers = t_numplayers + 1
WHERE
    t_name = 'Basket Gods';
    
SELECT "ADDS GIANNIS PLAYER TO A TEAM ----------------------";
UPDATE Player
SET p_team ='Weavin Demons' 
WHERE
    p_name = "Giannis Antetokounmpo" and p_sport = "Underwater Basket Weaving";

UPDATE Team
SET t_numplayers = t_numplayers + 1
WHERE
    t_name = 'Weavin Demons';



-- Update Record
    --update r_wins row of record for winning team
    --update r_losses row of record for losing team
SELECT 'UPDATES RECORD----------------------------------';
UPDATE Record
SET r_wins = r_wins + 1
WHERE
    r_teamname = 'Weavin Demons';

UPDATE Record
SET r_losses = r_losses + 1
WHERE
    r_teamname = 'Basket Gods';


-- SETTING THE CAPTAIN FOR A TEAM
    --remove previous captain (if exists)
    --add new captain
UPDATE Player
SET p_captain = 0
WHERE
    p_captain = 1 and p_team = "Basket Gods";

UPDATE Player
SET p_captain = 1
WHERE
    p_name = "Kevin Durant" and p_team = "Basket Gods";

UPDATE Player
SET p_captain = 0
WHERE
    p_captain = 1 and p_team = "Weavin Demons";

UPDATE Player
SET p_captain = 1
WHERE
    p_name = "Giannis Antetokounmpo" and p_team = "Weavin Demons";


-- SELECTS ALL MATCHES FOR A TEAM, so a team can figure out their schedule
SELECT m_teamone, m_teamtwo, m_date, m_refname
FROM Match
WHERE
    m_teamone = 'Basket Gods' or m_teamtwo = 'Basket Gods';


-- Select team with best record in their league (2)
SELECT r_teamname, MAX(recProp)
FROM 
(
    SELECT r_teamname, (r_wins / (r_losses + 1)) as recProp
    FROM Record, Team, League
    WHERE
        r_teamname = t_name AND
        t_leaguekey = l_leaguekey AND
        l_name = 'UWBW League 1'
    GROUP BY r_teamname
);

-- Select team with worst record in their league
SELECT r_teamname, MIN(recProp)
FROM 
(
    SELECT r_teamname, (r_wins / (r_losses + 1)) as recProp
    FROM Record, Team, League
    WHERE
        r_teamname = t_name AND
        t_leaguekey = l_leaguekey AND
        l_name = 'UWBW League 1'
    GROUP BY r_teamname
);

-- Find the tallest players in a league
SELECT p_name, MAX(p_heightin)
FROM Player, Team, League
WHERE 
    t_name = p_team AND 
    l_leaguekey = t_leaguekey AND
    l_name = 'UWBW League 1';


-- Select captain names from matchup-date
Select m_date, player1.p_name, player2.p_name 
from player player1, player player2, match
where player1.p_team = m_teamone and 
player2.p_team = m_teamtwo and 
m_date = '1950-04-20' and 
player1.p_captain=1 
and player2.p_captain=1;

--complexity of queries, number of data tuples in the database(100s in each)



-- Remove player from team
    --update the players team name based on name nand sport
    --update t_numplayers row of team
SELECT "DELETES A PLAYER FROM A TEAM -------------------";
UPDATE Player
SET p_team = ''
WHERE
    p_name = "Kevin Durant" and p_sport = "Underwater Basket Weaving";

UPDATE Team
SET t_numplayers = t_numplayers - 1
WHERE
    t = 'Basket Gods';
