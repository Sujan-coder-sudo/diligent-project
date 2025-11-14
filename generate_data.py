import csv
import random
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker
fake = Faker()

# Set random seed for reproducibility
random.seed(42)
Faker.seed(42)

# Generate users
def generate_users(n=150):
    users = []
    for i in range(1, n + 1):
        join_date = fake.date_between(start_date='-2y', end_date='today')
        users.append({
            'user_id': i,
            'name': fake.name(),
            'email': fake.email(),
            'join_date': join_date.strftime('%Y-%m-%d')
        })
    return users

# Generate products
def generate_products(n=100):
    categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports', 'Beauty']
    products = []
    
    # Predefined product names by category
    product_names = {
        'Electronics': ['Smartphone', 'Laptop', 'Headphones', 'Smart Watch', 'Tablet', 'Camera', 'Speaker', 'Monitor'],
        'Clothing': ['T-Shirt', 'Jeans', 'Dress', 'Jacket', 'Sneakers', 'Hat', 'Socks', 'Sweater'],
        'Books': ['Novel', 'Textbook', 'Cookbook', 'Biography', 'Mystery', 'Science Fiction', 'Fantasy', 'Self-Help'],
        'Home': ['Lamp', 'Desk', 'Chair', 'Bedding', 'Cookware', 'Utensils', 'Decor', 'Storage'],
        'Sports': ['Yoga Mat', 'Dumbbells', 'Running Shoes', 'Basketball', 'Tennis Racket', 'Bicycle', 'Treadmill', 'Swim Goggles'],
        'Beauty': ['Shampoo', 'Moisturizer', 'Lipstick', 'Perfume', 'Face Mask', 'Sunscreen', 'Mascara', 'Foundation']
    }
    
    product_id = 1
    for category in categories:
        for name in product_names[category]:
            for i in range(1, 4):  # 3 variants per product
                products.append({
                    'product_id': product_id,
                    'name': f"{name} {i}",
                    'category': category,
                    'price': round(random.uniform(10, 500), 2)
                })
                product_id += 1
                if product_id > n:
                    return products
    return products

def generate_orders(users, n=200):
    orders = []
    order_id = 1
    
    for _ in range(n):
        user = random.choice(users)
        order_date = fake.date_between(
            start_date=datetime.strptime(user['join_date'], '%Y-%m-%d'),
            end_date='today'
        )
        
        # Generate a random number of orders per user (1-5)
        num_orders = random.choices([1, 2, 3, 4, 5], weights=[0.4, 0.3, 0.15, 0.1, 0.05])[0]
        
        for _ in range(num_orders):
            if order_id > n:
                return orders
                
            # Generate order date (after join date and before today)
            days_since_join = (datetime.now().date() - 
                             datetime.strptime(user['join_date'], '%Y-%m-%d').date()).days
            days_after_join = random.randint(0, days_since_join)
            order_date = (datetime.strptime(user['join_date'], '%Y-%m-%d') + 
                         timedelta(days=days_after_join)).date()
            
            orders.append({
                'order_id': order_id,
                'user_id': user['user_id'],
                'order_date': order_date.strftime('%Y-%m-%d'),
                'total_amount': 0  # Will be updated when order items are generated
            })
            order_id += 1
    
    return orders

def generate_order_items(orders, products, n=400):
    order_items = []
    order_item_id = 1
    
    # Group orders by user
    orders_by_user = {}
    for order in orders:
        if order['user_id'] not in orders_by_user:
            orders_by_user[order['user_id']] = []
        orders_by_user[order['user_id']].append(order)
    
    # Generate order items
    for user_orders in orders_by_user.values():
        for order in user_orders:
            # 1-5 items per order
            num_items = random.choices([1, 2, 3, 4, 5], weights=[0.1, 0.3, 0.3, 0.2, 0.1])[0]
            
            # Select random products
            selected_products = random.sample(products, min(len(products), num_items))
            
            total_amount = 0
            for product in selected_products:
                quantity = random.randint(1, 3)
                order_items.append({
                    'order_item_id': order_item_id,
                    'order_id': order['order_id'],
                    'product_id': product['product_id'],
                    'quantity': quantity
                })
                total_amount += product['price'] * quantity
                order_item_id += 1
            
            # Update order total
            order['total_amount'] = round(total_amount, 2)
    
    return order_items

def generate_reviews(users, products, order_items, n=150):
    reviews = []
    review_id = 1
    
    # Get all products that were ordered
    ordered_products = set(item['product_id'] for item in order_items)
    
    for user in users:
        # 20% chance to leave a review for each ordered product
        if random.random() < 0.2:
            # Select random products to review (1-5 per user)
            num_reviews = random.randint(1, 5)
            user_products = random.sample(list(ordered_products), min(num_reviews, len(ordered_products)))
            
            for product_id in user_products:
                reviews.append({
                    'review_id': review_id,
                    'user_id': user['user_id'],
                    'product_id': product_id,
                    'rating': random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.1, 0.2, 0.3, 0.35])[0],
                    'review_text': fake.paragraph(nb_sentences=random.randint(1, 3))
                })
                review_id += 1
                if review_id > n:
                    return reviews
    
    return reviews

def save_to_csv(data, filename, fieldnames):
    with open(f'data/{filename}', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def main():
    print("Generating users...")
    users = generate_users(150)
    
    print("Generating products...")
    products = generate_products(100)
    
    print("Generating orders...")
    orders = generate_orders(users, 200)
    
    print("Generating order items...")
    order_items = generate_order_items(orders, products, 400)
    
    print("Generating reviews...")
    reviews = generate_reviews(users, products, order_items, 150)
    
    # Save to CSV files
    print("Saving to CSV files...")
    save_to_csv(users, 'users.csv', ['user_id', 'name', 'email', 'join_date'])
    save_to_csv(products, 'products.csv', ['product_id', 'name', 'category', 'price'])
    save_to_csv(orders, 'orders.csv', ['order_id', 'user_id', 'order_date', 'total_amount'])
    save_to_csv(order_items, 'order_items.csv', ['order_item_id', 'order_id', 'product_id', 'quantity'])
    save_to_csv(reviews, 'reviews.csv', ['review_id', 'user_id', 'product_id', 'rating', 'review_text'])
    
    print("Data generation complete!")

if __name__ == "__main__":
    main()
