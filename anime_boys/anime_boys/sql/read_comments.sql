SELECT
        c.thread_ as thread_id,
        c.user_ as user_id,
        c.text as text,
        c._comment as comment_id,
        c._time as time
    FROM comment c
    WHERE c.thread_ = %(thread)s