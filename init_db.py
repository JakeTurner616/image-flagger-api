import sqlite3

# Connect to the database
conn = sqlite3.connect('flags.db')

# Create the table if it does not exist
conn.execute('''
    CREATE TABLE IF NOT EXISTS flagged_images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_prompt TEXT,
        steps TEXT,
        sampler TEXT,
        cfg_scale TEXT,
        seed TEXT,
        size TEXT,
        model_hash TEXT,
        model_name TEXT,
        seed_resize_from TEXT,
        denoising_strength TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Close the connection
conn.close()
