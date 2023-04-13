SELECT
        u._user as user_id,
        u.nickname as nickname,
        u.password as password,
        u.publicInfo as publicInfo,
        u.privateInfo as privateInfo,
        u.isVip as isVip,
        u.additional as additional,
        u.image as img
    FROM usert u
    WHERE u.nickname = %(user)s