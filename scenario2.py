from typing import Tuple, Optional, Dict

from data_reader import routes_gen, numbers_gen

def get_price(number: str) -> Tuple[str, Optional[float]]:
    routes: Dict[str, float] = dict(routes_gen('35000'))
    price: Optional[float] = None
    prefix = number

    print("Dictionary generated!")

    while prefix != "+":
        try:
            price = routes[prefix]
            print(price)
            break
        except KeyError:
            prefix = prefix[:-1]
            print(prefix)

    return (number, price)

if __name__ == '__main__':
    price = get_price("+33676811907")
    print(price)
    assert price[1] == 0.39
