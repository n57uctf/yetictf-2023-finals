select
    g.user_ as user_id,
    g.group_ as group_id
    from groupuser g
    WHERE g.user_ = %(user_id)s