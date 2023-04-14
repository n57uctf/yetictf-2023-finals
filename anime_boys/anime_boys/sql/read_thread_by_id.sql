SELECT
        t._thread as thread_id,
        t.name as name,
        t.description as description,
        t.group_ as group_id
    FROM Thread t
    WHERE t._thread = %(id)s