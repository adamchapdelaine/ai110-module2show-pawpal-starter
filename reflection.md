# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design, prior to any interaction with AI, is shown below:

Owner:

    Attributes:

        owner name
        owner information

Pet:

    Attributes:
        pet name
        pet information 

Tasks:

    Attributes:
        task name
        task category
        duration
        priority

    Methods:
        add task
        edit task
        remove task

Scheduler:

    Attributes:
        scheduled tasks

    Methods:
        schedule a task (a walk, feeding, meds, etc)
        see today's tasks


**b. Design changes**

- Did your design change during implementation?

    Yes, significantly.

- If yes, describe at least one change and why you made it.

    Due to the extent of changes made, I'll describe three of the changes I made. 

    Firstly, I moved add_task and remove_task from Task to Pet because a task shouldn't create or delete itself, and the Pet class owns the task list.

    Secondly, I changed Owner to Pet cardinality from 1..* to 0..* because it would allow an owner to exist in the system before any pet is added. Owner information should be entered before pets are added, so having a minimum of one pet be a prerequisite for there to be an owner doesn't make sense.

    Thirdly, I added a new class called ScheduledItem because the Scheduler class needs somewhere to put its output, and tasks should be assigned to a time slot without being changed.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

    In my Scheduler class, the schedule_task function ignores each task's due_time and packs tasks back to back by priority. This prevents overlaps, but tasks may not run at the exact time the user requested.

- Why is that tradeoff reasonable for this scenario?
    The tradeoff is reasonable for this scenario because it ensures a usable, conflict-free plan with minimal code where the schedule is generated based on priority. It doesn't account for some activities that are very time-sensitive though, like medical ones, so in a different scenario it might be better to have tasks marked as fixed-time and others marked as flexible.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

    I used AI for design brainstorming, debugging, and refactoring. At the moment, I lack confidence in designing UML diagrams and struggled with some syntactical aspects of writing the code, so I leaned on AI to review my attempts and make suggestions. I accepted suggestions based on whether they made logical sense and fleshed out what I already had rather than invent logic on my behalf, I made it a point to struggle for 20-30 minutes on a problem before asking AI for help on steps where AI use was optional.

- What kinds of prompts or questions were most helpful?

    Here are two examples of prompts I used that I found particularly helpful:

    ```
     I'm being asked to create a new file named main.py, meant to test my logic and if it works in the terminal. I'm supposed to import my classes from pawpal_system.py, create an Owner and at least two Pets, add at least three Tasks with different times to those pets, and prints a "Today's Schedule to the terminal."

    I don't want you to write any code for me, just give me some hints to help bridge the gap between the pseudocode I have and what I'm supposed to write.
    ```

    ```
     I made some changes in uml.mmd. Review them. Ignore the code in pawpal_system.py. Explain how I can implement the changes I made, if any I attempted were done improperly.
    ```

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

    One moment where I did not accept an AI suggestion as-is was when it decided to add the class ScheduledItem when fleshing out the skeleton code I had in test_pawpal.py. I eventually went through with the change, but I had to verify it first.

- How did you evaluate or verify what the AI suggested?

    I verified what the AI suggested by drilling it with questions about why the change was added, what it's meant to do, and if it's worth adding. After reading the explanations the AI provided, I then used my best judgement at the time to decide whether or not I wanted to keep the change.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
