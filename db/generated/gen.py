from werkzeug.security import generate_password_hash
import csv, random
from faker import Faker

num_users = 100
num_games = 411
num_copies = 1000
num_collections = 500
num_libraries = 300
num_reviews = 2100
div_designers = 20
num_designers = 10

imgs = [
    "https://images.pexels.com/photos/247502/pexels-photo-247502.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
]

Faker.seed(0)
fake = Faker()

def get_csv_writer(f):
    return csv.writer(f, dialect='unix')

def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            about = fake.sentence()
            picture = random.choice(imgs)
            writer.writerow([uid, profile['name'], email, password, about, picture])
        print(f'{num_users} generated')
    return

def gen_gen(iterator, name):
    def temp(num, times=1):
        with open(f"{name}.csv", 'w') as f:
            writer = get_csv_writer(f)
            print(f"{name}...", end=" ", flush=True)
            for id in range(num):
                for _ in range(times):
                    result = iterator(id)
                    if result:
                        writer.writerow(result)
            print(f"{num} generated")
    return temp


def gen_copy(id):
    conditions = ["new", "good condition", "kinda dingy"]
    return [id, random.choice(conditions)]

def gen_collection(id):
    frames =[
        "The {place} Collection",
        "My Collection of all the {place} Games",
        "{place}",
        "The Ultimate {place}"
    ]
    title_word = fake.word()
    title = random.choice(frames).format(place=title_word)
    desc = fake.sentence()
    return [id, title, desc]

def gen_library(id):
    title = fake.first_name() + "'s Library"
    desc = f"Games for my {fake.word} club"
    return [id, title, desc]

def gen_copyOf(cpid):
    return [cpid, random.randrange(num_games)]

def gen_designedBy(gid):
    return [random.randrange(num_designers), gid]

def gen_reviewOf(id):
    uid = random.randrange(num_users)
    gid = random.randrange(num_games)
    rating = random.randrange(1,6)
    desc = fake.sentence(55)
    time = fake.date_time()
    return [uid, gid, rating, desc, time]

def gen_hasGame(cid):
    return [cid, random.randrange(num_games)]

def gen_hasCopy(cpid):
    return [random.randrange(num_libraries), cpid]

def gen_createdBy(cid):
    return [cid, random.randrange(num_users) ]

def gen_owns(lid):
    return [random.randrange(num_users), lid]

def gen_likesGame(uid):
    return [random.randrange(num_games), uid]

def gen_likesCollection(uid):
    return [random.randrange(num_collections), uid]

def gen_checkedOutBy(cpid):
    coin = [0,1]
    if random.choice(coin) == 1:
        return None
    return [cpid, random.randrange(num_users)]

def gen_playCount(uid):
    return [random.randrange(num_games), uid, random.randrange(50)]

gen_users(num_users)
gen_gen(gen_copy, "Copies")(num_copies)
gen_gen(gen_collection, "Collections")(num_collections)
gen_gen(gen_library, "Libraries")(num_libraries)
gen_gen(gen_copyOf, "CopyOf")(num_copies)
gen_gen(gen_designedBy, "DesignedBy")(num_games)
gen_gen(gen_reviewOf, "Reviews")(num_reviews)
gen_gen(gen_hasGame, "HasGame")(num_collections, times=10)
gen_gen(gen_hasCopy, "HasCopy")(num_copies)
gen_gen(gen_createdBy, "CreatedBy")(num_collections)
gen_gen(gen_owns, "Owns")(num_libraries)
gen_gen(gen_likesGame, "LikesGame")(num_users, times=16)
gen_gen(gen_likesCollection, "LikesCollection")(num_users, times=16)
gen_gen(gen_checkedOutBy, "CheckedOutBy")(num_copies)
gen_gen(gen_playCount, "PlayCount")(num_users)




