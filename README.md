# HAPPYFOX ASSIGNMENT

## pre-requisites to running the scripts

### Install Requirements

` pip install requirements.txt `

### PostgreSQL database

Sample commands to create db using Docker

``` 
docker pull postgres

docker run --name local-postgres -e POSTGRES_PASSWORD=xxxxx -d -p 5432:5432 postgres 

```

### Google OAuth credentials

Save Google OAuth credentials in a file named client_secrets.json with the below format

```
{
"web": {
"client_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
"client_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxx",
"redirect_uris": [],
"auth_uri": "https://accounts.google.com/o/oauth2/auth",
"token_uri": "https://accounts.google.com/o/oauth2/token"
}
}
```

### env 

Save the environment credentials in a .env file. The following variables are required
```
DB_HOST=xxxxx
DB_NAME=xxxxx
DB_USER=xxxxx
DB_PASS=xxxxx
```


## Instructions

There are 2 scripts 

### Part 1 

Fetch the emails using GMail API and store them in the database

` python part1.py`

### Part 2

Choose a rule and process the emails as per the rule

` python part2.py `
