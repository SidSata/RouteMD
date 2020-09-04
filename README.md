
# Route MD

Link to demonstration: https://youtu.be/_ty3Uxj_9xE

Link to devpost submission: https://devpost.com/software/route-md

### I (Siddhant Satapathy) worked on the dynamic front-end using HTML/CSS, Javascript and Bootstrap, as well as on the static About pages used in the demonstration.

## Inspiration
“‘The mayor of one town complained that doctors were forced to decide not to treat the very old, leaving them to die.” -The New York Times on the COVID-19 crisis in Italy

Harrowing quotes like these encapsulate the horrifying extent of the COVID-19 crisis and how it turns hospitals into triage wards. The brunt of this is borne not just by patients, but by healthcare professionals as well, who often have to work long hours and make unimaginable decisions about who lives and who doesn’t, leaving mental scars which they carry with them for the rest of their lives.

After realizing this, we were inspired to come up with a system that assists medical workers in moving new patients, and reallocating existing ones in order to save the greatest number of lives.

Route MD is the result of that inspiration.

## What it does

The patient’s details are entered into a database, then a Machine Learning algorithm evaluates key data points to provide an optimum room recommendation within seconds.

In case a room is completely filled and the current patient is at risk, the ML algorithm makes suggestions to allocate space by moving a lower-risk patient to another ward.

The algorithm is programmed with medical ethics in mind, and learns when its recommendation is declined by a human. Through Route MD, medical workers need not worry about moving patients, and can instead focus on what they do best: saving lives.

Aside from decreasing the burden on healthcare professionals, Route MD enables administrative workers to easily access and update patient records, and reduces waiting times for patients if a suitable reallocation is available.

## How we built it
We started off by instantiating a real-time database system on Google Firebase and by building a supplementary Python application that could access, modify, and maintain records in the database. Concurrently, we also developed the main hospital information page using HTML, CSS, BootStrap, JavaScript and jQuery, and the various forms that accompanied the addition, removal, and updating details of patients.

After this was completed, we transitioned into designing and implementing the machine learning algorithm that evaluates several key data points for each patient (Age, Disease, Drug history, etc.) and assigns a score to the patient from 0 to 1, where a score of 0 is the least vulnerable and a score of 1 is the most vulnerable. By assigning and comparing the scores of new patients to existing ones, the algorithm recommends where to move new patients and reallocate existing ones.

We also used a Flask server with Jinja templating in order to edit the HTML pages in real time. Ultimately, we glued our entire website together and created an About section to describe our project.

## Challenges we ran into
As we were all beginner hackers, the main challenge we faced was learning new skills and programming techniques in a short period of time. Additionally, we faced issues in integrating our javascript frontend with our backend, which took up a significant portion of our time and really tested our skills to their limit.

## Accomplishments that we're proud of
As we were all beginner hackers who hadn’t worked with each other before, getting a functional prototype up and running was a major accomplishment! Managing to maintain the deadlines we set, completing the work allocated to us on time and successfully building a website which has the potential to make hospital management systems more efficient and save lives especially in the current global situation, are accomplishments that we are proud of.

## What we’ve learnt:
Throughout this hackathon, we have learned to plan ahead and conform to deadlines, yet also have the flexibility to adapt to and overcome challenges. We improved our programming skills and learned to work with certain programming languages and interfaces that we don’t have much experience with.

## What’s next for Route MD
A thing that was in our minds but we couldn’t quite manage to accomplish was a dynamic visual representation of the rooms in a hospital and how the occupancy trended over time, as this could hold valuable information for hospital personnel. A future version of Route MD will likely focus on this. Currently, Route MD caters to just one hospital at a time, and it’s capacity for handling patients is rather limited. We plan to expand Route MD to cater for larger hospitals, eventually turning it into a multi-hospital management system for communities around the world.

