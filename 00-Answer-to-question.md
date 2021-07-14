## Tell us about your similarity calculation and why you chose it.
I put the metrics as an variable in the config.yml file. This helps to test different metrics to
test which one works better. 
- Cosine simialrity: Mainly has application for vectors of variables which have different length such as
comparing two documents. . It is the cosine of the angle between two vectors(could be same size or very different) in hyperspace. I started with this approach because it is apporporiate for the problem that we have in hand. Users could be widely different from each other and many of them could have no assessments at
all. Some othem might take just 1 course and the other could take 10s of courses. This i translated in vectors with very different sizes in different directions. However, two users (lets assume represented by a vector) could have diffenet courses and assessment taken by are both in the near direction (let's say cloud
computing direction in hyperspace). Thus, cosine similarity appears a good metric to use. 

However, there is an performance issue here. Cosine similarity requires brute force approach in SKlearn and 
also a defining a custome metric, because it's not techically a metric: it outputs one if they are the same and -1 if they are opposite. Sklearn algorithms are optimized to work with Euclidean, Minkowski, and several other metrics.  Let's have a look at the equation: 

\n<a href="https://www.codecogs.com/eqnedit.php?latex=\LARGE&space;xT&space;y&space;/&space;(||x||&space;*&space;||y||)" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\LARGE&space;xT&space;y&space;/&space;(||x||&space;*&space;||y||)" title="\LARGE xT y / (||x|| * ||y||)" /></a>




the cosine similarity. I  
- Euclidean and Manhattan are calculated based on difference between cartesian coordinates, squared and absolute 
differences, respectively.
- Minkowski is what I chose with a degree of 2, which is equivalent to Euclidean.
- Jaccard is intersection over union. It is sensetive to size of the data and can be misleading in small size data
- 