import aiohttp  # Eşzamansız HTTP istekleri için bir kütüphane
import random
from datetime import datetime, timedelta

class Pokemon:
    pokemons = {}
    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.power = random.randint(30, 60)
        self.hp = random.randint(200, 400)
        self.last_feed_time = datetime.now()
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için eşzamansız bir yöntem
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  # İstek için URL API'si
        async with aiohttp.ClientSession() as session:  # Bir HTTP oturumu açma
            async with session.get(url) as response:  # GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması ve kodunun çözülmesi
                    return data['forms'][0]['name']  # Bir Pokémon'un adını döndürme
                else:
                    return "Pikachu"  # İstek başarısız olursa varsayılan adı döndürür
    async def info(self):
        # Pokémon hakkında bilgi döndüren bir metot
        if not self.name:
            self.name = await self.get_name()  # Henüz yüklenmemişse bir adın geri alınması
        return f"""Pokémon'un ismi: {self.name} Pokémon'un gücü: {self.power} Pokémon'un sağlığı: {self.hp}"""

    async def show_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    img_url = data['sprites']['front_default']
                    return img_url
                else:
                    return None
                

    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = random.randint(1, 5)
            if chance == 1:
                return "Sihirbaz Pokémon, savaşta bir kalkan kullandı!"         
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pokémon eğitmeni @{self.pokemon_trainer}, @{enemy.pokemon_trainer}'ne saldırdı\n@{enemy.pokemon_trainer}'nin sağlık durumu şimdi {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer}, @{enemy.pokemon_trainer}'ni yendi!"
        

    async def feed(self, feed_interval=20, hp_increase=10):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Pokémon'un sağlığı geri yüklenir. Mevcut sağlık: {self.hp}"
        else:
            return f"Pokémonunuzu şu zaman besleyebilirsiniz: {current_time+delta_time}"  
                

class Wizard(Pokemon):
    def feed(self):
        return super().feed(hp_increase=20)

class Fighter(Pokemon):
     async def attack(self, enemy):
        super_power = random.randint(5, 15)
        self.power += super_power
        result = await super().attack(enemy)
        self.power -= super_power
        return result + f"\nDovuscu Pokémon süper saldırı kullandı. Eklenen guc: {super_power}"
     
     def feed(self):
        return super().feed(feed_interval=10)
     


import asyncio

async def main():
    wizard = Wizard("username1")
    fighter = Fighter("username2")

    # Pokémon bilgilerini göster
    wizard_info = await wizard.info()
    fighter_info = await fighter.info()
    print(wizard_info)
    print("#" * 10)
    print(fighter_info)
    print("#" * 10)

    # Saldırı senaryosu
    attack_result1 = await wizard.attack(fighter)
    attack_result2 = await fighter.attack(wizard)

    print(attack_result1)
    print(attack_result2)

# asyncio döngüsü ile çalıştır
asyncio.run(main())
