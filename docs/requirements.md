# COMP639 Studio Project – Semester 1 2025

# Group Software Development Project 2

# Premium Online Travel Journal

**Worth: 55 %**

**Reports/Presentation Due Dates**

Project Planning Report: Sunday 11 th May 2025, 11:59 PM

Presentation and Demo: Thursday 12 th June or Friday 13th June 2025
_(presentation schedule TBA)_

Individual Timesheets, End of Project Report,
and Peer Evaluations: Sunday 15 th June 2025, 11:59 PM

### P ROJECT D ESCRIP TION

In this project, you will build upon your Online Travel Journal web app from Group Project 1 to develop a more
fully-featured travel journal and blogging platform. All users will still have access to the free features they’re used
to, while a range of premium features will be added to draw in paid subscribers.

Your team’s primary goal in this project is to develop a high-quality web application that meets as many of the
client’s requirements as possible. To achieve this you will need to:

- Apply the methods and tools you learnt about during Group Project 1.
- Analyse high-level client requirements in this document to extract user stories and acceptance criteria.
- Evaluate technical solutions available to address those requirements within any specified constraints.
- Design and build a software solution together as a team.

### IM P ORTANT

This is a **group** assessment. Your group must not collaborate or confer with other groups. You may help
other groups by verbally explaining concepts and making suggestions in general terms, but without
directly showing or sharing your group’s code. You must develop the logical structure, the detail of your
code and the database within your group, even if you are working alongside other groups. Code that is
copied or shares a similar logic to other groups will receive zero marks for both groups.

The use of Artificial Intelligence (AI) tools, such as ChatGPT, to complete this assessment is **prohibited**.
You **must not** use AI to generate source code, database scripts, your project planning report, end of
project report, any part of your final presentation, or any other deliverable submitted for marking.
Assessment answers will be analysed for evidence of the use of AI and penalties may be administered.

The **only allowed use of AI** is for the generation of test data (e.g. user profiles, journey details, entries,
and/or images). Any use of AI to generate test data **must be declared** in your end of project report.

The University policy on Academic Integrity can be found here.


### SCENAR IO

The free Online Travel Journal app you developed in Group Project 1 has proven wildly successful, drawing in a
large number of users. This has enabled your client to secure investors’ funding for additional development, with
the aim of turning the app into a commercially successful product.

In Group Project 2, your team will expand your existing Online Travel Journal with a paid subscription model, and
implement a range of new free and premium features. Many of these new features are intended to enhance the
most popular functions of the site: sharing journeys, and engaging with journeys others have shared.

Your new web app should include **all the features required for Group Project 1**.**.** This means **you must implement
any user stories you did not implement during the first project**. You may reuse any of your own previous work
from Group Project 1, and from any of your group members’ individual assignments.

### REQUIREM ENTS

#### R E S P O N S I V E D E S I GN

Ensure that your web app adapts to different devices and screen sizes.

- Analytics have shown that most travellers use smartphones when updating their own journeys and
    reading other users’ shared journeys.
- Editors and Admins use PCs with widescreen monitors while working in the office. However, staff often
    use their own personal smartphones or tablets to edit journeys, ban or un-ban users, change user roles,
    and perform other administrative tasks while out of the office.
- By regularly deploying your app to PythonAnywhere during development, your team can use your own
    mobile devices for testing.
- You can also emulate various smartphone and tablet screen sizes using the “Responsive Design Mode” in
    Mozilla Firefox, or the “Device toolbar” (under “Developer tools”) in Google Chrome.

#### E P I C S

The requirements for this project are defined by eight “Epics”. Each of these represents a collection of related user
stories, which your group needs to identify and write. There are eight epics: one required, and seven optional.

**Your group must complete the required epic, and a minimum of two optional epics.** To achieve a high grade:

- A group of 5 members should aim to complete at least 4-5 optional epics to a high standard
    (i.e. implement all required and suggested functionality, with high levels of quality and usability).
- A group of 4 members should aim to complete at least 3-4 optional epics to a high standard.
- A group of 3 members should aim to complete at least 2-3 optional epics to a high standard.

These are only guidelines. **Marks will not be directly awarded based on the number of epics completed** : the
quality and level of functionality for each epic are very important.

**You must start with the required epic, “Premium Features”.** After that, your group may choose which epics to
complete and in what order. Your project planning report must include an initial plan for which epics your group


will address in each sprint. You may change this later. Before beginning an epic, you will need to work out all user
stories and acceptance criteria for that epic, then work through them with your product owner.

You may only start an epic during a product owner meeting, with the agreement of your product owner. Think
about what happens if your product owner says your user stories for that epic need work before you begin. You
can reduce that risk by working ahead, and making sure to have the user stories for at least a couple of epics
planned out whenever you’re proposing to begin a new one.

Many epics require substantial changes to the core product. To avoid major merge conflicts, it may be a good idea
to complete all user stories from one epic before moving on to the next.

When choosing an epic, think about the technical skills required. Some epics can be completed with the skills you
have now, while others may require some independent learning. If you decide to attempt an epic that requires
your group to develop new skills, consider planning that from the beginning of the project. Even if you change your
mind later, it helps to start with a general plan as to what epics you’re going to attempt and in what order.

#### R E Q U I R E D E P I C : P R E M I U M F E A T U R E S

Add a subscription option to your web app, which allows a **Traveller** to pay for access to premium features for One
Month, One Quarter, or One Year. **You must offer the subscription options and prices listed in Table 1.** Only
**Travellers** should be able to purchase subscriptions: staff users such as **Editors** and **Admins** should have access to
all premium features without the need for a paid subscription.

Subscriptions must work as a “prepay” service: **do not offer auto-renewal, or automatic billing**. Your client’s
marketing strategy is based around a “no commitments” concept for budget-conscious Travellers, where they can
“top up” their account by purchasing a new subscription whenever they want. Purchasing a subscription must add
the associated number of months to a Traveller’s account: e.g. if a Traveller has two months remaining, then
purchases a One Year subscription (+12 months), they should now have a total of 14 months remaining.

When a Traveller’s subscription is nearing its end, they should see a notification or reminder while using the site.

Travellers must also be able to choose a “Free Trial” option to receive a one-month subscription without providing
credit card details or making a payment. Each Traveller’s account must only be eligible for **one free trial**. Even if a
Traveller’s account is set to another role (e.g. Editor or Admin) then set back to a Traveller later, they should not be
eligible for another free trial if they’ve ever had one before.

**Table 1 : All paid subscription options your Online Travel Journal must support as part of the Premium Features epic.**

Payments made with a New Zealand billing address must be charged 15% GST (“Price including GST” in Table 1 ).
Payments made from any other country must **not** be charged GST (“Price excluding GST” in Table 1 ). This must be
based on the billing address for the payment (see below), **not** the home location specified in the user’s profile.

```
Subscription Length (Months) Discount Price excluding GST Price including GST
Free Trial + 1 - - -
One Month + 1 - NZ $5.22 NZ $6.
One Quarter + 3 10% NZ $14.09 NZ $16.
One Year + 12 25% NZ $46.96 NZ $54.
```

Purchases must be made using a simulated payment gateway: i.e. create a page where users can enter a fictional
credit card number (e.g. "0000- 0000 - 0000 - 0000"), expiry date (e.g. "01/2025"), CVV (e.g. "000"), and billing
address (with country selected from a list) to make a simulated payment. For the purpose of this project, **we will
not be implementing a real payment system**.

**Travellers** must be able to see their current subscription status (“Free”, “Trial”, or “Premium”) and the date their
subscription or trial (if any) is due to expire. **All logged-in users** , including **Travellers** , **Editors** , **Admins** , and any
other roles, must be able to view a history of all subscription payments they have made. Although staff users
cannot purchase new subscriptions, they may have paid to subscribe with their original Traveller account and still
need access to those records. Users should also be able to view a receipt for any previous subscription payment.
For payments made from New Zealand billing addresses, the receipt should indicate how much GST was charged.

**Admin** users must be able to give any **Traveller** a free subscription of +1, +3, or +12 months. They may do this for a
number of business reasons such as attracting popular travel bloggers to the site, rewarding users who generate
high-quality content, or giving users a credit if they’ve had a bad experience. These free subscriptions should show
up in a user’s subscription history, but without the option to view or download a receipt. Admin users must also be
able to view the complete subscription history, including all receipts, for any user of the site.

There are three main **Premium Features** that you must implement.

1. **Published Journeys:** Paid subscribers and staff can now choose a third option for the visibility of their
    journeys: Private, Public, or **Published**. Published journeys appear on the homepage of the site, and are
    visible to **anyone** : including visitors who aren’t logged in. _If a Traveller’s subscription expires, any_
    _Published journeys should remain “Published“ but only be visible to logged-in users (i.e. the same as the_
    _original “Public” setting) until the subscription is renewed._
2. **Multiple Images:** Paid subscribers and staff can now add **multiple images per event**. _If a Traveller’s_
    _subscription expires, they will still be able to see all the images they’ve previously added to each of their_
    _events. However, they will no longer be able to add images to an event that already has one or more_
    _images attached. For events in shared journeys, only the first image for each event will be visible to other_
    _users until the journey’s owner renews their subscription._
3. **Journey Cover Images** : Paid subscribers and staff can choose a “cover image” for a journey, which shows
    up as the journey’s header and icon/thumbnail. _If a Traveller’s subscription expires, any existing cover_
    _images will remain but there will be no option to add new ones: only an option to remove them._

These features will only be available to **Travellers** who have a current subscription. All **Editors** , **Admins** , and any
other staff roles should also have access to these premium features. Several of the optional epics below also
include premium features, which are **highlighted like this**. Details of how premium features should work when a
Traveller’s subscription expires (or a staff user is made back into a Traveller) are _shown in grey like this_.

You may need to make other adjustments to the requirements of Group Project 1 to suit the subscription model
and premium features described here, or to implement your group’s chosen epics. This should be done in
consultation with your product owner.

#### O P TI O N A L E P I C : C O M M U N I T Y F E A T U R E S

One of your client’s original aims was to build a strong community around the app. This has proven successful, but
much of that community activity takes place off-site on social media platforms. We need to shift that activity into


our own web app, keeping users engaged with the site. Enhance your app by giving any logged-in user the ability
to **“Like” or post comments on shared Events**.

Paid subscribers and staff should also be able to exchange **private messages** with other users (free, premium, and
staff). Travellers without a subscription can see and delete any messages they receive, but must subscribe to reply.

Let any logged-in user **Like or Dislike a comment** , and show the number of likes and dislikes alongside each one.
Also allow users to report a comment as abusive, offensive, or “spam”, and give Editors and Admins the ability to
review and optionally hide these comments. Create a new **Moderator** staff role that has the ability to review and
hide comments, but doesn’t have the extra rights of an Editor (e.g. they can’t edit shared journeys). Moderators
should also be able to report a comment to the Admin team if they think further action is necessary, such as a ban.

To support these community features, create a public user listing that any logged-in user (including Travellers) can
search through. Consider what user details should be public and what should stay private (i.e. only visible to the
user themselves, and staff roles such as Editors and Admins). This would be a good thing to discuss with your
product owner. Let users choose whether their accounts are visible or hidden from the public listing.

Consider expanding the user profile system to give users greater ability to express themselves through their
profiles. This doesn’t just mean adding more text fields: think about what users might want to share and display.
You might want to show a user’s recent likes and comments, journey updates, places they’ve been, etc.

#### O P TI O N A L E P I C : GA M I F I C A T I O N

Add game-like elements to encourage Travellers to engage more actively with the site. This should include a
system of “achievements” that can be earned by users and displayed on their public profile for other users to see.
This fits together nicely with the public user listing of the _Community Features_ epic.

Users might earn an achievement for creating their first journey, another for adding their first event, another for
sharing a journey publicly, etc. There could be an achievement for visiting more than 50 different locations overall,
having a journey that lasts more than 30 days, or being the first user to view a newly shared journey.

Include **some achievements only premium users can get**. For example, you could have an achievement for the
first journey a user **Publishes** on the homepage, or for adding a **Cover Image** to five journeys.

Implement a way for users to track which achievements they’ve unlocked, and which are still to be unlocked. For
achievements based on progress, like number of locations visited, find a way to make that progress visible to users.
Find other ways to encourage participation: for example, creating a public leader-board of users who’ve earned
the most achievements, and/or a list of users who’ve recently been awarded new achievements.

Think about achievements associated with other epics your group has chosen to implement: for example,
achievements for receiving a certain number of likes or comments on an event ( _Community Features_ epic), or
personalising your journal with a custom theme ( _Custom Themes_ epic).

#### O P TI O N A L E P I C : D E P A R TU R E B O A R D

During the initial trial of your free Online Travel Journal web app, many users signed up just to follow high-quality
journeys shared by popular users of the site. The **Departure Board** is an exclusive premium feature targeted at
those users, making it easier to follow their favourite journeys and to discover new ones.


Paid subscribers and staff users should be able to **Follow any shared journey**. Recent events from every journey
they follow should appear on their “Departure Board”: a personalised news feed, ordered by most recently
updated event first. Remember that events from many journeys will be shown together, like posts on a social
media feed, so each event will need to clearly identify the journey and user it belongs to.

Paid subscribers and staff should also be able to **Follow any user who has shared a journey**. This means events
from any of that user’s shared journeys will also appear on the Departure Board. This would work well together
with the public user listing and profiles from the _Community Features_ epic.

Finally, paid subscribers and staff should be able to **Follow a location**. Any shared journey events occurring at that
location should appear on the Departure Board, regardless of what user or journey they belong to.

Each item on a user’s Departure Board should clearly indicate why it’s there: is the user currently following that
particular journey, and/or the user who owns it, and/or that location? If not, give them the option to start
following right there and then. Make sure you also give users a quick and easy way to see the journeys, users, and
locations they’re currently following, and to un-follow them if they wish.

_If a Traveller’s subscription expires, they should lose access to their Departure Board. However, if they renew their
subscription, their Departure Board should remember all of the journeys, users, and locations they used to follow._

#### O P TI O N A L E P I C : A D V A N C E D E D I TI N G

Employing professional editors to polish and moderate shared journeys has generally been successful, and given
the site a reputation for hosting high-quality content. However, some users and staff have expressed concern that
this may result in overreach or censorship by editors. Implement additional features to make the editing process
more transparent, and to provide paid subscribers and staff with additional control over their content.

All changes made to a shared journey by an Editor, Admin, or other staff user must now be logged by the system.
This includes changes to journey or event text, event locations, or event images. Editors and Admins must now
provide a reason when making an edit (e.g. “Fixed typos” or “Removed copyrighted image due to DMCA takedown
notice”). The owner of a journey should receive a notification whenever an edit is made by an Editor or Admin,
clearly indicating what was changed and why.

Paid subscribers should be able to view the **Complete Edit History** , including the date and time, changes made, and
reason given for any edits made by staff users to any of their shared journeys and events.

Paid subscribers and staff should also be able to set a **“No Edits” flag** on their journeys, which should prevent
Editors or Admins from making any changes to the text or images of that journey if shared. However, Editors or
Admins must still be able to hide the entire journey in the event that objectionable content is reported or found. _If
a Traveller’s subscription expires, any No Edits flags they previously set should still apply. However, that Traveller
should no longer be able to turn the feature on or off until they renew their subscription._

All users should be able to appeal a hidden journey, a block from sharing journeys in general, or an overall ban
from the site. All appeals should be sent to a queue monitored by Editors and Admins, who may then choose to
remove the restriction or reply with an explanation of why it will be upheld.


**Hint:** If you have also chosen to implement the _Helpdesk_ epic, it might make sense to combine the appeals system
with the Helpdesk system in some way (e.g. processing appeals as a special type of helpdesk request). However,
you may also choose to implement either or both epics separately.

#### O P TI O NAL E P I C : H E L P D E S K

Sometimes users need help renewing their subscription, uploading an image, or trying to understand why their
images keep getting removed by Editors. Other times, our users find bugs we didn't even know existed. Create an
integrated Helpdesk system that allows staff to support users in all of these situations.

Give all users the ability to request help or report a bug. These requests should go into a queue that's only
accessible to Editors, Admins, and a new **Support Tech** staff role. A Support Tech has almost the same rights as an
Admin user: they can do everything an Editor can do, plus search for users, view their profiles, ban or un-ban users,
and view users’ subscription histories. However, **a Support Tech must not be able to change users’ roles**. Think
about what other rights a Support Tech might need, based on the other epics you have decided to implement.

Requests should start in "New" status, not assigned to anyone. Admins, Editors, and Support Techs can "Take" a
request, making them its owner, or assign it to any other Admin, Editor, or Support Tech. They can also "Drop" a
request, putting it back into the queue so that another user with more time or relevant experience can take it. The
current owner of a request can reply to the user who made that request. They can also set the request’s status to
"Open" (work in progress), “Stalled” (unable to be progressed at this time), or "Resolved". Once opened, a request
cannot be set back to “New”. Users can see all of the requests they have made, past and present, and can add
their own replies to a New, Open, or Stalled request, but can't add anything to a "Resolved" one.

**Premium Service:** Requests from paid subscribers or staff accounts should be clearly identified in the support
queue, so those requests can be prioritised by support staff.

#### O P TI O N A L E P I C : C U S TO M TH E M E S

Since the launch of your initial free Online Travel Journal, your client has been trying to attract well-known travel
bloggers to the site. However, many of those bloggers prefer to remain on other platforms such as WordPress or
Wix due to the control that gives them over how their journal is styled and presented. **Custom Themes** give paid
subscribers and staff the ability to customize the look and feel of their travel journal, including colours, background
images, layouts, and other visual design elements.

A custom theme should apply to all pages associated with a user’s journal—their list of journeys, journey and
event detail pages, etc. Customisations must also be visible to anyone viewing a shared journey, event, or public
user profile ( _Community Features_ epic). _If a Traveller’s subscription expires, their custom theme should still be
saved but should no longer be displayed (to them or to anyone else) until their subscription is renewed._

Customising a journal’s visual theme shouldn't require any knowledge of HTML or CSS. A user should be able to
select colours, upload images, or choose other design options through an intuitive user interface. Think about
allowing users to preview a design before applying it, or to roll back to a previous design if they make a mistake.

Not everyone is a designer. Consider providing a gallery of pre-made themes that Competition Admins can choose
from. If you do this, however, make sure you still allow a fully "custom" option for users who want more control
than selecting a pre-made theme.


**Hint:** Not sure how to implement this? Remember that Jinja isn’t just for generating HTML. You can use Jinja

### templates to dynamically generate CSS, either inline on your HTML pages within <style> tags or as standalone

CSS files that you refer to. Think about how you could use this approach to apply different styles to a page
depending on which competition you’re currently viewing. To avoid creating overly complex dynamic style sheets,
you might want to take a look at CSS Variables (https://www.w3schools.com/css/css3_variables.asp).

#### O P TI O N A L E P I C : L O C A TI O N F E A T U R E S

Travel is all about geography. Add location-based features that offer new ways for users to document their own
journeys and engage with the journeys shared by others.

Allow users to specify the location of an event on a map. Users should still be able to give each location a name.
For example, a user could select the Lincoln University campus on a map and name it “Lincoln University”. The
name and coordinates should be stored together, so that they or another user could later select “Lincoln
University” and re-use the same coordinates for another event. Either include a map showing the location when
displaying each event, or show the location in text and allow users to open a map view.

Display an overall map for each journey with clickable pop-ups or links for each event. Ideally, show lines between
each event and the next one in sequence (e.g. a trip from Wellington to attend the COMP639 Studio Project
Workshop might show a marker at Wellington airport, connected by a line to Christchurch Airport, connected by a
line to Lincoln University). Consider adding an optional “Destination” location for events such as flights. Then,
instead of creating two events (9“Departed Wellington Airport” and “Arrived at Christchurch Airport”), a user
could create a single “Flight from Wellington to Christchurch” with Location: Wellington Airport and Destination:
Christchurch Airport.

Consider also showing all of a user’s journeys together on a single map. You could do something similar for their
public user profile, as part of the _Community Features_ epic, showing only their publicly shared journeys. If you’re
implementing the _Departure Board_ epic, you could include another map in that view showing recent events from
all the journeys, users, and locations a user is following.

**Note:** Only use free frameworks to add location features. Do not use frameworks that require commercial API
keys. Make sure whatever you use works with PythonAnywhere. We strongly recommend using OpenStreetMap
with the open-source JavaScript library Leaflet. A good tutorial for using Leaflet with Flask is available at
https://medium.com/geekculture/how-to-make-a-web-map-with-pythons-flask-and-leaflet-9318c73c67c

### P ROJECT REQUIREM EN TS

Your group will need to produce the same set of deliverables that you did for Group Project 1, including a **Project
Planning Report** , **Presentation/Demonstration** , **Web App** on PythonAnywhere, **Source Code** on GitHub, and **End
of Project Report**. Individually, you will need to submit a **Timesheet** and **Peer Evaluation**.

1. TE C H N O L O GY S TA C K

- Use Python & Flask, JavaScript, and MySQL.
- Do not use SQLAlchemy, ReactJS, or similar technologies.


- You may use Bootstrap CSS, free Bootstrap themes, free alternatives to Bootstrap CSS, or your own
    custom CSS. **If you use an existing Bootstrap theme, or an alternative to Bootstrap, you must declare**
    **this in your end of project report**. If you do not declare this, it may be detected as plagiarism.

#### 2. GI TH U B R E P O S I T O R Y

- Your group has been allocated a **new Repository on GitHub for Project 2** which you must use.

### o Add a README file that clearly explains what a system administrator would need to know in

```
order to deploy and run your web app on their own server. Provide a clear set of steps, specific
to your web app: do not copy the README from the Login Example.
```
### o Ensure your repository has a .gitignore file to exclude the virtual environment.

- Include the following in your repository:
    o All Python, HTML, image files, and any other necessary files for the web app.

### o A requirements.txt file listing all required pip packages.

```
o Two MySQL scripts: one for database creation and one for record population.
```
- **DO NOT make any changes to your Project 1 repository.** If you are building on your Project 1 code,
    download a copy and check it in to your new Project 2 repository.

#### 3. H O S TI N G O N P Y TH O N A N YW H E R E

- Host your system, including the database, on PythonAnywhere.
- Add “lincolnmac” as your “teacher” via the site configuration.
- **DO NOT make any changes to your Project 1 PythonAnywhere site.** Create a new PythonAnywhere
    account for this project. Multiple accounts can be created using the same email address.

#### 4. S U B M I S S I O N

- Your End of Report must include URL and username/password details.

## IMPORTANT : Do NOT make any changes to your app on GitHub or PythonAnywhere after the

## submission date until your marks have been released. Any changes will be considered the same

## as a late submission and may be penalised with a late penalty of up to 100% of your mark.

#### 5. S C R U M

- Your group will adhere to Scrum Methodology. This includes hosting daily scrum meetings, project
    planning sessions, retrospectives, and a weekly Sprint Review Meeting with the Product Owner.
- The role of Scrum Master should rotate among team members. **Make sure that group members who**
    **didn’t serve as Scrum Master during Group Project 1 take the role at some point during Group Project 2.**

#### 6. U S E R S T O R I E S

- Before meeting with your product owner at the start of Sprint 1, you will need to have written the **User**
    **Stories for Epic 1** and **User Stories for the first two optional epics** that your team plans to complete.
- You will need to present these user stories, along with **Estimates in Story Points** and **Acceptance Criteria** , in
    your project planning report.


- User stories for the remaining epics may be written at any time during the project, but must be completed
    (with acceptance criteria and estimates) before you meet with your product owner to begin that epic.
       o For example, if you are planning to begin the “Gamification” epic during Sprint 4 , your group should
          have written the user stories for that epic, complete with estimates and acceptance criteria, before
          meeting with your product owner to plan that sprint.

#### 7. J I R A S C R U M B O A R D

- Set up a **new** group Jira Scrum Board following the instructions provided in the workshop. _It's crucial to use the_
    _correct account type to avoid access issues._
- Add user stories, acceptance criteria, priorities, and estimates in story points to the Jira board.
- Use the Jira board to track your progress throughout the project: don’t just update the board each week, but
    keep it updated in “real time” as you work to complete user stories.

### M ARKING CRITERI A

Your group’s combined mark is based on the components below. Your individual mark will then be adjusted based
on your **individual contribution to the project**. We determine your individual contribution through your self and
peer evaluation forms and examiner feedback. We may also look at your individual timesheets, individual GitHub
contributions, and other project artefacts if your individual contribution is unclear.

```
Component Mark (%)
```
```
Reports
```
```
Project Planning Report
(Note: planning report marks are not adjusted by individual contribution.
All group members will receive the same score.)
```
#### 10%

```
End of Project Report 20%
```
```
Presentation
```
```
Slideshow Presentation
(content, quality, presentation skills, and Q&A) 20%^
Live Software Demonstration
(quality of the final product, user interface) 10%^
```
```
Final Product
```
```
Source Code
(reviewed in GitHub) 20%^
Functionality
(tested live on PythonAnywhere) 20%^
Total 100%
```
## IMPORTANT: As with Group Project 1, your web app’s functionality will be assessed on your

## team’s PythonAnywhere site and the source code will be viewed on GitHub. If your project

## does not run on PythonAnywhere, you will not receive marks for functionality.


