from models.table_def import Group


def query_groups_color(s):
    s.query(Group.group_color).all()
