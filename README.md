# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
The domain I chose is based on student reviews of different professors in Computer Science at Arizona State University.
This knowledge is valuable and hard to find through official kind of knowledge, which are official university resources do not
highlight real course experience from students based on the teaching style of their professor, workload, exams, grading, and course expectations. 
Real kind of knowledge, like Rate My Professor reviews, uncover the true knowledge or information about a professor and the course under a professor,
along with those other aspects, and this RAG system will make the knowledge from these student reviews searchable so that other students can get
accurate and precise information about professors while getting more grounded answers based on reviews. 

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | prof1.txt | text file | https://www.ratemyprofessors.com/professor/2813800|
| 2 | prof2.txt | text file | https://www.ratemyprofessors.com/professor/1837088|
| 3 | prof3.txt | text file | https://www.ratemyprofessors.com/professor/1674624|
| 4 | prof4.txt | text file | https://www.ratemyprofessors.com/professor/2095554|
| 5 | prof5.txt | text file | https://www.ratemyprofessors.com/professor/2844149|
| 6 | prof6.txt | text file | http://ratemyprofessors.com/professor/2042001     |
| 7 | prof7.txt | text file | https://www.ratemyprofessors.com/professor/500103 |
| 8 | prof8.txt | text file | https://www.ratemyprofessors.com/professor/1167426|
| 9 | prof9.txt | text file | https://www.ratemyprofessors.com/professor/1661785|
| 10| prof10.txt| text file | https://www.ratemyprofessors.com/professor/2920261|

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

Each document contains 10 reviews for one professor, and each reviews varies in length, roughly between 5-75 words. Each review can be very short and brief or detailed, but not too long in length. Since each review has a different word count and are self-contained, we can treat each review as one chunk so that we can preserve the contents of each student's review about a professor as the reviews can be made by different students.
That being said, each chunk could be around 20-90 tokens.

**Overlap:**

The overlap size is 0.

**Why these choices fit your documents:**

Each student review could be different from other student review within a document, causing reviews to potentially be independent from each other. These reviews could be made from different students, and they may not be related to each other in terms of grading , workload, professor teaching style, and other factors as they could be based on different courses that had different course structures and sometimes students may have different opinions on a professor. For a worse case scenario, it would be recommended to treat each review seperately where in this case, one review would be one chunk. Each review is small in content, which is why we chose the value of chunk size to be around 20-90 tokens, and since we treat each review independently, the overlap would be 0.

**Final chunk count:**

Final chunk count is 100 as there are a totla of 100 review across all the 10 files.


**5 Labeled Sample Chunks**

Professor: Joshua Daymude
Review #: 1
Text: Dr. Daymude is one of the most talented professors at ASU. He has devised a curriculum that breaks down a complicated subject into digestible chunks in which the most important aspects are revisited at specific points in the semester. His class is not something you will forget about soon after you finish it.
--------------------------------------------------------------------------------
Professor: Bharatesh Chakravarthi
Review #: 1
Text: Class is super easy. Allows cheat sheet for exams, and project difficulty is just how lucky you get with the group.
--------------------------------------------------------------------------------
Professor: Ryan Meuth
Review #: 1
Text: Probably the most organized online course I've ever taken. Material is presented in an easy-to-understand manner through ZyBooks. ZyBooks can be wordy at times though, so just make sure to leave time to read through it. The questions and practice scatter in between the reading help comprehension. If you're not sure, the discuss board can help a lot
--------------------------------------------------------------------------------
Professor: David Claveau
Review #: 1
Text: My Exam scores were lowered during Finals Week without any notification, luckily I noticed and spoke up but it was very frustrating. I would've finished with a C but got a D because of it. Dr. Claveau blamed the graders and called it small adjustments. Grading is split across platforms and his TAs only show up during Exams, he's very unorganized!
--------------------------------------------------------------------------------
Professor: Ming Zhao
Review #: 1
Text: Hard class. Don't take if you don't want to put the effort in. Very rewarding and you'll get a lot out of it if you actually spend time to learn material/do the projects legit. I probably learned the most from this class out of any of my upper level/grad classes. Grading is tough and lectures can be hard to follow, but expectations are clear.
--------------------------------------------------------------------------------
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

I will be using the all-miniLM-L6-v2 via sentence-transfomers. I think this embedded model will be effective for embedding the chunks because we are dealing with chunks of short length. In addition to that, this embedding model is also optimized primarily for semantic chunking where it will find similarities semantically on sentences. 
**Production tradeoff reflection:**

If I were deploying this for real users and cost wasn't a constraint, I would weign in accuracy on domain- specific text and latency. 
For accuracy on domain-specific text, this is a important tradeoff when choosing another embedding model. the one we selected is optimized for semantic chunking on short text and takes up less time, but it could hinder accuracy compared to more complex and larger models. It may not be able to recognize the meaning of different wording whether that's specific terms like slang words or language that could imply the same thing, but uses different wording. If a different embedding model was selected, it would be a more accurate model that could recognize informal text or sentences  involving different wording that imply the same meaning and would also better recognize relationships between different chunks, allowing for more relevant chunks closer in meaning to be retrieved. 
Latency is also relevant because we need to make sure the model is generating quck responses, meaning we would have to reduce latency as efficient as possible. Our embedding model is lightweight and of reasonable size and is able to respond quickly. Choosing a larger, and more accurate model that could also be more complex would improve the process of retrieving more relevant and related chunks close in meaning to a query, but could  take up more time to respond. 

---

## Data Retrieval Test Examples:

1. Query: Which professor receives most praise for explaining challenging concepts in a clear manner?
Explanation: The returned chunks below are relevant to the user query above because each review contains direct language about a professor's ability to make difficult material understandable. Gordon's review mentions projects being "clearly explained" and a genuine desire for students to understand. Daymude's reviews stand out because proofs are inherently challenging, and reviewers specifically credit him with making them enjoyable and being "amazing at breaking down concepts." Claveau's review similarly praises his ability to explain concepts, with students retrospectively wondering why they ever struggled.

**Retrieved Chunks**

Result 1
Professor: James Gordon
Review #: 4
Distance: 0.338
Text: Amazing professor overall. His projects were always clearly explained, and the expectations were very straightforward. He was consistently available to answer questions and genuinely wanted students to understand the material. The class was well organized, and you could tell he cared about helping everyone succeed.
Source: prof5.txt

Result 2
Professor: Joshua Daymude
Review #: 2
Distance: 0.383
Text: Incredible professor! Grading is clear, lectures are as engaging as it can get for a class riddled with proofs. Singlehandedly made me enjoy proofs. Assignments are reasonable and helpful. Understands the purpose of the class and there is little shame in asking questions. Prof was given a round of applause on the last day of the semester!
Source: prof1.txt

Result 3
Professor: Joshua Daymude
Review #: 5
Distance: 0.418
Text: Geniunely the best professor I've had so far at ASU. Wasn't looking forward to this class, but he makes it super enjoyable and is amazing at breaking down concepts. The only thing I'm not a fan of so far is students grading each other's work.
Source: prof1.txt

Result 4
Professor: David Claveau
Review #: 9
Distance: 0.424
Text: Finally, an actual teacher at ASU. He lectures in a very traditional style with slides and walking around that is at times difficult to follow if it's complicated. However, he is very accessible to asking questions and explaining concepts. By the end of the class you'll wonder why you struggled. Apply yourself! He really cares about his students.
Source: prof3.txt

2. Query: Which professor is frequently described as approachable and supportive, especially when being able to help students outside class?
Explanation: he returned chunks below are relevant to the user query above because each review speaks to a professor's availability and investment in students beyond the classroom. Gordon is described as "consistently available to answer questions," which directly reflects out-of-class accessibility. Daymude's review is the strongest match, explicitly stating he is "easy to reach outside of class" and even adjusted the course based on student feedback — a clear sign of responsiveness. Claveau is described as "very accessible," and while Daymude's sixth review doesn't mention office hours specifically, the sentiment that he "cares about his students and their experience" still signals the kind of supportive presence the query is looking for.

**Retrieved Chunks**

Result 1
Professor: James Gordon
Review #: 4
Distance: 0.385
Text: Amazing professor overall. His projects were always clearly explained, and the expectations were very straightforward. He was consistently available to answer questions and genuinely wanted students to understand the material. The class was well organized, and you could tell he cared about helping everyone succeed.
Source: prof5.txt

Result 2
Professor: Joshua Daymude
Review #: 8
Distance: 0.409
Text: One of my favorite ASU professors so far. Incredibly organized and a great lecturer, which is important for this course. Easy to reach outside of class and even made changes in response to student feedback. Great example of a professor who truly cares about students and their learning. Highly recommend.
Source: prof1.txt

Result 3
Professor: David Claveau
Review #: 9
Distance: 0.435
Text: Finally, an actual teacher at ASU. He lectures in a very traditional style with slides and walking around that is at times difficult to follow if it's complicated. However, he is very accessible to asking questions and explaining concepts. By the end of the class you'll wonder why you struggled. Apply yourself! He really cares about his students.
Source: prof3.txt

Result 4
Professor: Joshua Daymude
Review #: 6
Distance: 0.440
Text: Easily the best instructor I've had at ASU. His lectures were clear and informative and the homework did a great job of supplementing and reinforcing the material. It's abundantly clear that he cares about his students and their experience. It was incredibly refreshing in a program that seems to care more about pumping people through for profit.
Source: prof1.txt

3. Which professor receives the most complaints about their curriculum and being difficult with hard or unfair exams?

Result 1
Professor: Xuerong Feng
Review #: 6
Distance: 0.400
Text: the most frustrating class I have taken. A frustrated professor/TA's when we are collectively confused & don't understand them, difficult / complicated tutorials, lots of figure it out on your own stuff. Programs are also nitpicky and no curved grading, the only thing we have that is considered grace is the extra credit quizzes. 0/10
Source: prof8.txt

Result 2
Professor: David Claveau
Review #: 6
Distance: 0.458
Text: Dr. Claveau is one of the worst CS profs at ASU, he clearly favors girls in the class and won't even let kids go to the bathroom during an exam even if it's an emergency. Unlike Gordon who's tests are 10x easier, Claveau's tests are way harder than he makes them seem. I'm sure bro wrote most of the good ratings and reported most if the bad ones.
Source: prof3.txt

Result 3
Professor: Subbarao Kambhampati
Review #: 7
Distance: 0.463
Text: The professor mostly just talked about himself and how AI is going to impact the world. He did not seem to actually know the Math that well behind the topics (he would just handwave formulas that he couldn't prove himself). On top of this, he made many rude comments towards certain groups of students. The exam questions usually had multiple answers
Source: prof9.txt

Result 4
Professor: Ming Zhao
Review #: 10
Distance: 0.468
Text: CONCEPTS EASY, TESTS ACTUALLY UNFAIR. I wasn't even in his section, but since he's the department chair, Alpha Z actually bullies other teachers for advocating for his students. Both the midterm and bonus quiz are worth an average of 50%. If he can actually get a 95% on his test i will eat my words and say this class is ok.
Source: prof4.txt

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

The system enforces grounding at the generation stage by strictly constraining the LLM to only use retrieved chunks returned from ChromaDB. The system prompt explicitly instructs the model that all answers must be based solely on the retrieved reviews and must not use outside knowledge or speculation.
The core grounding instruction used in the system prompt is:

You are a grounded RAG assistant.
Use only the retrieved reviews as evidence.
You may summarize and compare information across the reviews,
but do not use outside knowledge.

In addition to the system prompt, the user prompt further reinforces grounding with explicit constraints:

IMPORTANT RULES:

1. Use ONLY information found in the retrieved reviews.
2. Do NOT use outside knowledge.
3. Do NOT invent facts that are not supported by the retrieved reviews.
4. You MAY summarize, compare, and synthesize information across multiple retrieved reviews.
5. Any conclusion must be reasonably supported by the retrieved reviews.
6. When appropriate, mention the source filename that supports the information.
7. If the retrieved reviews do not provide enough evidence to answer the question, respond exactly:
   "I could not find enough information in the retrieved reviews."

**How source attribution is surfaced in the response:**

Source attribution is handled before the model is called, during context construction. Each retrieved chunk from ChromaDB includes metadata such as the professor name, source filename (e.g., prof1.txt), and the review text.

These fields are formatted into a structured context block that is passed directly into the prompt. For example:

Professor: Joshua Daymude
Source File: prof1.txt
Review Text: Easily the best instructor I've had at ASU...

All retrieved chunks are combined and included in the prompt under a “Retrieved Reviews” section. This ensures the model always has access to both the content and its source information while generating a response.

After the model produces an answer, the system collects the source filenames from the retrieved chunks, removes duplicates, and returns them alongside the response. This is done by appending each source file to a list, then converting it to a sorted set before returning.

These sources are then displayed in the UI under “Sources Used,” allowing users to verify that the response is grounded in specific documents rather than external knowledge.

---

**Grounded Generation with Source Attribution**

1. First Query: Which professor receives most praise for explaining challenging concepts in a clear manner?

***System Response***:
Based on the retrieved reviews, Joshua Daymude (prof1.txt) and David Claveau (prof3.txt) receive praise for explaining concepts clearly. However, Joshua Daymude is mentioned as being "amazing at breaking down concepts" and making a class "super enjoyable", suggesting he may receive slightly more praise for this aspect. James Gordon (prof5.txt) is also commended for clearly explaining projects and expectations. Among the retrieved reviews, Joshua Daymude seems to be highlighted for his ability to make complex concepts, such as proofs, enjoyable and clear.

Sources Used
• prof1.txt
• prof3.txt
• prof5.txt

2. Second Query: Which professor appears to leave the best overall impression on students?

***System Response***:
Based on the retrieved reviews, Joshua Daymude appears to leave a very positive impression on students, with one reviewer calling him "Geniunely the best professor I've had so far at ASU" (prof1.txt) and another stating he is "One of my favorite ASU professors so far" (prof1.txt). Similarly, James Gordon is described as "Amazing professor overall" (prof5.txt) and David Claveau is praised for being "very passionate about what he teaches" (prof3.txt). However, since two reviews praise Joshua Daymude, while the others have one review each, the retrieved reviews suggest that Joshua Daymude may leave the best overall impression on students.

Sources Used
• prof1.txt
• prof3.txt
• prof5.txt

**Out of Scope Query**: Which professor is seen to have the best teaching style in CSE 310?

***System Refusal Response***:
I could not find enough information in the retrieved reviews.

Sources Used
• prof10.txt
• prof3.txt
• prof7.txt

Grounding Enforced Explanation: Grounding is enforced in the prompt where I tell the Groq LLM that they are a Grounded RAG assistant where it should only used the retrieved context chunks given in the function parameter as its source for the answers it generates. I also emphasize this more then creating certain rules outlining different contraints of how it should be grounded such as "Use ONLY information found in the retrieved reviews", or "Do NOT use outside knowledge" or ."Do NOT invent facts that are not supported by the retrieved reviews". By including these rules, it provides better clarity on how grounding is involved when we are in the geneartion stage of the RAG implementation. 

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Which professor receives most praise for explaining challenging concepts in a clear manner?| Joshua Daymude| Bosh Joshua Daymude and David Claveau receive praise for explaining concepts clearly. James Gordon is also recognized for clearly explaining projects and expectations. Among these professors, Joshua Daymude  is most highlighted for his ability to make complex concepts, such as proofs, enjoyable and clear.  | Relevant| Accurate |
| 2 | Which professor is frequently described as approachable and supportive, especially when being able to help students outside class? | James Gordon | Both Joshua Daymude and James Gordon are described as approachable and supportive, with both being available to answer questions outside of class. David Claveau is also seen as accessible to asking questions, but Joshua Daymude is particularly highlighted for making changes in response to student feedback and being easy to reach outside of class  | Relevant | Partially Accurate |
| 3 | Which professor receives the most complaints about their curriculum and being difficult with hard or unfair exams?| Ming Zhao or David Claveau| Both Professor Ming Zhao and Professor David Claveau receive complaints about their curriculum and exams being difficult or unfair. Professor Xuerong Feng's review also mentions "difficult / complicated tutorials" and "no curved grading", but review for Professor Ming Zhao and Professor David Claveau specifically mention that the tests are "UNFAIR" and "way harder than he makes them seem", respectively. It is not possible to determine a single professor among these professors.  | Relevant | Accurate |
| 4 | Which professor is most often criticized for their coursework in terms of excessive workload or too much reading or course structure?| Xuerong Feng | Professor Xuerong Feng is criticized for their coursework, with the reviewer mentioning "difficult / complicated tutorials, lots of figure it out on your own stuff" and "no curved grading" | Relevant | Accurate |
| 5 | Which professor appears to leave the best overall impression on students?| Joshua Daymude | Joshua Daymude appears to leave a very positive impression on students. Both James  Gordon and David Claveau are also seen to be amazing professors and passionate about what they teach. However, oshua Daymude's reviews suggest the most consistently positive overall impression on students | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
Which professor receives the most student reviews that describe any course they taught as both difficult and rewarding?
**What the system returned:**
I could not find enough information in the retrieved reviews.

Sources Used
• prof1.txt
• prof5.txt
• prof9.txt
**Root cause (tied to a specific pipeline stage):**
The failure happens because the retrieval system is using semantic chunk search, which works for finding relevant text but not for aggregation tasks. Each retrieved chunk contains only individual reviews, so the model never receives a grouped view of all reviews per professor. As a result, it cannot count or compare how often each professor is described as both “difficult and rewarding.” The embedding-based retriever returns scattered, isolated examples rather than structured data, and the LLM correctly responds that there is not enough information to determine a ranking.
**What you would change to fix it:**
To fix this, the system should add a preprocessing or aggregation step that groups reviews by professor before sending them to the LLM. For questions involving comparisons or “most/least” logic, the pipeline should compute counts or structured summaries (e.g., how many reviews match certain traits per professor) and pass that instead of raw chunks. This would turn the system into a hybrid retrieval + aggregation pipeline, enabling it to handle ranking and frequency-based questions correctly.
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
THe spec helped me during implementation by providing in-depth explanations with clarity when my approaches and methods for different stages of our RAG implementation.
This gave better direction on how data retrieval, chunking, embedding, and generation are connected  and how each one interacts with the other, making it easier to
strcuture the Python scripts based on the  requirements for each Miletone. This reduced ambiguity and changes of hallunication from chatGPT and made sure each stage of the RAG implementation was created and designed in a accurate manner. 

**One way your implementation diverged from the spec, and why:**
One way my implementation diverged from the spec was it did not contain a way for me to include specific edge case that needed to be accounted for different stage of RAG,
especially chunking and retrieval and ranking or generation. Even though it described retrieval and chunking well, it did not understand how an LLM providing slightly different answers that implied the same meaning for a given question still meets the grounding requirements. 

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
I gave ChatGPT my Chunking strategy section from planning.md, a brief example structure of a .txt document I used for storing a professor's name, Unviersity name, Rate my professor URL, and list of 10 student reviews, the document section from planning.md, and my pipeline diagram of the RAG implementation. I asked it to implement a python script for loading the .txt document I store my data in and procesing the reviews. I then ask it to create chunks using fixed-size chunking where we have each student review as one chunk. 
- *What it produced:*
It returned a function named load_file_and_chunk_text that takes the folder_path for the .txt files as a parameter, loads all the .txt documents from the milestone1Doc directory and performs data chunking where it makes each review below the review markers(Review 1, Review 2, etc..) as one chunk. 
- *What I changed or overrode:*
I changed how the chunks are created and returned where I created it as a dictionary containing the professor's name, review number  whih =ch was helpful for uniquely identifying each review, and the source, which contains the filename as that is importnat to use for citing the answers generated by the LLM during the generation stage of the RAG implementation. 

**Instance 2**

- *What I gave the AI:*
I gave ChatGPT my Retrieval Approach section from planning.md, the constants I created to store the values of the embedding model, chomadb name and path, and top-k value for data retrieval, and my pipeline diagram of the RAG implementation. I first asked it to implement a python script containing just the  embedding function named embed_and_store that takes the chunks generated in the data chunking stage with one review as one chunk and uses chromaDB's embedding library with sentence transformers where I pass the constant storing the embedding model name as a function to it to  embedding the chunks created. I then asked it to include a retrieval function named retrieve that will take in a user question and the top-k value, and use the query function used on collection when creating a collection with chromaDB to retrieve the top-k context answers closest in meaning to the user question. I have it use cosine as part of the ranking calculations. 
- *What I changed or overrode:*
I overrode the top-k value to 4, while also changing the constant in config.py for it to that value as well so that I don't retrieve too many chunks or too few chunks as it wil help me get chunks of sufficient context  that are related to a user query. 
