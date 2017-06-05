# production = True
production = False


def get_database_host():
    if production:
        return 'localhost'
    else:
        return 'sddb.ece.iastate.edu'
