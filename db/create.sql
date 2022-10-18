-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.
CREATE TABLE Games (
    gid INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR NOT NULL,
    description TEXT NOT NULL,
    image_url VARCHAR NOT NULL,
    complexity INT NOT NULL,
    length INT NOT NULL,
    min_players INT NOT NULL,
    max_players INT NOT NULL
);

CREATE TABLE Users (
    uid INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    passowrd VARCHAR NOT NULL,
    about TEXT,
    image_url VARCHAR
);

CREATE TABLE Copies (
    cpid INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    comment TEXT
)

CREATE TABLE Mechanics (
    mech_name INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    description TEXT
)

CREATE TABLE Collections (
    cid INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    title VARCHAR NOT NULL,
    description text
)

CREATE TABLE Libraries (
    lid INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    title VARCHAR NOT NULL,
    description text
)

CREATE TABLE CopyOf (
    cpid INT NOT NULL REFERENCES Copies(cpid),
    gid INT NOT NULL REFERENCES Games(gid)    
)

CREATE TABLE DesignedBy (
    uid INT NOT NULL REFERENCES Users(uid),
    gid INT NOT NULL REFERENCES Games(gid)    
)

CREATE TABLE Implements (
    mech_name INT NOT NULL REFERENCES Mechanics(mech_name),
    gid INT NOT NULL REFERENCES Games(gid)    
)

CREATE TABLE ReviewOf (
    uid INT NOT NULL REFERENCES Users(uid),
    gid INT NOT NULL REFERENCES Games(gid) ,
    rating INT NOT NULL,
    description TEXT,
    time_posted timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
)

CREATE TABLE HasGame (
    cid INT NOT NULL REFERENCES Collections(cid),
    gid INT NOT NULL REFERENCES Games(gid)    
)

CREATE TABLE HasCopy (
    lid INT NOT NULL REFERENCES Libraries(lid),
    gid INT NOT NULL REFERENCES Games(gid)    
)

CREATE TABLE CreatedBy (
    cid INT NOT NULL REFERENCES Collections(cid),
    uid INT NOT NULL REFERENCES Users(uid)    
)

CREATE TABLE Owns (
    lid INT NOT NULL REFERENCES Libraries(lid),
    uid INT NOT NULL REFERENCES Users(uid)    
)

CREATE TABLE LikesCollection (
    cid INT NOT NULL REFERENCES Collections(cid),
    uid INT NOT NULL REFERENCES Users(uid)    
)

CREATE TABLE LikesGame (
    gid INT NOT NULL REFERENCES Games(gid),
    uid INT NOT NULL REFERENCES Users(uid)    
)

CREATE TABLE CheckedOutBy (
    cpid INT NOT NULL REFERENCES Copies(cpid),
    uid INT NOT NULL REFERENCES Users(uid)    
)

CREATE TABLE PlayCount (
    gid INT NOT NULL REFERENCES Games(gid),
    uid INT NOT NULL REFERENCES Users(uid),
    count INT NOT NULL  
);
