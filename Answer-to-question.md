1. **Tell us about your similarity calculation and why you chose it**  

- I put the metrics as an variable in the config.yml file. This helps to test different metrics to
test which one works better.  
**Cosine simialrity** mainly has application for vectors of variables which have different length such as
comparing two documents. It is the cosine of the angle between two vectors in hyperspace. I started with this approach because it is apporporiate for the problem that we have in hand. Users could be widely different from each other and many of them could have no assessments at
all. Some of them might take just 1 course and the other have taken 10s of courses. This is translated in vectors with very different sizes in different directions. However, two users (lets assume represented by two vectors) could have diffenet courses and assessment taken, but are both in a near direction (let's say cloud
computing direction in hyperspace). Thus, cosine similarity appears a good metric to use.

- However, there is an performance issue here. Cosine similarity requires brute force approach in SKlearn and 
also defining a custome metric. It's not techically a distance metric: it outputs 1 if they are the same and -1 if they are opposite. Moreover, it fails the the traiangle inequality! Sklearn algorithms are optimized to work with Euclidean, **Minkowski**, and several other distance metrics.   
The solution is have the norm2 Euclidean distance on normalized feature vector, which mathematically give very similar results to the Cosine similarity. I followed this approach and normalized the data as a step in 
the pipline. The metric in the config.yml file is "Minkowski" with a P=2, which is the same as Euclidean.
###
2. **We have provided you with a relatively small sample of users. At true scale, the number of users, and their associated behavior, would be much larger. What considerations would you make to accommodate that?**  

- One important correction is to incorporate a capability in the code to handle the users who don't have any history data. This could be challenging, but a trivial solution is that to return a list of users who most recently joined from the similar area or a list of users who have taken most popular courses. If the new users have shon some interests before, we can skip finding the similar users and directly sugget them the courses they showed interest for.


- We can pre-compute a table with nearest neighbors(e.g. 10 most similar users) for each user on daily basis and save it in Azure database or any other database. Then a call to the API  directly queries the database and lower the response time. This comes with the cost of precomputing job through a automatic pipeline on a daily basis but the API response could be very fast. 

- I would also look into optimization on the Database side, for example index the user alphabetically, or fo example partition the data based on the view date or registration date. Then I leverage the partitions filter in my SQL ETL for feature generations, for example for a View_date, I add a view_date_mnth and apply it in a "where" clauses, such as
###
```
where
        view_date_mnth > "2012-06"
```
###
- Moreover, leveraging Spark/Pyspark/sparksql could efficiently distribute the jobs in a cluster and speed up querying the databse. The SQL scripts themselves have room for improvement. I used several CTEs for tables, which could have been avoided by joinig tables all toghether in one query using nested queries. This could harm or improve efficiency depends on the spark cluster. However, I kept the CTEs separate and avoided nested SQL to keep the process clear to understand and debug.

- It could happen that using 30 million rows of data does not significantly change the model performance from a case that we use just 10 milion rows. So, I could explore this to say for example that we can just go with the data after 2015.

- Finally, the API side of the code can be improved for example by direct query the pre-computed nearestneighbor table.
###
3. **Given the context for which you might assume an API like this would be used, is there anything else you would think about? (e.g. other data you would like to collect?**
- I would collect the demographic data if law lets me and have the user permission.features such as age, sex, state, zipcode, level of education, occupation, company, level of seniority could potentially help to find similar users better.
- Shopping data, that would be greate if we get our hands on data that shows if the user has shopped around prior joining Pluralsight.
- Review data such as ratings, comments, likes to leverage NLP tools.
- Billing data such as payplan, was it by credit card or debit card, how much was the course
- Calculating a tenure feature by knowing the total number of days that a user was on a payplan and used the platform. The counterpart of this feature is the lapse time the uer took off the platform and re-joined.
- Discounts that user are getting. 
- the final API can also be used to peer users toghether for example to help each other or compete against each other. Moreover, we can use this model to lower user churns. Suppose that we have 100 customers who have churned. We can get 500 potential customer who will churn in coming weeks. We can act proactively and reach out to them with special discount or free courses. 


