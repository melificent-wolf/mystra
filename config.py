from dotenv import dotenv_values


class Config():
    def __init__(self):
        cfg = dotenv_values(".env")
        self.admin_role = cfg['ADMIN_ROLE']
        self.mod_role = cfg['MOD_ROLE']
        self.newcomer_role = cfg['NEWCOMER_ROLE']
