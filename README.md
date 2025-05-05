# Name of Thrones
It's like Game of Thrones but more focused on the Names of show's characters.

## Table of Contents

1. [**The Realm Unveiled** - *Description*](#the-realm-unveiled)  
   Discover the purpose and magic behind the app that tracks characters in Westeros.  

2. [**Feast of Features** - *Features*](#feast-of-features)  
   A banquet of functionalities to keep your GoT character chaos in check.  

3. [**Forge of Code** - *Tech Stack*](#forge-of-code)  
   Peek into the tools and technologies that power your app - crafted like Valyrian steel.  

4. [**Claim the Throne** - *Setup Instructions*](#claim-the-throne)  
   Step-by-step guidance to conquer the realm and set up your app like a true ruler.  

5. [**Rally the Bannermen** - *Instructions on How to Run the Server*](#rally-the-bannermen)  
   Assemble your forces and learn how to bring the app to life (server-side).  

6. [**Whispers in the Wind** - *Made Assumptions*](#whispers-in-the-wind)  
   A list of assumptions made while building the app - because even the Maesters can’t know everything.  

7. [**A Programmer’s Oath** - *Brief Description of Programmer's Approach*](#a-programmers-oath)  
   The thought process behind crafting an app worthy of the Iron Throne.  

8. [**The Scroll of Endpoints** - *List of All API Endpoints*](#the-scroll-of-endpoints)  
   A detailed map of routes to navigate the kingdom of data.  

9. **Defend the Realm** - *Testing*  
   - [9.1 **Clear Instructions on How to Run the Tests**](#clear-instructions-on-how-to-run-the-tests)  
        Arm yourself with knowledge to ensure the integrity of your app remains unbroken.  
   - [9.2 **The Trial of Tests** - *Test Results Interpretations*](#the-trial-of-tests)  
        Decipher the outcomes of testing battles and see who stands victorious.  
   - [9.3 **The Allies You’ll Need** - *Dependencies Needed for Testing*](#the-allies-youll-need)  
        A roster of key tools and frameworks that support your testing efforts.  
   - [9.4 **Command the Test Army** - *Sample Testing Commands for Running Tests*](#command-the-test-army)  
        Your battle-ready commands for unleashing the full power of the test suite.  


## The realm unveiled

Have you ever found yourself drowning in the sea of characters, houses, and alliances in Game of Thrones? Worry no more - we’ve got your back! Introducing Name of Thrones, the ultimate RESTful API for keeping track of all the power players in Westeros and beyond. Whether it’s the noble Stark wolf or the fiery Targaryen dragon, our app lets you organize, filter, and explore characters effortlessly.

Stay ahead of the chaos. With Name of Thrones, you’ll never lose track of who’s rising to power, who’s falling, and who’s wielding their strength to change the fate of the realm.

## Feast of Features

### Features fit for a king (or queen):

- *CRUD Operations:* Create, read, update, and delete characters with ease. Reading includes filtering, sorting, and pagination, so your data stays as organized as the Great Library of the Citadel.

- *Authentication & Authorization:* Rest assured, your app is guarded as fiercely as the Wall itself! Only authorized users may traverse the icy barrier and access POST, PUT, and DELETE endpoints - ensuring no White Walkers sneak past the authorization wall.

- *Character Attributes:* Track names, houses, animals, symbols, nicknames, roles, ages, deaths, and even their strength - because every detail matters in the game of thrones!

### A Tale of Two Storages

- *Ephemeral vs Eternal:* Choose your storage wisely! Will you live in the fleeting moment with JSON-based-in-memory storage (vanishing upon program shutdown, like a Read Priest's visions), or will you etch your data into PostgreSQL, ensuring persistence through every restart? Some things, like Valyrian steel and grudges, are meant to last forever - and the North remembers.

### Lords, Ladies, and The Office

- *User Management:* Every kingdom has its rules and subjects, and Name of Thrones is no different! CUD operations for users allow you to manage your cast of Office characters.

- *Regional Managers & Associates:* The hierarchy hierarchy is clear - Regional Managers (AKA Admins) wield power over all users, granting them the ability to read, modify, and delete any account. Others? Well, they can only manage their own profiles. After all, not everyone can be Michael Scott.

### When Two Worlds Collide

- *Dual Roles, Double the Fun:* In our realm, authenticated Office characters aren't just busy managing their own affairs. They step into the arena and wield their mighty CUD powers on Game of Thrones characters! Whether you're channeling your inner Michael Scott or thinking like Dwight Schrute, you'll create, update and delete Westerosi legentds with a single click. This dual functionality makes sure that every character - be it Scrontonian or a ruler of Westeros - gets the attention they deserve.

### A Do-Over Worthy of a Time Turner

- *Database Reset:* Sometimes, you just want to wipe the slate clean, send everything back to square one, and start fresh - whether it's avoiding a workplace scandal or undoing a battle blunder. The mighty "Reset Database" feature, available only to the exalted Regional Managers, restores the PostgreSQL database to its original state. Use it wisely, lest you invoke the wrath of your subjects.

### A Scroll of Convenience

- *Flasgger Documentation:* Why toil with cURL or Postman when you can interact with endpoints using a sleek GUI? With Flassger, your API is presented like a royal decree, making exploration and testing easier than ever - no ravens required.

## Forge of code

Peek behind the curtain to discover the enchanted ingredients that power the App - a mystical concoction forged from the rarest elements of modern coding. Each dependency was chosen like a secret spice in an alchemist's potion, lending its unique magic to our digital realm.

### The Anvil of Application

- *Flask (v3.1.0):* The nimble conjurer that forms the backbone of the App, channeling requests and responses with wizard-like speed.

- *Flask-SQLAlchemy (v3.1.1) & SQLAlchemy (v2.0.40):* This dynamic duo maps your kingdom's data with the precision of an enchanted quill recording ancient lore, making database interactions seamless and reliable.

- *Werkzeug (v3.1.3):* The trusted scribe that transforms raw data into captivating presentations, ensuring every detail is rendered with the elegance of a master storyteller.

### The Sword's Edge: API and Documentation

- *Flasgger (v0.9.7.1):* Experience the magic of interactive API exploration. With a sleek GUI, this tool lets you test endpoints as effortlessly as consulting an oracle - all without needing extra incantations like cURL or Postman.

### Defending the Wall

- *bcrypt (v4.3.0):* The Night's Watch of the App, standing resolute against the icy onslaught of unwanted intruders. No matter how many times they try to break through, this fortress holds strong.

- *isdangerous (v2.2.0) & PyJWT (v2.10.1):* As ancient runes and enchantments protect the realm from dark forces, these mystical guardians ensure that token-base authentication remains as impenetrable as the wards sealing off the lands from White Walker infiltration.

### Bridging to the World of Data

- *psycopg2-binary (v2.9.10):* Acting as the steadfast courier between the App and PostgreSQL, this tool ensures your data flows as reliably as a well-trained falcon on a mission.

### Deployment: Setting the Stage for Adventure

- *waitress (v3.0.2):* A production-grade server that stands at the vanguard, reliably serving the App to the world as if it were a mighty battalion on parade.

- *hupper (v.1.12.1):* The ever-watchful sentinel that detects code changes and breathes new life into the App, reminiscent of a messenger swiftly transmitting fresh orders across the realm.


## Claim the Throne

Follow these steps to conquer the realm and establish your app like a true sovereign:

1. Conquer the Repository

    **Clone the Repository:** Begin your conquest by cloning the code repository into your local keep. Replace the URL with your repository's sacred link:

    `git clone htts://github.com/e-kif/name_of_thrones`

2. Prepare Your Battleground

    **Create a Virtual Environment:** Forge an isolated realm for your app by creating a Python virtual environment:

    `python3 -m venv .venv`

    Activate the Virtual Environment:

    - On Unix/Linux: `source .venv/bin/activate`

    - On Windows: `.venv/Scripts/activate`

3. Arm Yourself with the Tools of the Trade

    **Install Dependencies:** Equip yourself with all the enchanted ingredients required by the application:

    `pip3 install -r requirements.txt`

    This command gathers every gem and artifact needed for your kingdom.

4. Draft Your Secret Scroll

    Create & Populate the *.env* File: At the root of your project, create a file named *.env* containing your realm's secret configurations:

    ```python
    DATABASE_URI='postgresql://username:password@host:port/db_name'
    SECRET_KEY='you-secret-key'
    PROTOCOL='http' # Use 'https for a fortified realm in production with SSL certificates
    ```
    Replace *username*, *password*, *host*, *port* and *db_name* with your actual database details. The *SECRET_KEY* should be a robust, mysterious string to secure your citizens against dark arts.

5. Prepare the Database Realm

   Set Up the SQL Database:

   Ensure PostgreSQL is installed and running in your domain.

   Create the database using your PostgreSQL client (for example):

   `CREATE DATABASE db_name;`

   Ensure the credentials in your *.env* file align with what you've set up. Gather your database's user, password and host details as these will be the keys to your treasure vault.

6. Additional Tips for a Ruling Master

   **Environment Virables:** Verify that your *.env* file is loaded correctly.

   Local vs. Production Protocols:

   For day-to-day rulership (local development), use `PROTOCOL='http'`.

   For deployment, fortify your realm with `'PROTOCOL=https'` and install valid SSL certificates to protect your subjects.


## Rally the Bannermen

Instructions on How to Run the Server

Assemble your forces and let your digital kingdom come alive! Whether you're staging a local skirmish or launching a full-scale siege, these instructions will mobilize your server like a fleet marching to conquer new territories. Remember, *'When you play the game of Throes, you win or you die'* - so ensure your deployment strategy is as formidable as a well-planned conquest.

### For Local Development

#### Prepare Your War Room

Ensure your virtual environment is activated:
- Unix/Linux: `source .venv/bin/activate`
- Windows: `.venv\Scripts\activate`

#### Command the Development Forces

Start your app with Flask's built-in server:
`python3 app.py`
This spins up your development sever, perfect for testing new strategies and making tactical adjustments in real time.

### For Production Deployment

#### Double-Check Your Battle Plans

Verify that your `.env` file is solid:
- *DATABASE_URI:* Correctly set to connect your PostgresSQL fortress.
- *SECRET_KEY:* A potent secret to safeguard your realm.
- *PROTOCOL:* Use `'https'` to secure your kingdom if you've equipped SSL certificates.

#### Deploy with Waitress

When it's time for the main siege, use *Waitress* to stand guard at your front lines:

`waitress-serve --port=80 --call 'app:production'`

Replace _80_ with your desired port. This production-grade server ensures that your application remains resilient and accessible to loyal subjects far and wide.

#### Optional: Hupper for Rapid Reinforcements

For those times when every change needs to echo immediately across the battlefield, launch your app using _Hupper:_

`hupper -m waitress-serve --port=80 --call 'app:production'`

This ensures your forces are constantly in sync with your latest commands.

With these commands, you're not merely running a server - you're unleashing an army of digital prowess. Your web domain is set to become a realm where every visitor experiences the might of your technological mastery.

## Whispers in the Wind

The unseen forces guiding the realm. This section outlines the silent rules shaping the foundation of the system - assumptions that ensure stability in the ever-shifting landscape of data and logic. Like the _Faceless Men_, these truths are ever-present yet seldom noticed, subtly influencing the world from the shadows. Though unspoken, they dictate the order of  things, much like whispered intrigues in the halls of power.

### Assumptions:

1. **Required character fields** are _name_, _role_ and _strength_, as determined from the initial _characters.json_ file. These attributes are as fundamental as a sword to a knight - every character must possess them to stand firm in the story.

2. **Optional fields** are determined based on the presence of _null_ values in the _characters.json_ file. If an attribute is missing for any character, it is considered optional - much like the unpredictable fate of minor lords in Westeros. Some details may vanish into obscurity, but the realm endures.

3. **Immutable IDs:** The identities of both characters and users are set in stone - no mortal (or developer) shall alter them. Much like the names in the annals of history or the lineage of noble houses, IDs remain unchangeable, ensuring the integrity of the realm.

4.  **The Quill vs. The Rusted Blade.** In the realm of logic and precision, a good scribe wields the well-forged *age_less_than*, ensuring calculations stand true like Master-written records. However, lurking in the shadows, the not-so-gifted scribe wields the questionable *age_less_then* - a blade dulled by typos, ready to betray unsuspecting code warriors.

    Fear not, for this app accommodates both, though we advise keeping your scrolls error-free—lest the Citadel revoke your writing privileges!

5. **Default Sort Order:** If no specific sort order is declared alongside the sorting parameter, the system shall assume _sort_asc_ - much like how the realm follows tradition when no ruler steps forward to redefine the order of things. Order must prevail, lest chaos reign across the kingdom!

6. **Sorting Behavior:** When sorting is ascending order by an optional key, entries with _None_ values shall gracefully retreat to the end of the list - much like exiled lords and fallen houses, lingering on the edges of history.

7. **Interpreting Empty Filter Values:** An empty string withing a filter value is taken as a signal that the key is _None_ - much like how a name whispered into the void fades into obscurity. Some truths are left unspoken, but their absence speaks volumes.

## A Programmer’s Oath

### Code, Honor, and Innovation

In the pursuit of clean, efficient, and battle-hardened code, I vow to wield logic with precision, embrace creativity without compromise, and fortify every function against chaos. Whether forging new features or refining old foundations, I uphold the sacred balance between readability, performance, and maintainability - because in the realm of programming, greatness is built one line at a time.

- **Architectural Overview:** The architecture follows a modular design, ensuring separation of concerns for maintainability and scalability.
```python
    ├── data  # database management
    ├── models  # SQLAlchemy mapping definitions
    ├── routers  # Flask blueprints
    ├── storage  # storage files containing characters and users information
    ├── test  # Pytest tests
    └── utils  # app settings, security functions, swagger documentation template
```
- **Data Retrieval:** Original data is stored as a list of dictionaries. To keep id-based lookups efficient without converting it into a dictionary each time, the list is sorted on startup and binary search is used.
- **OOP Flexibility:** Two classes - JSONDataManager and SQLDataManager - are implemented to allow seamless switching between an in-memory JSON data source and a PostgreSQL database.
- **Database Reset:** The *_reset_database* method in SQLDataManager reinitializes the PostgreSQL database with default data (50 characters and 4 users), useful for initial setup or returning to a pristine state.
- **Filtering Attention:** Characters filtering key *age_less_then* was treated as an attentiveness test: both filter keys (*age_less_then* and *age_less_than*) were implemented.
- **Field Classification:** Character attributes are devided into required fields (*name*, *role*, *strength*) and optional fields (*age*, *animal*, *death*, *house*, *nickname*, *symbol*).
- **Data Normalization:** The characters table stores only the *id* and required fields. Optional fields are handled as hybrid properties, resulting in a cleaner database and simpler SQLAlchemy queries for retrieving, setting, filtering and sorting.
- **Sorting Flexibility:** Sorting supports both long (e.g., *sort_asc/sort_des*) and short (*asc/desc*) order parameters, defaulting to ascending when no order is provided.
- **Database Toggle:** The *use_sql_database* boolean variable switches the app's backend between an in-memory JSON list and a PostgreSQL database.
- **TDD & Testing:** A *skip_test* dictionary is available to skip specific test categories for faster debugging after refactoring or introducing new changes.


## The Scroll of Endpoints

Coming soon...


## Defend the Realm

### Clear Instructions on How to Run the Tests

Coming soon...


### The Trial of Tests

Coming soon...

### The Allies You’ll Need

Coming soon...


### Command the Test Army

Coming soon...
