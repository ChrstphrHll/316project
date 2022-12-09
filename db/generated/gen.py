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
    "https://cdn.thisiswhyimbroke.com/images/top-hats-for-small-pets-pamperedbeardies-640x533.jpg",
    "https://static.boredpanda.com/blog/wp-content/uploads/2015/11/cute-snakes-wear-hats-106__700.jpg",
    "https://static.boredpanda.com/blog/wp-content/uploads/2015/11/cute-snakes-wear-hats-101__700.jpg",
    "https://metro.co.uk/wp-content/uploads/2014/07/ad_141155444.jpg?quality=90&strip=all",
    "https://i.etsystatic.com/9011195/c/1138/905/53/184/il/b3352e/2882492848/il_500x500.2882492848_10j7.jpg",
    "https://i.imgur.com/0JwHWJy.jpg",
    "https://i.imgur.com/MWPE8l3.jpeg",
    "https://i.chzbgr.com/full/9563699200/hA5030140/hat",
    "https://cdn11.bigcommerce.com/s-hzrdyz5h6m/images/stencil/2048x2048/products/145/518/Mad-Hatter-Mardi-Gras-hat-f__95469.1491956771.jpg?c=2",
    "https://ae01.alicdn.com/kf/S82dd04b8354e4d538eb5b1a2f92724efa/Small-Animals-Hats-Rabbit-Guinea-Pig-Hamster-Totoro-Hedgehog-Hat-And-Bow-Tie-Top-Hat-Pet.jpg",
    "https://st3.depositphotos.com/2800301/15669/i/450/depositphotos_156699968-stock-photo-brown-bear-russian-bear-wearing.jpg",
    "https://render.fineartamerica.com/images/images-profile-flow/400/images/artworkimages/mediumlarge/3/edwardian-gentleman-fox-michael-thomas.jpg",
    "https://i.etsystatic.com/5218985/c/2153/1711/0/386/il/4bc26a/2843345880/il_570xN.2843345880_933c.jpg",
    "https://img.freepik.com/premium-photo/chocolate-brown-newfoundland-wearing-top-hat_493961-1703.jpg",
    "https://thumbs.dreamstime.com/b/grizzly-bear-big-wild-bear-wearing-cylinder-top-hat-vintage-style-drawing-animal-94276749.jpg",
    "https://64.media.tumblr.com/fa9abe22433efda162f12b7191c1b8ad/89ff66914978230a-ed/s400x600/909415a7eb350782ddbcfd831f4b53ddfbbe02ff.jpg",
    "https://1.bp.blogspot.com/-S18BtoPojgY/YStGru4ieCI/AAAAAAABeXI/98hL291YN40WZVRcuRK_R3y1DM8rkCxIACLcBGAsYHQ/s16000/Time%2BFound%2BTails1.jpg",
    "https://img1.goodfon.com/wallpaper/nbig/a/2e/kot-koshka-pan-kot-uchenyy.jpg",
    "https://images.fineartamerica.com/images-medium-5/cute-dog-in-an-unusual-hat--vector-vitaly-grin.jpg",
    "https://i.pinimg.com/originals/5d/2f/7e/5d2f7e9e7148efbce1ddc0c512cab312.jpg",
    "https://i.etsystatic.com/9981514/r/il/655f00/1824248823/il_570xN.1824248823_ol7t.jpg",
    "https://media-exp1.licdn.com/dms/image/C4D03AQFecN8e0B8GTQ/profile-displayphoto-shrink_800_800/0/1645489506188?e=2147483647&v=beta&t=fC3SXWcuOVNOhwXNbSqJ87inFn-LWqeQt28jGLJ2Xw4",
    "https://s7d2.scene7.com/is/image/TWCNews/0916_alligator_wildlifecenterwebsite_09162022",
    "https://mir-s3-cdn-cf.behance.net/project_modules/max_1200/f6a4e742328863.57ca56f081e5e.jpg",
    "https://64.media.tumblr.com/f97a02c170570472316ccc063ed96353/d7c6ab2412c90be0-0e/s540x810/16c02bec88f87e86805340f70bf3dfadbdf825b7.jpg",
    "https://thumbs.dreamstime.com/b/wild-bear-portrait-animal-head-grizzly-bowler-hat-215607557.jpg",
    "https://amorphia-apparel.com/storage/images/sir-tardigrade/sir-tardigrade.1300x700.png?63d82fc46612ddd8001eae2947e6f9f0",
    
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
    desc = f"Games for my {fake.word()} club"
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




