## Inspiration

Given the literature about the [underrepresentation of women](https://www.natureindex.com/news-blog/women-edged-out-of-last-named-authorships-in-top-journals) in high impact journals, and the
[high attrition rate of women](https://www.insidehighered.com/news/2017/08/29/study-says-multiple-factors-work-together-drive-women-away-stem) in higher education, we were motivated to characterize gender disparity
in bioRxiv submissions. 

The main idea behind this project is to characterize the gender of the first author in a bioRxiv submission, and use thatinformation to decide whether or not to retweet to shine a spotlight on the first author. Our approach also enabled us to analyze a variety of information about past bioRxiv tweets.

## What it does

This project was used to create a twitter bot , [SbotLite](https://twitter.com/sbotlite), which retweets articles by female first authors. We had a dual purpose. The first was to accurately represent the problem of gender bias in scientific submissions, and to raise awareness about the issue. The second was to make sense of the data that we acquired through the course of this project. 

We also analyzed around 1000 past bioRxiv tweets to characterize the gender disparity in submissions 

## How we built it

We used tools like gender-guesser python module, google colab to code collectively, tweepy for working
with the twitter api and git/github to keep all of our code version controlled and cohesive! We also hosted
the real time anlysis on google cloud.

## Challenges we ran into

Data wrangling challenges, extracting correct gender of first names across cultures, deciding which information
we want our bot to highlight

## Accomplishments that we’re proud of

The fact that our bot can actually make positive impact in the world, and the fact that we all worked
so well together as a team, and contributed equally to the project

## What we learned

Even automated analysis makes a strong case for intersectionality. Using our approach, we were able to quantify the gender disparity in scientific submissions. However, our friendly neighborhood Twitter Bot, SbotLite, seeks to address this bias, one tweet at a time!  

## What’s next for sBotLite
- Implementation of better handling for ambiguous names using gender guesser module
- Annotating gender of senior authors 
- Assess whether senior women tend to have more women collaborators 
- Real time analysis of gender disparity in bioRxiv retweets
- Generalization to scientific journals
- Create a gender-tagging system for new authors 

