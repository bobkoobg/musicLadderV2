CREATE DATABASE IF NOT EXISTS music_ladder;

USE music_ladder;

DROP TABLE IF EXISTS game_TBL;
DROP TABLE IF EXISTS song_tournament_TBL;
DROP TABLE IF EXISTS song_TBL;
DROP TABLE IF EXISTS tournament_TBL;
DROP TABLE IF EXISTS user_TBL;

CREATE TABLE IF NOT EXISTS user_TBL (
	id INT AUTO_INCREMENT,
	username VARCHAR(255) NOT NULL,
	hashed_password VARCHAR(255) NOT NULL,
	full_name VARCHAR(255) NOT NULL,
	alias VARCHAR(255) NOT NULL,
	motto VARCHAR(255),
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS tournament_TBL (
	id INT AUTO_INCREMENT,
	title VARCHAR(255) NOT NULL,
	tournament_type VARCHAR(255) NOT NULL,
	state VARCHAR(255) NOT NULL,
	round INT DEFAULT 0,
	user_id INT NOT NULL,
	creation_time DATETIME DEFAULT CURRENT_TIMESTAMP,
	modification_time DATETIME ON UPDATE CURRENT_TIMESTAMP,
	description TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY (user_id)
		REFERENCES user_TBL(id),
	INDEX user_id_index (user_id)
);

delimiter //
CREATE TRIGGER tournament_before_insert_check BEFORE INSERT ON tournament_TBL
	FOR EACH ROW
	BEGIN
		IF NEW.tournament_type NOT IN ('elimination','cup','ladder') OR NEW.state NOT IN ('open','running','finished') THEN
			signal sqlstate '45000';
		END IF;
	END;
// delimiter ;

delimiter //
CREATE TRIGGER tournament_before_update_check BEFORE UPDATE ON tournament_TBL
	FOR EACH ROW
	BEGIN
		IF NEW.tournament_type NOT IN ('elimination','cup','ladder') OR NEW.state NOT IN ('open','running','finished') THEN
			signal sqlstate '45000';
		END IF;
	END;
// delimiter ;

CREATE TABLE IF NOT EXISTS song_TBL (
	id INT AUTO_INCREMENT,
	title VARCHAR(255) NOT NULL,
	url VARCHAR(255) NOT NULL,
	user_id INT NOT NULL,
	creation_time DATETIME DEFAULT CURRENT_TIMESTAMP,
	modification_time DATETIME ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (id),
	FOREIGN KEY (user_id)
		REFERENCES user_TBL(id),
	INDEX user_id_index (user_id)
);

CREATE TABLE IF NOT EXISTS song_tournament_TBL (
	tournament_id INT NOT NULL,
	song_id INT NOT NULL,
	user_id INT NOT NULL,
	active BOOLEAN DEFAULT True,
	rating INT NOT NULL DEFAULT 1000,
	matches INT NOT NULL DEFAULT 0,
	wins INT NOT NULL DEFAULT 0,
	draws INT NOT NULL DEFAULT 0,
	losses INT NOT NULL DEFAULT 0,
	creation_time DATETIME DEFAULT CURRENT_TIMESTAMP,
	modification_time DATETIME ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (tournament_id,song_id),
	FOREIGN KEY (tournament_id)
		REFERENCES tournament_TBL(id),
	FOREIGN KEY (song_id)
		REFERENCES song_TBL(id),
	FOREIGN KEY (user_id)
		REFERENCES user_TBL(id),
	INDEX song_by_tournament_index (tournament_id,song_id),
	INDEX tournament_creation_index (tournament_id,active),
	INDEX user_id_index (user_id),
	INDEX song_by_tournament_and_user_index (tournament_id,song_id,user_id)
);

delimiter //
CREATE TRIGGER song_after_insert_check AFTER INSERT ON song_TBL
	FOR EACH ROW
	BEGIN
		INSERT INTO song_tournament_TBL (tournament_id,song_id,user_id) VALUES (1,NEW.id,NEW.user_id);
	END;
// delimiter ;

CREATE TABLE IF NOT EXISTS game_TBL (
	id INT AUTO_INCREMENT,
	tournament_id INT NOT NULL,
	user_id INT NOT NULL,
	state BOOLEAN DEFAULT False, #if match is done or not
	round INT DEFAULT -1, #which is the current round, useful for elimination and cup
	song_left_id INT NOT NULL,
	song_left_before_rating INT NOT NULL,
	song_left_after_rating INT DEFAULT -1,
	song_left_score INT DEFAULT -1,
	song_right_score INT DEFAULT -1,
	song_right_after_rating INT DEFAULT -1,
	song_right_before_rating INT NOT NULL,
	song_right_id INT NOT NULL,
	creation_time DATETIME DEFAULT CURRENT_TIMESTAMP,
	modification_time DATETIME ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (id),
	FOREIGN KEY (tournament_id)
		REFERENCES tournament_TBL(id),
	FOREIGN KEY (song_left_id)
		REFERENCES song_TBL(id),
	FOREIGN KEY (song_right_id)
		REFERENCES song_TBL(id),
	FOREIGN KEY (user_id)
		REFERENCES user_TBL(id),
	INDEX update_finish_index (tournament_id,song_left_id,song_right_id),
	INDEX song_left_id_index (song_left_id),
	INDEX song_right_id_index (song_right_id),
	INDEX tournament_id_index (tournament_id),
	INDEX user_id_index (user_id)
);

delimiter //
CREATE TRIGGER game_before_insert_check BEFORE INSERT ON game_TBL
	FOR EACH ROW
	BEGIN
        DECLARE game_state INT DEFAULT 0;
        DECLARE tournament_state VARCHAR(255) DEFAULT False;

        SET tournament_state = (SELECT state FROM tournament_TBL WHERE id = NEW.tournament_id);

		IF tournament_state in ('finished') THEN
			signal sqlstate '45000';
        END IF;

		IF NEW.song_left_score > NEW.song_right_score THEN
			SET game_state = 1;
		END IF;
		IF NEW.song_left_score < NEW.song_right_score THEN
			SET game_state = -1;
		END IF;

		IF NEW.round = -1 THEN
			SET NEW.round = (
				SELECT round
					FROM tournament_TBL
                    WHERE id = NEW.tournament_id
			);
        END IF;

        SET NEW.song_left_before_rating = (
			SELECT rating
				FROM song_tournament_TBL
				WHERE tournament_id = NEW.tournament_id AND song_id = NEW.song_left_id
		);

        SET NEW.song_right_before_rating = (
			SELECT rating
				FROM song_tournament_TBL
				WHERE tournament_id = NEW.tournament_id AND song_id = NEW.song_right_id
		);

		IF NEW.song_left_after_rating != -1 THEN
			IF NEW.song_left_score = -1 THEN
			   signal sqlstate '45000';
			END IF;

            IF NEW.song_left_score > NEW.song_right_score THEN
				UPDATE song_tournament_TBL
					SET rating = NEW.song_left_after_rating,
						matches = matches + 1,
						wins = wins + 1
					WHERE tournament_id = NEW.tournament_id AND song_id = NEW.song_left_id;
			ELSEIF NEW.song_left_score < NEW.song_right_score THEN
				UPDATE song_tournament_TBL
					SET rating = NEW.song_left_after_rating,
						matches = matches + 1,
						losses = losses + 1
					WHERE tournament_id = NEW.tournament_id AND song_id = NEW.song_left_id;
			ELSEIF NEW.song_left_score = NEW.song_right_score THEN
				UPDATE song_tournament_TBL
					SET rating = NEW.song_left_after_rating,
						matches = matches + 1,
						draws = draws + 1
					WHERE tournament_id = NEW.tournament_id AND song_id = NEW.song_left_id;
			END IF;

		END IF;

		IF NEW.song_right_after_rating != -1 THEN
			IF NEW.song_right_score = -1 THEN
			   signal sqlstate '45000';
			END IF;

			IF NEW.song_left_score > NEW.song_right_score THEN
				UPDATE song_tournament_TBL
					SET rating = NEW.song_right_after_rating,
						matches = matches + 1,
						losses = losses + 1
					WHERE tournament_id = NEW.tournament_id AND song_id = NEW.song_right_id;
			ELSEIF NEW.song_left_score < NEW.song_right_score THEN
				UPDATE song_tournament_TBL
					SET rating = NEW.song_right_after_rating,
						matches = matches + 1,
						wins = wins + 1
					WHERE tournament_id = NEW.tournament_id AND song_id = NEW.song_right_id;
			ELSEIF NEW.song_left_score = NEW.song_right_score THEN
				UPDATE song_tournament_TBL
					SET rating = NEW.song_right_after_rating,
						matches = matches + 1,
						draws = draws + 1
					WHERE tournament_id = NEW.tournament_id AND song_id = NEW.song_right_id;
			END IF;
		END IF;

        IF NEW.song_left_after_rating != -1 AND NEW.song_left_score != -1 AND
			NEW.song_right_after_rating != -1 AND NEW.song_right_score != -1 THEN
            SET NEW.state = 1;
		END IF;
	END;
// delimiter ;

delimiter //
CREATE TRIGGER game_before_update_check BEFORE UPDATE ON game_TBL
	FOR EACH ROW
	BEGIN
        DECLARE game_state INT DEFAULT 0;
        DECLARE tournament_state VARCHAR(255) DEFAULT False;

        SET tournament_state = (SELECT state FROM tournament_TBL WHERE id = NEW.tournament_id);

		IF tournament_state in ('finished') THEN
			signal sqlstate '45000';
        END IF;

		IF NEW.song_left_score > NEW.song_right_score THEN
			SET game_state = 1;
		END IF;
		IF NEW.song_left_score < NEW.song_right_score THEN
			SET game_state = -1;
		END IF;

        IF NEW.round = -1 THEN
			SET NEW.round = (
				SELECT round
					FROM tournament_TBL
                    WHERE id = NEW.tournament_id
			);
        END IF;

        SET NEW.song_left_before_rating = (
			SELECT rating
				FROM song_tournament_TBL
				WHERE tournament_id = NEW.tournament_id AND song_id = NEW.song_left_id
		);

        SET NEW.song_right_before_rating = (
			SELECT rating
				FROM song_tournament_TBL
				WHERE tournament_id = NEW.tournament_id AND song_id = NEW.song_right_id
		);

		IF NEW.song_left_after_rating != -1 THEN
			IF NEW.song_left_score = -1 THEN
			   signal sqlstate '45000';
			END IF;

            IF NEW.song_left_score > NEW.song_right_score THEN
				UPDATE song_tournament_TBL
					SET rating = NEW.song_left_after_rating,
						matches = matches + 1,
						wins = wins + 1
					WHERE tournament_id = NEW.tournament_id AND song_id = NEW.song_left_id;
			ELSEIF NEW.song_left_score < NEW.song_right_score THEN
				UPDATE song_tournament_TBL
					SET rating = NEW.song_left_after_rating,
						matches = matches + 1,
						losses = losses + 1
					WHERE tournament_id = NEW.tournament_id AND song_id = NEW.song_left_id;
			ELSEIF NEW.song_left_score = NEW.song_right_score THEN
				UPDATE song_tournament_TBL
					SET rating = NEW.song_left_after_rating,
						matches = matches + 1,
						draws = draws + 1
					WHERE tournament_id = NEW.tournament_id AND song_id = NEW.song_left_id;
			END IF;

		END IF;

		IF NEW.song_right_after_rating != -1 THEN
			IF NEW.song_right_score = -1 THEN
			   signal sqlstate '45000';
			END IF;

			IF NEW.song_left_score > NEW.song_right_score THEN
				UPDATE song_tournament_TBL
					SET rating = NEW.song_right_after_rating,
						matches = matches + 1,
						losses = losses + 1
					WHERE tournament_id = NEW.tournament_id AND song_id = NEW.song_right_id;
			ELSEIF NEW.song_left_score < NEW.song_right_score THEN
				UPDATE song_tournament_TBL
					SET rating = NEW.song_right_after_rating,
						matches = matches + 1,
						wins = wins + 1
					WHERE tournament_id = NEW.tournament_id AND song_id = NEW.song_right_id;
			ELSEIF NEW.song_left_score = NEW.song_right_score THEN
				UPDATE song_tournament_TBL
					SET rating = NEW.song_right_after_rating,
						matches = matches + 1,
						draws = draws + 1
					WHERE tournament_id = NEW.tournament_id AND song_id = NEW.song_right_id;
			END IF;
		END IF;

        IF NEW.song_left_after_rating != -1 AND NEW.song_left_score != -1 AND
			NEW.song_right_after_rating != -1 AND NEW.song_right_score != -1 THEN
            SET NEW.state = 1;
		END IF;
	END;
// delimiter ;

INSERT INTO user_TBL(username,hashed_password,full_name,alias) VALUES
	("bobkoo","qwerty12345","Boyko Surlev","bobkoo" );
INSERT INTO tournament_TBL (title,tournament_type,state,user_id) VALUES
	("Default","ladder","open",1), ("Katie's list","cup","open",1);
INSERT INTO song_TBL (title,url,user_id) VALUES
	("V:RGO x DIM - Ei Tuka Ei Tai [Official Video]","OCpJXSvzhAw",1),
	("VessoU - BAKSHISH [Official Video]","BEei9maHeIM",1),
    ("Nebezao feat. Rafal - Чёрная Пантера (Чёрном Панамера)","CzfvU8tKm5I",1),
    ("GRIVINA - Я люблю deep house (2018)","52AdOe0GRXs",1),
    ("Dara Ekimova - God is a woman x Чужди усмивки cover","IDfffZVBrsk",1),
    ("MONOIR feat. DARA - My Time (Lyric Video)","MniOhiXSRg8",1),
    ("100 KILA feat. Magi Djanavarova - Just the Two of Us (Official Video) 2018","F3M8U2rn1fY",1),
    ("GRIVINA - Я ХОЧУ","D_BlsEEvHXY",1);
    
INSERT INTO song_tournament_TBL (tournament_id,song_id,user_id) VALUES 
    (2,1,1),
    (2,2,1),
    (2,3,1),
    (2,4,1),
    (2,5,1),
    (2,6,1),
    (2,7,1),
    (2,8,1);

INSERT INTO game_TBL (tournament_id,user_id,state,song_left_id,song_left_after_rating,
	song_left_score,song_right_score,song_right_after_rating,song_right_id)
	VALUES (1,1,True,1,1000,5,5,1000,2);
INSERT INTO game_TBL (tournament_id,user_id,state,song_left_id,song_left_after_rating,
	song_left_score,song_right_score,song_right_after_rating,song_right_id)
	VALUES (1,1,True,1,1020,9,1,980,2);
INSERT INTO game_TBL (tournament_id,user_id,song_left_id,song_right_id) VALUES (1,1,1,2);
UPDATE game_TBL
	SET song_left_after_rating = 1010, song_left_score = 4, song_right_score = 6, song_right_after_rating = 990
	WHERE id = 3 AND tournament_id = 1 AND song_left_id = 1 AND song_right_id = 2;
INSERT INTO game_TBL (tournament_id,user_id,song_left_id,song_right_id) VALUES (1,1,1,2);

SELECT * FROM user_TBL;
SELECT * FROM song_TBL;
SELECT * FROM tournament_TBL ORDER BY creation_time DESC;
SELECT * FROM game_TBL;
SELECT * FROM game_TBL where tournament_id = 2 and ( song_left_id = 4 OR song_right_id = 4) and state = 1 ORDER BY id;
SELECT * FROM song_tournament_TBL WHERE tournament_id = 2 ORDER BY rating DESC;
SELECT * FROM tournament_TBL ORDER BY creation_time DESC;

#SELECT * FROM song_tournament_TBL WHERE tournament_id = 2 ORDER BY rating DESC;


#SELECT s.title, u.alias, st.rating, st.matches, 
#	st.wins, st.draws, st.losses
#                FROM song_tournament_TBL AS st 
#                INNER JOIN user_TBL AS u 
#                    ON u.id = st.user_id 
#                INNER JOIN song_TBL AS s 
#                    ON s.id = st.song_id 
#                WHERE st.tournament_id = 2 
#                ORDER BY st.rating DESC;

#SELECT s.title, st.rating, st.matches, st.wins, st.draws, st.losses
#                FROM song_tournament_TBL AS st
#                WHERE st.tournament_id = 2;
                
#SELECT * FROM song_tournament_TBL WHERE tournament_id = 2;

#SELECT
#	g.id, g.tournament_id, g.user_id, uc.alias,
#	g.state, g.round, g.song_left_id, s1.title, s1.url, u1.alias, 
#	g.song_left_before_rating, g.song_left_after_rating, g.song_left_score, 
#    g.song_right_score, g.song_right_after_rating, g.song_right_before_rating, 
#    g.song_right_id, s2.title, s2.url, u2.alias, g.creation_time, g.modification_time
#	FROM game_TBL AS g
#	INNER JOIN song_TBL AS s1
#		ON g.song_left_id = s1.id
#	INNER JOIN user_TBL AS u1
#		ON s1.user_id = u1.id
#	INNER JOIN song_TBL AS s2
#		ON g.song_right_id = s2.id
#	INNER JOIN user_TBL AS u2
#		ON s2.user_id = u2.id
#	INNER JOIN user_TBL AS uc
#		ON g.user_id = uc.id
#	WHERE g.tournament_id = 2
 #   ORDER BY g.round ASC;
    
    
    #UPDATE game_TBL
	#	SET song_left_before_rating = 1000, song_left_after_rating = 1010, song_left_score = 6,
	#		song_right_score = 1000, song_right_after_rating = 990, song_right_before_rating = 4
    #           WHERE id = 27 AND tournament_id = 2 AND song_left_id = 5 AND song_right_id = 4;
