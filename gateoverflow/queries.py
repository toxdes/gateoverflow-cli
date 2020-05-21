# Most static queries are listed here, yet there are a few cases where it's kinda easier if they are generated dynamically

create_tables = '''
CREATE TABLE IF NOT EXISTS user(
    name varchar(200),
    username varchar(200)
);
CREATE TABLE IF NOT EXISTS recents(
    question_id INTEGER PRIMARY KEY,
    visited_count INTEGER NOT NULL DEFAULT 1,
    metadata_scraped INTEGER DEFAULT 0,
    crawl_attempts INTEGER DEFAULT 1,
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

# TODO: Find a better way to change existing database-structure on the fly, like adding a column
alter_tables = '''

'''
create_triggers = '''
CREATE TRIGGER IF NOT EXISTS [update_last_visited]
AFTER UPDATE OF visited_count
ON recents
BEGIN
UPDATE recents SET last_visited =(STRFTIME('%s','now')) WHERE question_id = old.question_id;
END
'''
create_default_tags = '''
INSERT OR REPLACE INTO tags(id, name, questions_count) VALUES (1,'important',(SELECT COUNT(*) FROM tq_relation WHERE tag_id=1));
INSERT OR REPLACE INTO tags(id, name, questions_count) VALUES (2,'tricky',(SELECT COUNT(*) FROM tq_relation WHERE tag_id=2));
INSERT OR REPLACE INTO tags(id, name, questions_count) VALUES (3,'read-later',(SELECT COUNT(*) FROM tq_relation WHERE tag_id=3));
INSERT OR REPLACE INTO tags(id, name, questions_count) VALUES (4,'super-important',(SELECT COUNT(*) FROM tq_relation WHERE tag_id=4));
INSERT OR REPLACE INTO tags(id, name, questions_count) VALUES (5,'wrongly-attempted',(SELECT COUNT(*) FROM tq_relation WHERE tag_id=5));
INSERT OR REPLACE INTO tags(id, name, questions_count) VALUES (6,'easy',(SELECT COUNT(*) FROM tq_relation WHERE tag_id=6));
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
uncrawled_metadata_count = "SELECT COUNT(*) FROM recents WHERE metadata_scraped=0"
get_unscraped_question_ids = "SELECT question_id FROM recents WHERE metadata_scraped=0"
insert_into_metadata = 'INSERT OR REPLACE INTO metadata(question_id, title, desc, image_url) values(?,?,?,?)'
update_metadata_scraped_questions = 'UPDATE recents SET metadata_scraped=1 WHERE question_id=?'


update_visited_count = "UPDATE recents SET visited_count=(SELECT visited_count FROM recents WHERE question_id=?)+1  where question_id=?"
get_question = "SELECT * FROM recents WHERE question_id=?"
insert_into_recents = "INSERT INTO recents(question_id) values(?)"

get_recent = '''
select recents.question_id, title, desc, visited_count, last_visited from
recents left join metadata on
recents.question_id = metadata.question_id
order by last_visited desc, visited_count desc LIMIT ? OFFSET ?;'''

# get_recent = "SELECT question_id, visited_count, last_visited FROM recents ORDER BY last_visited DESC, visited_count DESC  LIMIT ? OFFSET ?"

get_tags = "SELECT name, questions_count FROM tags ORDER BY questions_count DESC;"
update_crawl_attempts = "UPDATE recents set crawl_attempts=crawl_attempts+1 where question_id=?"
delete_invalid_questions = "DELETE from recents where crawl_attempts>?"
create_user = "INSERT OR REPLACE INTO user(username, name) VALUES (?,?);"
get_user = "SELECT * from user;"
update_questions_count = 'UPDATE tags SET questions_count=questions_count+1 WHERE id=?'
