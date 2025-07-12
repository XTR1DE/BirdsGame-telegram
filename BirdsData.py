class Bird:
    def __init__(self, name, productivity, price, url_buy: str):
        self.name = name
        self.productivity = productivity
        self.price = price
        self.url = url_buy
        self.eggs = 0

    def update(self):
        return self.productivity / 60


Birdtypes = {
    "green": Bird('green', 100, 1, "https://google.com"),
    "yellow": Bird('yellow', 500, 5, "https://google.com"),
    "brown": Bird('brown', 1000, 10, "https://google.com"),
    "blue": Bird('blue', 10000, 100, "https://google.com")
}