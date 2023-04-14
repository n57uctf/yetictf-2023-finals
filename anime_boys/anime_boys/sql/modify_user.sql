UPDATE UserT SET(publicInfo, privateInfo, IsVip) = (%(inputBio)s, %(inputPrivateBio)s, %(profileStatus)s)
        WHERE UserT.nickname = %(user)s