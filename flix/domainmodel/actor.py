from typing import List


class Actor:
    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_full_name.strip()

        self.__colleagues: List[str] = list()

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    def add_actor_colleague(self, colleague: str):
        self.__colleagues.append(colleague)

    def check_if_this_actor_worked_with(self, colleague):
        if colleague in self.__colleagues:
            return True
        else:
            return False

    def __repr__(self):
        return f"<Actor {self.__actor_full_name}>"

    def __eq__(self, other):
        if self.__actor_full_name == other.actor_full_name:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.__actor_full_name < other.actor_full_name:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.__actor_full_name)


"""
actor1 = Actor("Angelina Jolie")
print(actor1)

actor1.add_actor_colleague("Brad Pitt")
actor1.add_actor_colleague("Tom Cruise")
actor1.add_actor_colleague("Lauren German")

print(actor1.check_if_this_actor_worked_with("Lauren German"))

print()

print(actor1.check_if_this_actor_worked_with(Actor("Lauren German")))
print("x")
print(actor1 == Actor("Angelina Jolie"))
"""
