## Well this is pretty much a webcrawler, so lets make one

---
to run, either:
```bash
pip install -r requirements.txt
uvicorn src.api:api --host 0.0.0.0 --port 8000
```

Or use any host and port you wish, but this one is standard.
the root (/) route will drop you on the swagger docs, but you can also use the program by http POST to localhost/crawler with a body like
```json
{
  "url": "String",
  "max_depth": "Int",
  "max_ext": "Int",
  "unique": "Boolean"
}
```
Where:
1. url is the starting point of the crawl
2. max_depth is how far in you wish to dive
3. max_ext is how many urls you wish to get from each one
4. Unique is if you wish to allow duplicates

Nothing's got a default set, so you must give EVERY parameter. This is out of consideration that if you do not know what you want, this program shall not try to guess it.

The Results will be generated and save inside /results, where the root is where you decided to run it from. absolute path on PC can lead to insecure access and errors, so be mindful of your location!

You could also setup the application with docker like so:
```bash
mkdir results
docker build -t demo_image .
docker run -d --name demo_container -p 8000:8000 demo_image
```
This would be useless without a way to connect to the container, as the results are saved inside the container, which you may or may not be able to connect and use.

Or you could mount it, if you feel like it.

---
Task description-

Write a software program that downloads a source URL/s html and the html of URL/s appearing in the resulting page/s.  The program should accept 4 arguments:  

1. The URL to start the process with.  
2. The maximal amount of different URLs to extract from the page.  
3. How deep the process should run (depth factor).  
4. Boolean flag indicating cross-level uniqueness.


 Store each page downloaded to a file, naming convention should be ‘<depth>/<url>.html’ – meaning each depth should have its' htmls stored in a separate folder – If needed, replace any characters not allowed for file names with an underscore. 

Example  Url: https://www.ynetnews.com/ , maximum: 5, depth factor: 2, uniqueness: true.

Depth 0: 
The program should fetch and save the source URL content to 0/www_ynetnews_com.html, extract 5 new URLs from it and fetch them in the next level.
 
Depth 1:
 The program should fetch and save the html content of the 5 URLs from depth 0, save them to 1/<file-name>.html, and extract up to 5 new and different URLs from each html to fetch in the next level. (Since the uniqueness flag is true, the URLs should be different from those found in depth 0 as well as those already found)    

Depth 2:  
The program should fetch up to 5*5 URLs from depth 1, save their html content to 2/<file-name>.html, and terminate.
