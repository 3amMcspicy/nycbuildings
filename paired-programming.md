# Paired Programming Assignment -aparnac25

### Goal of the project: Is it clear to you from the proposal.md how the goal can be accomplished using Python and the specified packages?

I think the goal is pretty clear. He wants to present an untouched dataset, where users can visually look at water and electricty consumption data. The packages look alright, there is a program I came across called `kepler.gl` which would make some pretty cool maps. 

### The Data: Is it clear to you from the proposal.md what the data for this project is, or will look like?

From the project description I was a little unsure about what the data would look like. But after discussing it, I think the data will be a csv file that the website has access to and specifically just on water and electricty consumption.  

### The code: (Look at the Python code files in detail first and try to comprehend a bit of what is written so far)

No code has been written so far. 

### Does the current code include a proper skeleton (pseudocode) for starting this project? What can this code do so far?

Not yet

### Ideas, questions, code...

I can't remember did you want to download the csv and have the website the user goes to call that or have the csv already online? Would you need to return the csv data as a json format for the website or `FastAPI`. I'm not hundred percent sure I fully understand fastAPI. If you have to do that you may have to also import `json` right? I was wondering if you could just use the JSON URL they have on their website instead of downloading and manipulating a csv and having the file online. And with the JSON URL choose the data you want to be represented? 

Like what we've had on the tutorials..


`URL = "https://data.cityofnewyork.us/api/views/66be-66yr/rows.json?accessType=DOWNLOAD"`

`response = requests.get(URL)`

`response.status_code`

save it has maybe a dictionary?

`wdict = response.json()`

and convert that into a pandas data frame? this is really basic code and I know that the tutorials have it...but I don't know if this an avenue you would want to take? 

These are my intial comments but I wanted to send this to ASAP 