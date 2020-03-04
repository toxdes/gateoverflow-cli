create_tables = '''
CREATE TABLE IF NOT EXISTS recents(
    question_id INTEGER PRIMARY KEY, 
    visited_count INTEGER NOT NULL DEFAULT 1, 
    last_visited INTEGER(4) NOT NULL DEFAULT (STRFTIME('%s','now'))
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
    '''

get_all = "SELECT * from recents;"
