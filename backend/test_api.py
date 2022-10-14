def members():
    return {
        'members': ["member1", "member2", "member3", "member4"]
    }


routes = [{'url': '/api/members',
           'name': 'members',
           'fn': members,
           'methods': ['GET']}]
