def is_teststep(member):
    return hasattr(member, 'start') and hasattr(member, 'end') and callable(member)
