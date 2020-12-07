## Architecture
-----------------------------
-----      Crawler      -----
-- crawls for github links --
----        MAVEN       -----
-----------------------------
             ll
             ll feeds github links into (also associated published releases tag)
             \/
------------------------------
-----       Extract      -----
--- fetches repo + release ---
------------------------------
             ll
             ll 
             \/
------------------------------
-----       Runner      ------
--- fetches repo + release ---
------------------------------
             ll
             ll 
             \/
------------------------------
------       App       -------
----    runs everything   ----
------------------------------


## Crawler
For the Crawler, it could crawl for different types of **published artifacts** from websites such as 
- Maven (Java)
- PyPi (Python)
- NPM (JS and TS)

