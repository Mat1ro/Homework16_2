import json


def add_info_to_user(class_name):
    with open('data/user.json', 'r', encoding='utf-8') as users:
        result = []
        users = json.load(users)
        for i in users:
            user = class_name(
                first_name=i["first_name"],
                last_name=i["last_name"],
                age=i['age'],
                email=i['email'],
                role=i['role'],
                phone=i['phone']
            )
            result.append(user)
    return result


def add_info_to_order(class_name):
    with open('data/orders.json', 'r', encoding='utf-8') as orders:
        result = []
        orders = json.load(orders)
        for i in orders:
            order = class_name(
                name=i["name"],
                description=i["description"],
                start_date=i['start_date'],
                end_date=i['end_date'],
                address=i['address'],
                price=i['price'],
                customer_id=i['customer_id'],
                executor_id=i['executor_id']
            )
            result.append(order)
    return result


def add_info_to_offer(class_name):
    with open('data/offers.json', 'r', encoding='utf-8') as offers:
        result = []
        offers = json.load(offers)
        for i in offers:
            offer = class_name(
                order_id=i["order_id"],
                executor_id=i["executor_id"]
            )
            result.append(offer)
    return result


def add_new_user(class_name, user):
    user = class_name(
        first_name=user["first_name"],
        last_name=user["last_name"],
        age=user['age'],
        email=user['email'],
        role=user['role'],
        phone=user['phone']
    )
    return user


def add_new_order(class_name, order):
    order = class_name(
        name=order["name"],
        description=order["description"],
        start_date=order['start_date'],
        end_date=order['end_date'],
        address=order['address'],
        price=order['price'],
        customer_id=order['customer_id'],
        executor_id=order['executor_id']
    )
    return order


def add_new_offer(class_name, offer):
    offer = class_name(
        order_id=offer["order_id"],
        executor_id=offer["executor_id"]
    )
    return offer
