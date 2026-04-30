from config import CARGO_STAFF

def is_staff(member):
    return any(role.id == CARGO_STAFF for role in member.roles)