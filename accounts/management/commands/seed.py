import random
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from rest_framework.authtoken.models import Token

from accounts.models import AISetting, ShopSetting, TeamMember, UserProfile
from calls.models import Call
from challenges.models import Challenge, Entry
from customers.models import Customer
from fitcheck.models import FitCheck
from orders.models import Order
from products.models import Product


class Command(BaseCommand):
    help = "Clear and repopulate the database with ConfirmAI / TechZone demo data."

    def handle(self, *args, **options):
        random.seed(42)
        for model in (Entry, Challenge, FitCheck, Call, Order, Customer, Product, TeamMember, AISetting, ShopSetting):
            model.objects.all().delete()
        Token.objects.all().delete()
        User.objects.all().delete()

        seller = User.objects.create(username="karim@techzone.dz", email="karim@techzone.dz", first_name="Karim Boudiaf")
        seller.set_password("TechZone2026!")
        seller.save()
        UserProfile.objects.create(user=seller, role="seller", full_name="Karim Boudiaf")
        Token.objects.create(user=seller)

        customer = User.objects.create(username="yousef@gmail.com", email="yousef@gmail.com", first_name="Yousef")
        customer.set_password("Customer2026!")
        customer.save()
        UserProfile.objects.create(user=customer, role="customer", full_name="Yousef")
        Token.objects.create(user=customer)

        products = [
            dict(name="Wireless Earbuds Pro", category="Audio", price=6500, stock=120, low_stock_threshold=15,
                 sku="TZ-1001", sold_30d=64, verified_buyers=True,
                 description="Bluetooth 5.3 earbuds with noise reduction and a 24-hour charging case. One-year warranty.",
                 image_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=700&q=70"),
            dict(name="Smart Watch S2", category="Wearables", price=12900, stock=35, low_stock_threshold=10,
                 sku="TZ-1002", sold_30d=22, verified_buyers=True,
                 description="Heart-rate and sleep tracking, 7-day battery, water resistant. Works with Android and iPhone.",
                 image_url="https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=700&q=70"),
            dict(name="Power Bank 20000mAh", category="Accessories", price=3800, stock=8, low_stock_threshold=15,
                 sku="TZ-1003", sold_30d=41, verified_buyers=True,
                 description="20,000 mAh with dual USB-C fast charging. Charges a phone about four times.",
                 image_url="https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=700&q=70"),
            dict(name="Bluetooth Speaker", category="Audio", price=7800, stock=0, low_stock_threshold=10,
                 sku="TZ-1004", sold_30d=17, verified_buyers=True, follow=True,
                 expected_restock=date(2026, 10, 12),
                 supplier_note="Supplier confirmed a new shipment from Algiers port.",
                 description="Portable waterproof speaker with 12 hours of playtime.",
                 image_url="https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=700&q=70"),
            dict(name="Leather Phone Case", category="Accessories", price=900, stock=0, low_stock_threshold=20,
                 sku="TZ-1005", sold_30d=58, verified_buyers=False,
                 description="Slim leather case that fits the most common phone models.",
                 image_url="https://images.unsplash.com/photo-1601599560945-441296f1c0d5?w=700&q=70"),
            dict(name="Beige Cotton Hoodie", category="Clothing", price=3500, stock=14, low_stock_threshold=6,
                 sku="TZ-2001", sold_30d=11, verified_buyers=True, ai_added=True,
                 garment_chest_cm=102, garment_waist_cm=88,
                 description="Soft cotton hoodie, unisex, true to size. Scanned for AI fit check.",
                 image_url="https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=700&q=70"),
            dict(name="Running Sneakers", category="Footwear", price=8900, stock=6, low_stock_threshold=6,
                 sku="TZ-2002", sold_30d=9, verified_buyers=True, ai_added=True,
                 garment_chest_cm=0, garment_waist_cm=0,
                 description="Lightweight breathable running shoes with cushioned sole. Scanned for AI fit check.",
                 image_url="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=700&q=70"),
        ]
        for p in products:
            Product.objects.create(owner=seller, **p)

        names = [
            "Nadia Brahimi", "Omar Sahraoui", "Meriem Kaci", "Walid Merah",
            "Amine Khelifi", "Yasmine Bouzid", "Karim Haddad", "Lina Cherif",
            "Sofiane Amrani", "Ines Belkacem", "Rachid Medjahed", "Samira Zerrouki",
        ]
        cities = ["Algiers", "Oran", "Constantine", "Annaba", "Setif", "Blida"]
        customers = [Customer.objects.create(owner=seller, name=n, city=cities[i % len(cities)], phone=f"+213 6 6{i:02d} {i:02d}{i:02d} {i:02d}{i:02d}", address=f"{10 + i} Rue Didouche Mourad") for i, n in enumerate(names)]

        all_products = list(Product.objects.all())
        statuses = ["pending", "pending", "pending", "calling", "approval", "approval", "packing", "packing", "packing", "cancelled", "cancelled", "escalated", "escalated"]
        sources = ["Shopify", "WhatsApp", "Website"]
        orders = []
        for i, st in enumerate(statuses):
            p = all_products[i % len(all_products)]
            q = 1 + (i % 2)
            o = Order.objects.create(
                owner=seller,
                order_no=7744 - i,
                customer_name=names[i % len(names)],
                customer=customers[i % len(customers)],
                product=p,
                item_name=p.name,
                quantity=q,
                total_price=p.price * q,
                status=st,
                source=sources[i % 3],
                reviewed_by="Karim" if st == "packing" else "",
                release_note="Owner approval is on" if st == "approval" else "",
            )
            orders.append(o)

        call_statuses = (["success"] * 7) + (["unreachable"] * 3) + (["declined"] * 3) + (["escalated"] * 2)
        for i in range(15):
            st = call_statuses[i]
            o = orders[i % len(orders)]
            first = names[i % len(names)].split(" ")[0]
            if st == "unreachable":
                transcript = [{"speaker": "Sarah", "text": "No answer after 6 rings. Retry scheduled in 2 hours (attempt 1 of 2)."}]
                sentiment = None
                duration = 15
            elif st == "success":
                transcript = [
                    {"speaker": "Sarah", "text": f"Hello, is this {first}? This is Sarah from TechZone, calling about your order."},
                    {"speaker": first, "text": "Yes, speaking."},
                    {"speaker": "Sarah", "text": f"You ordered the {o.item_name} for {o.total_price} DZD, delivered to your address. Do you confirm?"},
                    {"speaker": first, "text": "Yes, I confirm. Is there a warranty?"},
                    {"speaker": "Sarah", "text": "One year. I've confirmed your order. Delivery is tomorrow."},
                    {"speaker": first, "text": "Perfect, thanks."},
                ]
                sentiment = round(0.3 + random.random() * 0.6, 2)
                duration = 60 + random.randint(0, 110)
            elif st == "declined":
                transcript = [
                    {"speaker": "Sarah", "text": f"Hello, is this {first}? This is Sarah from TechZone."},
                    {"speaker": first, "text": "No, I changed my mind."},
                    {"speaker": "Sarah", "text": "No problem, I've cancelled it. Have a good day."},
                ]
                sentiment = round(random.random() * 0.3 - 0.1, 2)
                duration = 60 + random.randint(0, 60)
            else:
                transcript = [
                    {"speaker": "Sarah", "text": f"Hello {first}, Sarah from TechZone."},
                    {"speaker": first, "text": "Can I talk to someone from the shop?"},
                    {"speaker": "Sarah", "text": "Of course. I'll pass you to the team."},
                ]
                sentiment = round(random.random() * 0.3 - 0.1, 2)
                duration = 60 + random.randint(0, 60)
            Call.objects.create(
                owner=seller,
                order=o, customer_name=o.customer_name, order_no=o.order_no,
                status=st, duration_sec=duration, sentiment=sentiment, transcript=transcript,
            )

        hoodie = Product.objects.get(sku="TZ-2001")
        sneakers = Product.objects.get(sku="TZ-2002")
        earbuds = Product.objects.get(sku="TZ-1001")
        ch1 = Challenge.objects.create(
            owner=seller, product=hoodie, status="open", entry_fee=50,
            description="Win the Beige Cotton Hoodie free. Choose your game, join, we play the match outside the shop.",
        )
        ch2 = Challenge.objects.create(
            owner=seller, product=sneakers, status="live", entry_fee=50,
            description="Win the Running Sneakers. Live challenge — join before it ends!",
        )
        for ch, players in ((ch1, ["Walid", "Ines"]), (ch2, ["Amine", "Lina", "Sofiane"])):
            for pl in players:
                Entry.objects.create(challenge=ch, player_name=pl, game="Penalty Kicks")

        FitCheck.objects.create(owner=seller, product=hoodie, score=88, verdict="Fits well — chest and waist are in the expected range for size M.")
        FitCheck.objects.create(owner=seller, product=sneakers, score=74, verdict="Slightly narrow. Consider half a size up for wide feet.")

        for name, role in [("Karim Boudiaf", "Owner"), ("Sara Mansouri", "Support"), ("Yacine Amrani", "Packing")]:
            TeamMember.objects.create(owner=seller, name=name, role=role)

        AISetting.objects.create(
            owner=seller, mode="owner", auto_call=True, call_from="09:00", call_until="20:00",
            retries=2, voice="Sarah (FR)",
            opening_line="Hello, this is Sarah from TechZone calling about your order.",
            shop_notes="Always confirm address and delivery time before approving.",
            release_limit=10000,
        )
        ShopSetting.objects.create(owner=seller, shop_name="TechZone", currency="DZD", phone="+213 555 010 203")

        self.stdout.write(self.style.SUCCESS("Seed complete."))
