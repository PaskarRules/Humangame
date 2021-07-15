from TZ.models import Human

humans = []
children = []


def main():
    description()
    while True:
        menu()


def description():
    print(" Human's game! ")
    print("  You can create and breed humans!")
    print("  Good luck!")


def create_human():
    gender = input("gender - ")
    while True:
        if gender in ["boy", "girl"]:
            break
        gender = input("gender - ")

    return Human(
        name=input("Name - "),
        surname=input("Surname - "),
        gender=gender,
        age=int(input("Age - ")),
        city=input("City - "),
        country=input("Country - "),

    )


def make_child():
    if len(humans) < 2:
        print("Not enough people!")

    if any(human.gender == "girl" for human in humans) and any(human.gender == "boy" for human in humans):
        boy = choose_human("boy")
        girl = choose_human("girl")
        children.append(boy.breed(girl))
        return

    print("No one to breed!")


def choose_human(gender=""):
    if gender:
        filter_humans = [human for human in humans if human.gender == gender]
    else:
        filter_humans = humans

    for i in range(len(filter_humans)):
        print(f"{i + 1}. {filter_humans[i].name} {filter_humans[i].surname}")

    while True:
        choice = int(input("Choose human - "))
        if 1 <= choice <= len(filter_humans):
            return filter_humans[choice - 1]


def show_children():
    for i in range(len(children)):
        print(f"{i + 1}. {children[i].name} {children[i].surname}")


def menu():
    print("1. Create human."
          "2. Make child."
          "3. Info human."
          "4. Info children."
          "5. Exit.")

    choice = int(input("You choice - "))
    if choice == 1:
        humans.append(create_human())
    elif choice == 2:
        make_child()
    elif choice == 3:
        print(choose_human())
    elif choice == 4:
        show_children()
    elif choice == 5:
        exit()


if __name__ == "__main__":
    main()
