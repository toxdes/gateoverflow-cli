create_tables = '''
CREATE TABLE IF NOT EXISTS recents(
    question_id INTEGER PRIMARY KEY, 
    visited_count INTEGER NOT NULL DEFAULT 1, 
    metadata_scraped INTEGER DEFAULT 0,
    last_visited INTEGER(4) NOT NULL DEFAULT (STRFTIME('%s','now'))
    );
CREATE TABLE IF NOT EXISTS metadata(
    question_id INTEGER PRIMARY KEY,
    title VARCHAR(120) NOT NULL,
    desc VARCHAR(240) NOT NULL,
    image_url VARCHAR(240) NOT NULL
);
CREATE TABLE IF NOT EXISTS tags(
    id INTEGER PRIMARY KEY AUTOINCREMENT DEFAULT 1,
    name varchar(240) NOT NULL,
    questions_count INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS tq_relation(
    id INTEGER PRIMARY KEY DEFAULT 1,
    question_id INTEGER NOT NULL REFERENCES recents(question_id),
    tag_id INTEGER NOT NULL REFERENCES tags(id)
);
'''

create_triggers = '''
CREATE TRIGGER IF NOT EXISTS [update_last_visited]
AFTER UPDATE OF visited_count
ON recents
BEGIN
UPDATE recents SET last_visited = (STRFTIME('%s','now')) WHERE question_id = old.question_id;
END
'''
insert_dummy_values = '''
    INSERT or REPLACE INTO recents(question_id, visited_count) VALUES (22, 12);
    INSERT or REPLACE INTO recents(question_id, visited_count) VALUES (1212, 1);
    INSERT or REPLACE INTO recents(question_id, visited_count) VALUES (12, 22);
    INSERT or REPLACE INTO recents(question_id, visited_count) VALUES (12, 23);
    INSERT or REPLACE INTO recents(question_id, visited_count) VALUES (12, 32);
    INSERT or REPLACE INTO recents(question_id, visited_count) VALUES (22, 4);
    INSERT or REPLACE INTO recents(question_id, visited_count) VALUES (23, 5);
    insert into tags(name) values ("important");
    insert into tags(name) values ("tricky");
    insert into tags(name) values ("read-later");
    insert into tags(name) values ("superimportant");
    insert into tags(name) values ("wrongly-attempted");
    insert into tags(name) values ("easy");
    '''

get_all = "SELECT * from recents;"
