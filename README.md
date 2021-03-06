# UnifyID-Challenge
Challenge for UnifyID Full Stack Engineer position.


Fun with Random.org
This challenge is programming language agnostic! Pick whichever language you're most comfortable with. Random.org is a web front-end to an atmospheric noise sensor, which can give us pretty good random numbers. It's the reverse from a noise cancelling filter, since it cancels everything BUT the noise. Weather conditions, solar flares, a full-moon can have little impact on this, since it focuses on getting the purest white noise possible from their hardware sensors. If you too think this is cool, you'd be thrilled to try our challenge:

1. Using the HTTP API for random.org (https://www.random.org/clients/http/) we will ask you to get truly random numbers. Look out for the guidelines, or you may get banned!

2. Using these random numbers create one of the following, to get bonus points:

- An RGB bitmap picture of 128x128 pixels. (70 points)  /// ALMOST ///

- A white noise WAV sound sample of 3 seconds (70 points)

- An RSA key pair. (100 points) /// COMPLETED ///

3. Push your code and one of the 3 requirements on github on your own public repo. Send us an email back at jobs@unify.id with your repo URL. You have 3 hours and we'll check your time on whatever is earliest, the timestamp on your last commit or your email reply back. Have fun with randomness!


Summary of Work:

I started out reading the website and figuring out the JSON requests and API format. Then I built the helper generation functions for integers and hex blobs. I first coded the bitmap requirement but realized that 128x128x3x8 was too many bits for my API KEY to handle and I wouldn't be able to complete the first one. An RSA key only takes 1024 bits rough minimum (some accept down to 512) so I did that one. It took a little bit of reading through the pycrypto library documentation. The links to references I used can all be found in the code.
