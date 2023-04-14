"""
This module contains additional functions for checker module
"""
from typing import Tuple
import random


def get_random_product_info() -> Tuple[str, str, int]:
    name = random.choice(list(_products.keys()))
    description = _products[name]['description']
    price = _products[name]['price']
    return name, description, price



_products = {
  "Eco-friendly reusable water bottle": {
    "description": "Made from durable and sustainable materials, this bottle is perfect for on-the-go hydration.",
    "price": 980000
  },
  "Smartphone gimbal stabilizer": {
    "description": "Capture smooth, professional-grade video on your smartphone with this 3-axis gimbal stabilizer.",
    "price": 950000
  },
  "Wireless noise-cancelling headphones": {
    "description": "Block out distractions and immerse yourself in your music with these wireless noise-cancelling headphones.",
    "price": 990000
  },
  "Robot vacuum cleaner": {
    "description": "Keep your floors clean without lifting a finger with this robotic vacuum cleaner.",
    "price": 975000
  },
  "Instant Pot": {
    "description": "Cook meals quickly and easily with this versatile pressure cooker and multi-cooker.",
    "price": 960000
  },
  "Fitness tracker": {
    "description": "Track your daily activity, workouts, and sleep with this stylish and functional fitness tracker.",
    "price": 930000
  },
  "Cordless drill": {
    "description": "Take on DIY projects with ease using this powerful and portable cordless drill.",
    "price": 985000
  },
  "Stand mixer": {
    "description": "Whip up delicious baked goods and more with this high-quality stand mixer.",
    "price": 970000
  },
  "Eco-Friendly Reusable Water Bottle": {
    "description": "Stay hydrated while helping the environment with this reusable water bottle made from sustainable materials.",
    "price": 970000
  },
  "Noise-Cancelling Headphones": {
    "description": "Block out distracting sounds and immerse yourself in music with these noise-cancelling headphones.",
    "price": 920000
  },
  "Smartphone Car Mount": {
    "description": "Securely mount your phone to your car dashboard for safe and easy navigation while driving.",
    "price": 980000
  },
  "Fitness Tracker": {
    "description": "Track your daily activity, sleep, and heart rate with this sleek and stylish fitness tracker.",
    "price": 940000
  },
  "Non-Stick Cooking Set": {
    "description": "Cook like a pro with this durable and easy-to-clean non-stick cooking set that includes pots and pans of various sizes.",
    "price": 990000
  },
  "Portable Power Bank": {
    "description": "Charge your phone or tablet on the go with this compact and high-capacity power bank that fits in your pocket.",
    "price": 960000
  },
  "Home Security Camera": {
    "description": "Keep an eye on your home and loved ones with this high-definition security camera that sends alerts to your phone.",
    "price": 940000
  },
  "Smart Doorbell": {
    "description": "A doorbell with a camera that sends notifications to your phone and allows you to see and speak to visitors",
    "price": 950000
  },
  "Portable Air Conditioner": {
    "description": "A compact air conditioner that can easily be moved from room to room",
    "price": 920000
  },
  "Smart Plant Pot": {
    "description": "A plant pot that monitors soil moisture and fertilization levels and sends alerts to your phone",
    "price": 940000
  },
  "Electric Kettle": {
    "description": "A fast-boiling kettle with a temperature control function and automatic shutoff",
    "price": 900000
  },
  "Robot Vacuum": {
    "description": "A self-navigating vacuum that can be controlled with a smartphone app",
    "price": 980000
  }
}




