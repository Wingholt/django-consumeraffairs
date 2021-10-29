# cosumeraffairs-test
### _C. Wing Ho_

### Current Status
    These are working code that can be run locally.

### Design
- Users send their data to the webserver
      localhost:8000/eye
> data is stored as cache/db/file... (For simplicity I will store them in cache for now)
- Users can get the whole report (all stored data)
       localhost:8000/report/all
- Users can request filtered data, for example {“category” : “page interaction”}
       localhost:8000/report
- Users can query count by session, category or name

      localhost:8000/session/count
      localhost:8000/category/count
      localhost:8000/name/count

### Other considertaions
- "Applications should be recognized as "trusted clients" to "The Eye" - *Can add clients' IP address to ALLOWED_HOSTS[] in settings.py*
-  "The Eye will be receiving, in average, ~100 events/second, so consider not processing events in real time" - *Can be done in background, kicked off by a cron job periodically for instance, or when traffic is slow.*
-  "When Applications talk to "The Eye", make sure to not leave them hanging" - *Save input and process later so from client's point of view it is a fire and forget (only after data is stored successfully of course)*
-  "Your models should have proper constraints to avoid race conditions when multiple events are being processed at the same time" - *In production multiple instances of Django should really be running in each CPU (each with a number of suprocesses) of a multi-core linux platform (Apache/mod_wsgi can configure that), on top of that the Big IP should do load balancing as well. Multi-threads may be considered, but Django doesn't work too well with multi-threads, it is tricky.*
*
### Assumptions
- For each session user sends only one event at a time

------------


### TODO
- Add input validation.
- Query with given time range.
- Allow users to send multiple events.
- Write input to file so you don't need to reenter all input again after webserver restart.
- spawn background job to process data when webserver is not busy and be able to run on demand.
- Convert response to JSON from native Python dictionary.
- Add model serializer to take advantage of Django Rest Framework.
