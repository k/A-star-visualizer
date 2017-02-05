def make_admissible(h):
    def h_admissable(s1, s2):
        return h(s1, s2)/4
    return h_admissable
