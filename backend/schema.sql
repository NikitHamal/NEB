-- Schema for NEBians D1 Database

DROP TABLE IF EXISTS reply_likes;
DROP TABLE IF EXISTS post_likes;
DROP TABLE IF EXISTS replies;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS resources;
DROP TABLE IF EXISTS fcm_tokens;
DROP TABLE IF EXISTS users;

-- 1. Users Table
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT,
    photo_url TEXT,
    display_name TEXT,
    dob TEXT NOT NULL,
    gender TEXT,
    class TEXT,
    subjects TEXT, -- Comma-separated list of subjects
    pradesh TEXT,
    district TEXT,
    school TEXT,
    is_locked INTEGER DEFAULT 0, -- 0 = Unlocked/Public, 1 = Locked/Private
    created_at INTEGER NOT NULL
);

-- 2. Resources Table
CREATE TABLE resources (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    subject TEXT NOT NULL,
    grade_level TEXT NOT NULL,
    type TEXT NOT NULL,
    file_url TEXT NOT NULL,
    thumbnail_url TEXT,
    file_size INTEGER DEFAULT 0,
    added_at INTEGER NOT NULL,
    view_count INTEGER DEFAULT 0
);

-- 3. Posts Table
CREATE TABLE posts (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category TEXT NOT NULL,
    thumbs_up_count INTEGER DEFAULT 0,
    reply_count INTEGER DEFAULT 0,
    created_at INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 4. Post Likes Table (to prevent double liking)
CREATE TABLE post_likes (
    post_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    PRIMARY KEY (post_id, user_id),
    FOREIGN KEY(post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 5. Replies Table
CREATE TABLE replies (
    id TEXT PRIMARY KEY,
    post_id TEXT NOT NULL,
    parent_reply_id TEXT, -- Nullable for top level replies
    user_id TEXT NOT NULL,
    content TEXT NOT NULL,
    thumbs_up_count INTEGER DEFAULT 0,
    created_at INTEGER NOT NULL,
    FOREIGN KEY(post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 6. Reply Likes Table
CREATE TABLE reply_likes (
    reply_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    PRIMARY KEY (reply_id, user_id),
    FOREIGN KEY(reply_id) REFERENCES replies(id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 7. FCM Tokens Table
CREATE TABLE fcm_tokens (
    token TEXT PRIMARY KEY,
    user_id TEXT, -- Nullable for guests
    created_at INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Seed Initial Study Resources
INSERT INTO resources (id, title, description, subject, grade_level, type, file_url, thumbnail_url, file_size, added_at, view_count) VALUES
('res_phy_11_01', 'NEB Physics Class 11 Textbook', 'Official NEB curriculum textbook for Physics Class 11 covering Mechanics, Heat, and Waves.', 'Physics', 'Grade 11', 'Textbook', 'https://resources.nebians.com/physics/class11/textbook.pdf', '', 15400000, 1716900000000, 0),
('res_phy_11_02', 'Physics Notes - Mechanics & Kinematics', 'Comprehensive handwritten notes covering Newtons Laws, projectile motion, and circular motion for Class 11.', 'Physics', 'Grade 11', 'Notes', 'https://resources.nebians.com/physics/class11/mechanics_notes.pdf', '', 4200000, 1716900000000, 0),
('res_phy_12_01', 'NEB Physics Class 12 Textbook', 'Official NEB curriculum textbook for Physics Class 12 covering Electricity, Magnetism, and Modern Physics.', 'Physics', 'Grade 12', 'Textbook', 'https://resources.nebians.com/physics/class12/textbook.pdf', '', 18200000, 1716900000000, 0),
('res_phy_12_02', 'Physics Past Paper 2080 BS', 'NEB board examination paper for Physics from 2080 BS with marking scheme.', 'Physics', 'Grade 12', 'Past Papers', 'https://resources.nebians.com/physics/class12/past_paper_2080.pdf', '', 2100000, 1716900000000, 0),
('res_chem_11_01', 'NEB Chemistry Class 11 Textbook', 'Official NEB curriculum textbook for Chemistry Class 11 covering General and Physical Chemistry.', 'Chemistry', 'Grade 11', 'Textbook', 'https://resources.nebians.com/chemistry/class11/textbook.pdf', '', 14800000, 1716900000000, 0),
('res_chem_11_02', 'Chemistry Notes - Atomic Structure & Periodic Table', 'Detailed notes on atomic models, electronic configuration, and periodic properties.', 'Chemistry', 'Grade 11', 'Notes', 'https://resources.nebians.com/chemistry/class11/atomic_structure_notes.pdf', '', 3500000, 1716900000000, 0),
('res_chem_12_01', 'Chemistry Notes - Organic Chemistry', 'Complete notes on organic chemistry including hydrocarbons, alcohols, aldehydes, ketones, and carboxylic acids.', 'Chemistry', 'Grade 12', 'Notes', 'https://resources.nebians.com/chemistry/class12/organic_notes.pdf', '', 5600000, 1716900000000, 0),
('res_chem_12_02', 'Chemistry Past Paper 2080 BS', 'NEB board examination paper for Chemistry from 2080 BS with solution guide.', 'Chemistry', 'Grade 12', 'Past Papers', 'https://resources.nebians.com/chemistry/class12/past_paper_2080.pdf', '', 1800000, 1716900000000, 0),
('res_math_11_01', 'NEB Mathematics Class 11 Textbook', 'Official NEB curriculum textbook for Mathematics Class 11 covering Algebra, Trigonometry, and Coordinate Geometry.', 'Mathematics', 'Grade 11', 'Textbook', 'https://resources.nebians.com/math/class11/textbook.pdf', '', 12500000, 1716900000000, 0),
('res_math_11_02', 'Mathematics Notes - Trigonometry', 'Step-by-step solutions and notes for trigonometric identities, equations, and inverse functions.', 'Mathematics', 'Grade 11', 'Notes', 'https://resources.nebians.com/math/class11/trigonometry_notes.pdf', '', 3800000, 1716900000000, 0),
('res_math_12_01', 'NEB Mathematics Class 12 Textbook', 'Official NEB curriculum textbook for Mathematics Class 12 covering Calculus, Vectors, and Statistics.', 'Mathematics', 'Grade 12', 'Textbook', 'https://resources.nebians.com/math/class12/textbook.pdf', '', 13700000, 1716900000000, 0),
('res_math_12_02', 'Mathematics Past Paper 2080 BS', 'NEB board examination paper for Mathematics from 2080 BS with detailed solutions.', 'Mathematics', 'Grade 12', 'Past Papers', 'https://resources.nebians.com/math/class12/past_paper_2080.pdf', '', 2400000, 1716900000000, 0),
('res_bio_11_01', 'NEB Biology Class 11 Textbook', 'Official NEB curriculum textbook for Biology Class 11 covering Botany and Zoology.', 'Biology', 'Grade 11', 'Textbook', 'https://resources.nebians.com/biology/class11/textbook.pdf', '', 16300000, 1716900000000, 0),
('res_bio_11_02', 'Biology Notes - Cell Biology & Biomolecules', 'Comprehensive notes covering cell structure, cell division, enzymes, and biomolecules.', 'Biology', 'Grade 11', 'Notes', 'https://resources.nebians.com/biology/class11/cell_biology_notes.pdf', '', 4100000, 1716900000000, 0),
('res_eng_12_01', 'NEB English Class 12 Textbook - Meanings into Words', 'Official NEB English textbook for Class 12 with all prose, poetry, and drama sections.', 'English', 'Grade 12', 'Textbook', 'https://resources.nebians.com/english/class12/textbook.pdf', '', 8900000, 1716900000000, 0),
('res_eng_12_02', 'English Past Paper 2080 BS', 'NEB board examination paper for Compulsory English from 2080 BS.', 'English', 'Grade 12', 'Past Papers', 'https://resources.nebians.com/english/class12/past_paper_2080.pdf', '', 1500000, 1716900000000, 0),
('res_cs_11_01', 'NEB Computer Science Class 11 Textbook', 'Official NEB curriculum textbook for Computer Science Class 11 covering fundamentals, C programming, and web technology.', 'Computer Science', 'Grade 11', 'Textbook', 'https://resources.nebians.com/cs/class11/textbook.pdf', '', 10200000, 1716900000000, 0),
('res_cs_11_02', 'Computer Science Notes - C Programming', 'Complete notes on C programming language including arrays, functions, structures, pointers, and file handling.', 'Computer Science', 'Grade 11', 'Notes', 'https://resources.nebians.com/cs/class11/c_programming_notes.pdf', '', 3200000, 1716900000000, 0),
('res_cs_12_01', 'Computer Science Past Paper 2080 BS', 'NEB board examination paper for Computer Science from 2080 BS with model answers.', 'Computer Science', 'Grade 12', 'Past Papers', 'https://resources.nebians.com/cs/class12/past_paper_2080.pdf', '', 1900000, 1716900000000, 0);
