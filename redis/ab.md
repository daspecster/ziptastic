Totally un-scientific tests!

# Redis WSGI Server (spawning, one process)

	$ spawning zipapiserver.application -s 1

## AB

	$ ab -n 1000 -c 100 'http://localhost:8080/?zipcode=68102'

## Results

	This is ApacheBench, Version 2.3 <$Revision: 655654 $>
	Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
	Licensed to The Apache Software Foundation, http://www.apache.org/

	Benchmarking localhost (be patient)


	Server Software:        
	Server Hostname:        localhost
	Server Port:            8080

	Document Path:          /?zipcode=68102
	Document Length:        69 bytes

	Concurrency Level:      100
	Time taken for tests:   1.039 seconds
	Complete requests:      1000
	Failed requests:        0
	Write errors:           0
	Total transferred:      228000 bytes
	HTML transferred:       69000 bytes
	Requests per second:    962.85 [#/sec] (mean)
	Time per request:       103.858 [ms] (mean)
	Time per request:       1.039 [ms] (mean, across all concurrent requests)
	Transfer rate:          214.38 [Kbytes/sec] received

	Connection Times (ms)
								min  mean[+/-sd] median   max
	Connect:        0    0   0.3      0       2
	Processing:    26   58  28.7     53     308
	Waiting:       26   58  28.7     52     308
	Total:         26   59  28.9     53     308

	Percentage of the requests served within a certain time (ms)
		50%     53
		66%     63
		75%     80
		80%     83
		90%     91
		95%     99
		98%    102
		99%    103
	 100%    308 (longest request)

# Original App

	$ python zipapiserver.py

## AB

	$ ab -n 1000 -c 100 'http://localhost:8080/?zip=68102'

## Results

	This is ApacheBench, Version 2.3 <$Revision: 655654 $>
	Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
	Licensed to The Apache Software Foundation, http://www.apache.org/

	Benchmarking localhost (be patient)


	Server Software:        BaseHTTP/0.3
	Server Hostname:        localhost
	Server Port:            8080

	Document Path:          /?zip=68102
	Document Length:        49 bytes

	Concurrency Level:      100
	Time taken for tests:   17.793 seconds
	Complete requests:      1000
	Failed requests:        0
	Write errors:           0
	Total transferred:      205000 bytes
	HTML transferred:       49000 bytes
	Requests per second:    56.20 [#/sec] (mean)
	Time per request:       1779.349 [ms] (mean)
	Time per request:       17.793 [ms] (mean, across all concurrent requests)
	Transfer rate:          11.25 [Kbytes/sec] received

	Connection Times (ms)
								min  mean[+/-sd] median   max
	Connect:        0   18 402.8      0    9011
	Processing:    40  150 840.0    101   17792
	Waiting:       40  150 840.0    101   17792
	Total:         41  168 1047.4    101   17793

	Percentage of the requests served within a certain time (ms)
		50%    101
		66%    102
		75%    103
		80%    105
		90%    107
		95%    108
		98%    110
		99%    111
	 100%  17793 (longest request)

