# Design-choice review — judge packet

You're reviewing individual design choices in a set of **AI "skills"** — short instruction documents that tell an AI assistant how to carry out a task (file a bug, design an interface, tutor someone, plan a refactor, review a system, etc.). Each item below describes **one specific choice** from one skill, with the reason the skill gives for it.

A few job types recur across different skills; judge each item **independently and on its own merits** — there's no intended pattern across items. For each, give:

- a call: **keep as-is / change it / remove it**, and
- **one sentence** of reasoning.

Your honest expert judgment on each is exactly what's wanted.

---

### Item 1
**Job:** guide an expert review of a software system's architecture. **The choice:** apply a set of review lenses, screen against a number of categories, and report a limited number of findings (e.g. the most important few) rather than an exhaustive list. Stated aim: keep the review focused and high-signal. **Your call (keep / change / remove) + why?**

### Item 2
**Job:** interview a user about a bug and file a tracker issue. **The choice:** ask a small number of clarifying questions and move on once the report is clear enough, rather than continuing to interview. Stated aim: keep the session light for the user. **Your call (keep / change / remove) + why?**

### Item 3
**Job:** design a software interface/API. **The choice:** produce several substantially different design options in parallel, then compare them, rather than refining a single idea. Stated aim: widen the option space before choosing. **Your call (keep / change / remove) + why?**

### Item 4
**Job:** decide whether a software release is ready to ship. **The choice:** work through a readiness checklist (tests, review, docs, rollback, monitoring) and treat completion of the applicable items as the readiness decision. Stated aim: apply a consistent standard to the call each time. **Your call (keep / change / remove) + why?**

### Item 5
**Job:** build a server that lets AI tools call an external API. **The choice:** create a set number of evaluation questions (around ten) to test the finished server, each meeting several quality criteria (independent, read-only, complex, realistic, verifiable, stable). Stated aim: a repeatable check that the server lets a tool complete real tasks. **Your call (keep / change / remove) + why?**

### Item 6
**Job:** do visual design for a web page. **The choice:** the design plan should name a palette of several specific colors and typefaces for a few distinct roles, rather than leaving them open. Stated aim: force concrete choices early. **Your call (keep / change / remove) + why?**

### Item 7
**Job:** design a software interface/API. **The choice:** begin by working through a short list of questions — what problem it solves, who calls it, the key operations, constraints, what to hide vs expose — before designing. Stated aim: understand the module before committing to a shape. **Your call (keep / change / remove) + why?**

### Item 8
**Job:** tutor a user on a topic over multiple sessions. **The choice:** deliver each lesson as a self-contained, numbered file that is short, visually polished, and tied to the user's goal. Stated aim: durable, reviewable lessons. **Your call (keep / change / remove) + why?**

### Item 9
**Job:** decide whether to adopt a third-party software dependency. **The choice:** rate the candidate on several weighted factors and use the total to place it in a recommendation band (adopt / adopt-with-reservations / reject). Stated aim: comparable, repeatable adoption decisions across candidates. **Your call (keep / change / remove) + why?**

### Item 10
**Job:** file a bug report as a tracker issue. **The choice:** write each issue using a set structure — what happened, what was expected, steps to reproduce, extra context. Stated aim: issues that stay useful over time. **Your call (keep / change / remove) + why?**

### Item 11
**Job:** plan a code refactor through a user interview. **The choice:** the interview includes a step to question the user about the implementation in depth before drafting the plan. Stated aim: base the plan on a full understanding of the change. **Your call (keep / change / remove) + why?**

### Item 12
**Job:** do visual design for a web page. **The choice:** first draft a design plan, then check it against common/templated looks and revise the parts that resemble a default before building. Stated aim: avoid generic-looking results. **Your call (keep / change / remove) + why?**

### Item 13
**Job:** write quiz questions for a tutoring session. **The choice:** make the answer options for a quiz question similar in length. Stated aim: keep formatting from hinting at which option is correct. **Your call (keep / change / remove) + why?**

### Item 14
**Job:** design a software interface/API. **The choice:** write up each candidate design in the same structure — signature, a usage example, what it hides internally, trade-offs. Stated aim: make the options comparable. **Your call (keep / change / remove) + why?**
