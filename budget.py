def tester(f, *args):
    print("tester:", f)
    return f

class Category:
    def __init__(self, category: str) -> None:
        self.__name: str = category
        self.__totalAmount: int | float = 0
        self.__ledger: list = []

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def ledger(self) -> list:
        return self.__ledger
    
    # methods
    def deposit(self, amount: int | float, description: str = "") -> None:
        self.__totalAmount += amount
        self.__ledger.append({
            "amount": amount,
            "description": description
        })

    def withdraw(self, amount: int | float, description: str = "") -> bool:
        re = False
        if self.check_funds(amount):
            re = True
            self.__totalAmount -= amount
            self.__ledger.append({
            "amount": -amount,
            "description": description
        })
        
        return re
            
    def get_balance(self) -> int | float:
        return sum([e["amount"] for e in self.__ledger])
    
    def transfer(self, amount: int | float, category: object) -> bool:
        re = False

        if self.withdraw(amount, f"Transfer to {category.name}"):
            re = True
            category.deposit(amount, f"Transfer from {self.name}")

        return re
    
    def check_funds(self, amount: int | float) -> bool:
        return amount <= self.get_balance()
    
    def __str__(self) -> str:
        string = f"""{(_is:=f"{'*'*int(15-len(self.name)/2)}{self.name}")}{'*'*(30-len(_is))}"""

        for record in self.__ledger:
            string += f"""\n{f"{d}{' '*(23-len(d))}" if len(d:=record["description"]) <= 23 else (d:=d[:23])}{' '*(7-len(a:=str(format(record["amount"],".2f"))))}{a}"""

        string += f"\nTotal: {self.get_balance()}"

        return string


def create_spend_chart(categories: list[Category]):
    totalSpent = round(sum(cbs:=[sum([(abs(a) if (a:=r["amount"]) < 0 else 0) for r in  categorie.ledger]) for categorie in categories]), 2)
    addIterations = max(len(categorie.name) for categorie in categories)
    spentPercentages = list(map(lambda amount: int((((amount / totalSpent) * 10) // 1) * 10), cbs))

    string = "Percentage spent by category\n"
    for i in range(12+addIterations):
        if i <= 10:
            string += f"""{str(y:=100-i*10).rjust(3)}| {"".join([('o  ' if (percent >= y) else '   ') for percent in spentPercentages])}\n"""
        elif i == 11:
            string += f"    -{''.join('---' for _ in range(len(categories)))}"
        else:
            string += f"""\n     {"".join((f"{name[i-12] if len(name:=categorie.name) > (i-12) else ' '}  ") for categorie in categories)}"""


    return string
