# Djangoproject - Contrib

**Pages:** 16

---

## Accessibility | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/internals/contributing/accessibility/

**Contents:**
- Accessibility¶
- Accessibility standards¶
- Support targets and testing¶
  - Testing baseline¶
  - Recommended assistive technologies¶
- Known issues and how to help¶

The Django project is committed to ensuring that websites built with Django are usable by everyone, including people with disabilities. Django’s built-in components, such as the admin interface and default form rendering, should adhere to established accessibility standards and meet our own targets for supporting specific input devices and assistive technologies.

We work to conform with the Web Content Accessibility Guidelines (WCAG), version 2.2, at the AA level. WCAG is the most established standard for web accessibility. AA-level guidelines are the most common legal compliance target worldwide.

We also aim to follow other best practices, such as:

WCAG 2.2 AAA-level guidelines – stricter criteria that go beyond the AA level.

The upcoming WCAG 3.0 guidelines – a new, evolving standard that aims to unify and improve upon previous versions of WCAG.

Authoring Tool Accessibility Guidelines (ATAG) 2.0 – guidelines for software and services that are used to produce web content.

To learn more about accessibility without diving straight into standards, we recommend The A11Y Project, a community-driven effort to make digital accessibility easier.

Beyond standards, we want to make sure Django actually works for people using a wide range of input devices and assistive technologies. This has benefits to make sure Django works better for everyone. The best way to do this effectively is to take accessibility considerations into account as part of designing features. If in doubt, consult with users who rely on assistive technologies or with accessibility experts. You can reach out to the Accessibility team via the Accessibility Django forum topic or via the #accessibility channel on the Django Discord server.

Design the UI with accessibility in mind, and the testing will only be needed as a final check. For more complex interfaces, confer with other contributors to decide on testing targets. Reach out to the Accessibility team for support and to coordinate testing.

Always test user interface changes with:

Keyboard-only navigation. Common issues include:

An interactive element can’t be reached using the Tab or arrow keys.

An interactive element “traps” input focus and prevents navigating away.

An interactive element doesn’t give a visible indication when it has input focus.

The focus order is inconsistent with the logical order that’s communicated visually.

The Accessibility Insights browser extension’s automated checks feature, or an equivalent tool with the Axe checker.

Where the UI changes could affect those modalities, also test with:

Touch-only navigation. Common issues include:

A touch target (interactive element) is too small.

Hover-based based interaction which does not translate to touch, such as a hover only tooltip.

400% browser zoom. Common issues include:

Content is cut off or disappears when zoomed.

Content that does not inherently require a two-dimensional layout causes scrolling in both directions (vertical and horizontal). Two-dimensional scrolling is acceptable for content like images, maps, videos, and data tables, which require both dimensions to be usable.

Forced-colors mode (for example Windows Contrast Themes). Note that this can be tested via the "high_contrast" mode in the screenshot tests. Common issues include:

Over-reliance on color for meaning, which is lost in forced-colors mode.

Use of !important or inline styles may break forced-colors mode.

Where the UI changes could affect assistive technologies, here are popular free options we recommend testing with.

NVDA - recommended with Firefox ESR

Narrator - recommended with Microsoft Edge

Windows Speech Recognition

VoiceOver - recommended with Safari

Orca - recommended with Firefox ESR

For mobile or tablet:

VoiceOver on iOS, or TalkBack on Android

The following are popular licensed options. If you are a user of these, or can work with a user holding a license, also test against:

There are parts of Django that do not meet our accessibility targets. We actively work on fixing issues, both as part of ongoing maintenance and bigger overhauls. To learn about known issues, and get involved, see:

#accessibility on the Django Discord server.

The Accessibility Django forum topic.

Accessibility issues on the ticket tracker.

Our django accessibility improvements project board.

The Accessibility team.

---

## Advice for new contributors | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/internals/contributing/new-contributors/

**Contents:**
- Advice for new contributors¶
- First steps¶
  - Triage tickets¶
  - Review patches of accepted tickets¶
  - Keep old patches up-to-date¶
  - Write some documentation¶
  - Sign the Contributor License Agreement¶
- Guidelines¶
  - Pick a subject area¶
  - Analyze tickets’ context and history¶

New contributor and not sure what to do? Want to help but just don’t know how to get started? This is the section for you.

If you are new to contributing to Django, the Writing your first contribution for Django tutorial will give you an introduction to the tools and the workflow.

This page contains more general advice on ways you can contribute to Django, and how to approach that.

If you are looking for a reference on the details of making code contributions, see the Contributing code documentation.

Start with these steps to discover Django’s development process.

If an unreviewed ticket reports a bug, try and reproduce it. If you can reproduce it and it seems valid, make a note that you confirmed the bug and accept the ticket. Make sure the ticket is filed under the correct component area. Consider writing a patch that adds a test for the bug’s behavior, even if you don’t fix the bug itself. See more at How can I help with development?.

This will help you build familiarity with the codebase and processes. Mark the appropriate flags if a patch needs docs or tests. Look through the changes a patch makes, and keep an eye out for syntax that is incompatible with older but still supported versions of Python. Run the tests and make sure they pass. Where possible and relevant, try them out on a database other than SQLite. Leave comments and feedback!

Oftentimes the codebase will change between a patch being submitted and the time it gets reviewed. Make sure it still applies cleanly and functions as expected. Updating a patch is both useful and important! See more on Contribution checklist.

Django’s documentation is great but it can always be improved. Did you find a typo? Do you think that something should be clarified? Go ahead and suggest a documentation patch! See also the guide on Writing documentation.

The reports page contains links to many useful Trac queries, including several that are useful for triaging tickets and reviewing patches as suggested above.

The code that you write belongs to you or your employer. If your contribution is more than one or two lines of code, you have the option to sign the CLA. See the Contributor License Agreement FAQ for a more thorough explanation.

As a newcomer on a large project, it’s easy to experience frustration. Here’s some advice to make your work on Django more useful and rewarding.

This should be something that you care about, that you are familiar with or that you want to learn about. You don’t already have to be an expert on the area you want to work on; you become an expert through your ongoing contributions to the code.

Trac isn’t an absolute; the context is just as important as the words. When reading Trac, you need to take into account who says things, and when they were said. Support for an idea two years ago doesn’t necessarily mean that the idea will still have support. You also need to pay attention to who hasn’t spoken – for example, if an experienced contributor hasn’t been recently involved in a discussion, then a ticket may not have the support required to get into Django.

It’s easier to get feedback on a little issue than on a big one. See the easy pickings.

This means getting someone else to confirm that a bug is real before you fix the issue, and ensuring that there’s consensus on a proposed feature before you go implementing it.

Sometimes it can be scary to put your opinion out to the world and say “this ticket is correct” or “this patch needs work”, but it’s the only way the project moves forward. The contributions of the broad Django community ultimately have a much greater impact than that of any one person. We can’t do it without you!

If you’re really not certain if a ticket is ready, don’t mark it as such. Leave a comment instead, letting others know your thoughts. If you’re mostly certain, but not completely certain, you might also try asking on the #contributing-getting-started channel in the Django Discord server to see if someone else can confirm your suspicions.

Focus on one or two tickets, see them through from start to finish, and repeat. The shotgun approach of taking on lots of tickets and letting some fall by the wayside ends up doing more harm than good.

When we say “PEP 8, and must have docs and tests”, we mean it. If a patch doesn’t have docs and tests, there had better be a good reason. Arguments like “I couldn’t find any existing tests of this feature” don’t carry much weight. While it may be true, that means you have the extra-important job of writing the very first tests for that feature, not that you get a pass from writing tests altogether.

It’s not always easy for your ticket or your patch to be reviewed quickly. This isn’t personal. There are a lot of tickets and pull requests to get through.

Keeping your patch up to date is important. Review the ticket on Trac to ensure that the Needs tests, Needs documentation, and Patch needs improvement flags are unchecked once you’ve addressed all review comments.

Remember that Django has an eight-month release cycle, so there’s plenty of time for your patch to be reviewed.

Finally, a well-timed reminder can help. See contributing code FAQ for ideas here.

---

## Coding style | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/internals/contributing/writing-code/coding-style/

**Contents:**
- Coding style¶
- Pre-commit checks¶
- Python style¶
- Imports¶
- Template style¶
- View style¶
- Model style¶
- Use of django.conf.settings¶
- Miscellaneous¶
- JavaScript style¶

Please follow these coding standards when writing code for inclusion in Django.

pre-commit is a framework for managing pre-commit hooks. These hooks help to identify simple issues before committing code for review. By checking for these issues before code review it allows the reviewer to focus on the change itself, and it can also help to reduce the number of CI runs.

To use the tool, first install pre-commit and then the git hooks:

On the first commit pre-commit will install the hooks, these are installed in their own environments and will take a short while to install on the first run. Subsequent checks will be significantly faster. If an error is found an appropriate error message will be displayed. If the error was with black or isort then the tool will go ahead and fix them for you. Review the changes and re-stage for commit if you are happy with them.

All files should be formatted using the black auto-formatter. This will be run by pre-commit if that is configured.

The project repository includes an .editorconfig file. We recommend using a text editor with EditorConfig support to avoid indentation and whitespace issues. The Python files use 4 spaces for indentation and the HTML files use 2 spaces.

Unless otherwise specified, follow PEP 8.

Use flake8 to check for problems in this area. Note that our .flake8 file excludes some errors that we don’t consider as gross violations. Remember that PEP 8 is only a guide, so respect the style of the surrounding code as a primary goal.

An exception to PEP 8 is our rules on line lengths. We allow up to 88 characters in code, as this is the line length used by black. Documentation, comments, and docstrings should be wrapped at 79 characters. These limits are checked when flake8 is run.

String variable interpolation may use %-formatting, f-strings, or str.format() as appropriate, with the goal of maximizing code readability.

Final judgments of readability are left to the Merger’s discretion. As a guide, f-strings should use only plain variable and property access, with prior local variable assignment for more complex cases:

f-strings should not be used for any string that may require translation, including error and logging messages. In general format() is more verbose, so the other formatting methods are preferred.

Don’t waste time doing unrelated refactoring of existing code to adjust the formatting method.

Avoid use of “we” in comments, e.g. “Loop over” rather than “We loop over”.

Use underscores, not camelCase, for variable, function and method names (i.e. poll.get_unique_voters(), not poll.getUniqueVoters()).

Use InitialCaps for class names (or for factory functions that return classes).

In docstrings, follow the style of existing docstrings and PEP 257.

In tests, use assertRaisesMessage() and assertWarnsMessage() instead of assertRaises() and assertWarns() so you can check the exception or warning message. Use assertRaisesRegex() and assertWarnsRegex() only if you need regular expression matching.

Use assertIs(…, True/False) for testing boolean values, rather than assertTrue() and assertFalse(), so you can check the actual boolean value, not the truthiness of the expression.

In test docstrings, state the expected behavior that each test demonstrates. Don’t include preambles such as “Tests that” or “Ensures that”.

Reserve ticket references for obscure issues where the ticket has additional details that can’t be easily described in docstrings or comments. Include the ticket number at the end of a sentence like this:

Where applicable, use unpacking generalizations compliant with PEP 448, such as merging mappings ({**x, **y}) or sequences ([*a, *b]). This improves performance, readability, and maintainability while reducing errors.

Use isort to automate import sorting using the guidelines below.

This runs isort recursively from your current directory, modifying any files that don’t conform to the guidelines. If you need to have imports out of order (to avoid a circular import, for example) use a comment like this:

Put imports in these groups: future, standard library, third-party libraries, other Django components, local Django component, try/excepts. Sort lines in each group alphabetically by the full module name. Place all import module statements before from module import objects in each section. Use absolute imports for other Django components and a one-dot relative import (from .foo import Bar) for local components. Avoid multi-dot relative imports.

On each line, alphabetize the items with the upper case items grouped before the lowercase items.

Break long lines using parentheses and indent continuation lines by 4 spaces. Include a trailing comma after the last import and put the closing parenthesis on its own line.

Use a single blank line between the last import and any module level code, and use two blank lines above the first function or class.

For example (comments are for explanatory purposes only):

Use convenience imports whenever available. For example, do this

Follow the below rules in Django template code.

{% extends %} should be the first non-comment line.

Put exactly one space between {{, variable contents, and }}.

In {% load ... %}, list libraries in alphabetical order.

Put exactly one space between {%, tag contents, and %}.

Put the {% block %} tag name in the {% endblock %} tag if it is not on the same line.

Inside curly braces, separate tokens by single spaces, except for around the . for attribute access and the | for a filter.

Within a template using {% extends %}, avoid indenting top-level {% block %} tags.

In Django views, the first parameter in a view function should be called request.

Field names should be all lowercase, using underscores instead of camelCase.

The class Meta should appear after the fields are defined, with a single blank line separating the fields and the class definition.

The order of model inner classes and standard methods should be as follows (noting that these are not all required):

Custom manager attributes

def __str__() and other Python magic methods

def get_absolute_url()

If choices is defined for a given model field, define each choice as a mapping, with an all-uppercase name as a class attribute on the model. Example:

Alternatively, consider using Enumeration types:

Modules should not in general use settings stored in django.conf.settings at the top level (i.e. evaluated when the module is imported). The explanation for this is as follows:

Manual configuration of settings (i.e. not relying on the DJANGO_SETTINGS_MODULE environment variable) is allowed and possible as follows:

However, if any setting is accessed before the settings.configure line, this will not work. (Internally, settings is a LazyObject which configures itself automatically when the settings are accessed if it has not already been configured).

So, if there is a module containing some code as follows:

…then importing this module will cause the settings object to be configured. That means that the ability for third parties to import the module at the top level is incompatible with the ability to configure the settings object manually, or makes it very difficult in some circumstances.

Instead of the above code, a level of laziness or indirection must be used, such as django.utils.functional.LazyObject, django.utils.functional.lazy() or lambda.

Mark all strings for internationalization; see the i18n documentation for details.

Remove import statements that are no longer used when you change code. flake8 will identify these imports for you. If an unused import needs to remain for backwards-compatibility, mark the end of with # NOQA to silence the flake8 warning.

Systematically remove all trailing whitespaces from your code as those add unnecessary bytes, add visual clutter to the patches and can also occasionally cause unnecessary merge conflicts. Some IDE’s can be configured to automatically remove them and most VCS tools can be set to highlight them in diff outputs.

Please don’t put your name in the code you contribute. Our policy is to keep contributors’ names in the AUTHORS file distributed with Django – not scattered throughout the codebase itself. Feel free to include a change to the AUTHORS file in your patch if you make more than a single trivial change.

For details about the JavaScript code style used by Django, see JavaScript code.

---

## Committing code | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/internals/contributing/committing-code/

**Contents:**
- Committing code¶
- Handling pull requests¶
- Committing guidelines¶
- Reverting commits¶

This section is addressed to the mergers and to anyone interested in knowing how code gets committed into Django. The Committing guidelines apply to all contributors, with or without commit rights.

If you’re a community member who wants to contribute code to Django, look at Working with Git and GitHub instead.

Since Django is hosted on GitHub, patches are provided in the form of pull requests.

When committing a pull request, make sure each individual commit matches the commit guidelines described below. Contributors are expected to provide the best pull requests possible. In practice mergers - who will likely be more familiar with the commit guidelines - may decide to bring a commit up to standard themselves.

You may want to have Jenkins or GitHub actions test the pull request with one of the pull request builders that doesn’t run automatically, such as Oracle or Selenium. See the CI wiki page for instructions.

If you find yourself checking out pull requests locally more often, this git alias will be helpful:

Add it to your ~/.gitconfig, and set upstream to be django/django. Then you can run git pr #### to checkout the corresponding pull request.

At this point, you can work on the code. Use git rebase -i and git commit --amend to make sure the commits have the expected level of quality. Once you’re ready:

Force push to the branch after rebasing on main but before merging and pushing to upstream. This allows the commit hashes on main and the branch to match which automatically closes the pull request.

If a pull request doesn’t need to be merged as multiple commits, you can use GitHub’s “Squash and merge” button on the website. Edit the commit message as needed to conform to the guidelines and remove the pull request number that’s automatically appended to the message’s first line.

When rewriting the commit history of a pull request, the goal is to make Django’s commit history as usable as possible:

If a patch contains back-and-forth commits, then rewrite those into one. For example, if a commit adds some code and a second commit fixes stylistic issues introduced in the first commit, those commits should be squashed before merging.

Separate changes to different commits by logical grouping: if you do a stylistic cleanup at the same time as you do other changes to a file, separating the changes into two different commits will make reviewing history easier.

Beware of merges of upstream branches in the pull requests.

Tests should pass and docs should build after each commit. Neither the tests nor the docs should emit warnings.

Trivial and small patches usually are best done in one commit. Medium to large work may be split into multiple commits if it makes sense.

Practicality beats purity, so it is up to each merger to decide how much history mangling to do for a pull request. The main points are engaging the community, getting work done, and having a usable commit history.

These guidelines apply to all commits to Django’s Git repository, whether submitted by a contributor via a pull request or landed directly by a merger:

Never change the published history of django/django branches by force pushing. If you absolutely must (for security reasons for example), first discuss the situation with the team.

For any medium-to-big changes, where “medium-to-big” is according to your judgment, please bring things up on the Django Forum before making the change.

If you bring something up and nobody responds, please don’t take that to mean your idea is great and should be implemented immediately because nobody contested it. Everyone doesn’t always have a lot of time to read discussions immediately, so you may have to wait a couple of days before getting a response.

Write detailed commit messages in the past tense, not present tense, and end the subject line with a period.

Correct: “Fixed Unicode bug in RSS API.”

Incorrect: “Fixes Unicode bug in RSS API.” (present tense)

Incorrect: “Fixing Unicode bug in RSS API.” (“-ing” form)

Incorrect: “Fixed Unicode bug in RSS API” (missing trailing period)

The commit message should be in lines of 72 chars maximum. There should be a subject line, separated by a blank line and then paragraphs of 72 char lines. The limits are soft. For the subject line, shorter is better.

In the body of the commit message more detail is better than less, and should explain why the change was made, not what was changed or how. The code itself shows what changed; the commit message should provide the context and reasoning that the code cannot.

Credit the contributors in the commit message: “Thanks A for the report and B for review.” Use git’s Co-Authored-By as appropriate.

For commits to a branch, prefix the commit message with the branch name. For example: “[1.4.x] Fixed #xxxxx – Added support for mind reading.”

Limit commits to the most granular change that makes sense. This means, use frequent small commits rather than infrequent large commits. For example, if implementing feature X requires a small change to library Y, first commit the change to library Y, then commit feature X in a separate commit. This goes a long way in helping everyone follow your changes.

Separate bug fixes from feature changes. Bugfixes may need to be backported to the stable branch, according to Supported versions.

If your commit closes a ticket in the Django ticket tracker, begin your commit message with the text “Fixed #xxxxx”, where “xxxxx” is the number of the ticket your commit fixes. Example: “Fixed #123 – Added whizbang feature.”. We’ve rigged Trac so that any commit message in that format will automatically close the referenced ticket and post a comment to it with the full commit message.

For the curious, we’re using a Trac plugin for this.

Note that the Trac integration doesn’t know anything about pull requests. So if you try to close a pull request with the phrase “closes #400” in your commit message, GitHub will close the pull request, but the Trac plugin will not close the same numbered ticket in Trac.

If your commit references a ticket in the Django ticket tracker but does not close the ticket, include the phrase “Refs #xxxxx”, where “xxxxx” is the number of the ticket your commit references. This will automatically post a comment to the appropriate ticket.

Write commit messages for backports using this pattern:

There’s a script on the wiki to automate this.

If the commit fixes a regression, include this in the commit message:

(use the commit hash where the regression was introduced).

Nobody’s perfect; mistakes will be committed.

But try very hard to ensure that mistakes don’t happen. Just because we have a reversion policy doesn’t relax your responsibility to aim for the highest quality possible. Really: double-check your work, or have it checked by another merger before you commit it in the first place!

When a mistaken commit is discovered, please follow these guidelines:

If possible, have the original author revert their own commit.

Don’t revert another author’s changes without permission from the original author.

Use git revert – this will make a reverse commit, but the original commit will still be part of the commit history.

If the original author can’t be reached (within a reasonable amount of time – a day or so) and the problem is severe – crashing bug, major test failures, etc. – then ask for objections on the Django Forum then revert if there are none.

If the problem is small (a feature commit after feature freeze, say), wait it out.

If there’s a disagreement between the merger and the reverter-to-be then try to work it out on the Django Forum . If an agreement can’t be reached then it should be put to a vote.

If the commit introduced a confirmed, disclosed security vulnerability then the commit may be reverted immediately without permission from anyone.

The release branch maintainer may back out commits to the release branch without permission if the commit breaks the release branch.

If you mistakenly push a topic branch to django/django, delete it. For instance, if you did: git push upstream feature_antigravity, do a reverse push: git push upstream :feature_antigravity.

---

## Contributing code | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/internals/contributing/writing-code/

**Contents:**
- Contributing code¶
- Tutorials¶
- How-to guides¶
- Related topics¶

So you’d like to write some code, documentation or tests to improve Django? There are several ways you can help Django’s development.

The Django tutorial contains a whole section that walks you step-by-step through the contributing code process.

If you already have some familiarity with the processes and principles, our documentation also contains useful guidance on specific topics:

It’s important to understand how we work and the conventions we adopt.

We maintain a curated list of small issues suited to first-time or less experienced contributors, using the “easy pickings” filter. These are strongly recommended for those contributors looking to make a contribution.

Browse easy pickings tickets.

---

## Contributing to Django | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/internals/contributing/

**Contents:**
- Contributing to Django¶
- Communication channels¶
  - Join the Django community¶
- Getting started¶
- Work on the Django framework¶
  - Contributing code¶
  - Contributing documentation¶
  - Localizing Django¶
- Other ways of contributing¶

Django is a community that lives on its volunteers. As it keeps growing, we always need more people to help others. You can contribute in many ways, either on the framework itself or in the wider ecosystem.

We’re passionate about helping Django users make the jump to contributing members of the community. Communication is key - working on Django is being part of a conversation. Join it, to become familiar with what we’re doing and how we talk about it. You’ll be able to form relationships with more experienced contributors who are there to help guide you towards success.

There are several ways you can help the Django community and others to maintain a great ecosystem to work in:

Join the Django Forum. This forum is a place for discussing the Django framework and applications and projects that use it. This is also a good place to ask and answer any questions related to installing, using, or contributing to Django.

Join the Django Discord server to discuss and answer questions. By explaining Django to other users, you’re going to learn a lot about the framework yourself.

Blog about Django. We syndicate all the Django blogs we know about on the community page; if you’d like to see your blog on that page you can register it here.

Contribute to open-source Django projects, write some documentation, or release your own code as an open-source pluggable application. The ecosystem of pluggable applications is a big strength of Django, help us build it!

Django encourages and welcomes new contributors, and makes an effort to help them become experienced, confident contributors to Open Source Software (OSS). Our documentation contains guidance for first-time contributors, including:

If you enjoy working with Django, wait until you start working on it. Really, anyone can do something to improve Django, which will improve the experience of lots of people!

The work on Django itself falls into three major areas:

Fix a bug, or add a new feature. You can make a pull request and see your code in the next version of Django.

Django’s documentation is one of its key strengths. It’s informative and thorough. You can help to improve the documentation and keep it relevant as the framework evolves.

Django is translated into over 100 languages - There’s even some translation for Klingon?! The i18n team is always looking for translators to help maintain and increase language reach.

Explore additional avenues of contributing to Django beyond coding. Django’s ticket tracker is the central hub for managing issues, improvements, and contributions to Django. It’s a valuable resource where you can report bugs you encounter or assist in triaging existing tickets to ensure a smooth development workflow.

Django also has a process for suggesting ideas where you can join the community in discussing ideas for new features. Beyond the Django codebase, there’s a vibrant ecosystem that is maintained by the community that you can contribute to.

Explore the ways you can make a difference below, and join us in making Django better for everyone.

We’re looking forward to working with you. Welcome aboard!

---

## FAQ: Contributing code | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/faq/contributing/

**Contents:**
- FAQ: Contributing code¶
- How can I get started contributing code to Django?¶
- I submitted a bug fix several weeks ago. Why are you ignoring my contribution?¶
- When and how might I remind the team of a change I care about?¶
- But I’ve reminded you several times and you keep ignoring my contribution!¶
- I’m sure my ticket is absolutely 100% perfect, can I mark it as “Ready For Checkin” myself?¶

Thanks for asking! We’ve written an entire document devoted to this question. It’s titled Contributing to Django.

Don’t worry: We’re not ignoring you!

It’s important to understand there is a difference between “a ticket is being ignored” and “a ticket has not been attended to yet.” Django’s ticket system contains hundreds of open tickets, of various degrees of impact on end-user functionality, and Django’s developers have to review and prioritize.

On top of that: the people who work on Django are all volunteers. As a result, the amount of time that we have to work on the framework is limited and will vary from week to week depending on our spare time. If we’re busy, we may not be able to spend as much time on Django as we might want.

The best way to make sure tickets do not get hung up on the way to checkin is to make it dead easy, even for someone who may not be intimately familiar with that area of the code, to understand the problem and verify the fix:

Are there clear instructions on how to reproduce the bug? If this touches a dependency (such as Pillow), a contrib module, or a specific database, are those instructions clear enough even for someone not familiar with it?

If there are several branches linked to the ticket, is it clear what each one does, which ones can be ignored and which matter?

Does the change include a unit test? If not, is there a very clear explanation why not? A test expresses succinctly what the problem is, and shows that the branch actually fixes it.

If your contribution is not suitable for inclusion in Django, we won’t ignore it – we’ll close the ticket. So if your ticket is still open, it doesn’t mean we’re ignoring you; it just means we haven’t had time to look at it yet.

A polite, well-timed message in the forum/branch is one way to get attention. To determine the right time, you need to keep an eye on the schedule. If you post your message right before a release deadline, you’re not likely to get the sort of attention you require.

Gentle reminders in the #contributing-getting-started channel in the Django Discord server can work.

Another way to get traction is to pull several related tickets together. When someone sits down to review a bug in an area they haven’t touched for a while, it can take a few minutes to remember all the fine details of how that area of code works. If you collect several minor bug fixes together into a similarly themed group, you make an attractive target, as the cost of coming up to speed on an area of code can be spread over multiple tickets.

Please refrain from emailing anyone personally or repeatedly raising the same issue over and over again. This sort of behavior will not gain you any additional attention – certainly not the attention that you need in order to get your issue addressed.

Seriously - we’re not ignoring you. If your contribution is not suitable for inclusion in Django, we will close the ticket. For all the other tickets, we need to prioritize our efforts, which means that some tickets will be addressed before others.

One of the criteria that is used to prioritize bug fixes is the number of people that will likely be affected by a given bug. Bugs that have the potential to affect many people will generally get priority over those that are edge cases.

Another reason that a bug might be ignored for a while is if the bug is a symptom of a larger problem. While we can spend time writing, testing and applying lots of little changes, sometimes the right solution is to rebuild. If a rebuild or refactor of a particular component has been proposed or is underway, you may find that bugs affecting that component will not get as much attention. Again, this is a matter of prioritizing scarce resources. By concentrating on the rebuild, we can close all the little bugs at once, and hopefully prevent other little bugs from appearing in the future.

Whatever the reason, please keep in mind that while you may hit a particular bug regularly, it doesn’t necessarily follow that every single Django user will hit the same bug. Different users use Django in different ways, stressing different parts of the code under different conditions. When we evaluate the relative priorities, we are generally trying to consider the needs of the entire community, instead of prioritizing the impact on one particular user. This doesn’t mean that we think your problem is unimportant – just that in the limited time we have available, we will always err on the side of making 10 people happy rather than making a single person happy.

Sorry, no. It’s always better to get another set of eyes on a ticket. If you’re having trouble getting that second set of eyes, see questions above.

---

## JavaScript code | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/internals/contributing/writing-code/javascript/

**Contents:**
- JavaScript code¶
- Code style¶
- JavaScript patches¶
- JavaScript tests¶
  - Writing tests¶
  - Running tests¶
    - Testing from a web browser¶
    - Testing from the command line¶

While most of Django core is Python, the admin and gis contrib apps contain JavaScript code.

Please follow these coding standards when writing JavaScript code for inclusion in Django.

Please conform to the indentation style dictated in the .editorconfig file. We recommend using a text editor with EditorConfig support to avoid indentation and whitespace issues. Most of the JavaScript files use 4 spaces for indentation, but there are some exceptions.

When naming variables, use camelCase instead of underscore_case. Different JavaScript files sometimes use a different code style. Please try to conform to the code style of each file.

Use the ESLint code linter to check your code for bugs and style errors. ESLint will be run when you run the JavaScript tests. We also recommended installing a ESLint plugin in your text editor.

Where possible, write code that will work even if the page structure is later changed with JavaScript. For instance, when binding a click handler, use $('body').on('click', selector, func) instead of $(selector).click(func). This makes it easier for projects to extend Django’s default behavior with JavaScript.

Django’s admin system leverages the jQuery framework to increase the capabilities of the admin interface. In conjunction, there is an emphasis on admin JavaScript performance and minimizing overall admin media file size.

Django’s JavaScript tests can be run in a browser or from the command line. The tests are located in a top level js_tests directory.

Django’s JavaScript tests use QUnit. Here is an example test module:

Please consult the QUnit documentation for information on the types of assertions supported by QUnit.

The JavaScript tests may be run from a web browser or from the command line.

To run the tests from a web browser, open up js_tests/tests.html in your browser.

To measure code coverage when running the tests, you need to view that file over HTTP. To view code coverage:

Execute python -m http.server from the root directory (not from inside js_tests).

Open http://localhost:8000/js_tests/tests.html in your web browser.

To run the tests from the command line, you need to have Node.js installed.

After installing Node.js, install the JavaScript test dependencies by running the following from the root of your Django checkout:

Then run the tests with:

---

## Localizing Django | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/internals/contributing/localizing/

**Contents:**
- Localizing Django¶
- Translations¶
- Formats¶
- Documentation¶

Various parts of Django, such as the admin site and validation error messages, are internationalized. This means they display differently depending on each user’s language or country. For this, Django uses the same internationalization and localization infrastructure available to Django applications, described in the i18n documentation.

Translations are contributed by Django users worldwide. The translation work is coordinated at Transifex.

If you find an incorrect translation or want to discuss specific translations, go to the Django project page. If you would like to help out with translating or adding a language that isn’t yet translated, here’s what to do:

Introduce yourself on the Django internationalization forum.

Make sure you read the notes about Specialties of Django translation.

Sign up at Transifex and visit the Django project page.

On the Django project page, choose the language you want to work on, or – in case the language doesn’t exist yet – request a new language team by clicking on the “Request language” link and selecting the appropriate language.

Then, click the “Join this Team” button to become a member of this team. Every team has at least one coordinator who is responsible to review your membership request. You can also contact the team coordinator to clarify procedural problems and handle the actual translation process.

Once you are a member of a team choose the translation resource you want to update on the team page. For example, the “core” resource refers to the translation catalog that contains all non-contrib translations. Each of the contrib apps also has a resource (prefixed with “contrib”).

For more information about how to use Transifex, read the Transifex User Guide.

Translations from Transifex are only integrated into the Django repository at the time of a new feature release. We try to update them a second time during one of the following patch releases, but that depends on the translation manager’s availability. So don’t miss the string freeze period (between the release candidate and the feature release) to take the opportunity to complete and fix the translations for your language!

You can also review conf/locale/<locale>/formats.py. This file describes the date, time and numbers formatting particularities of your locale. See Format localization for details.

The format files aren’t managed by the use of Transifex. To change them, you must:

Create a pull request against the Django Git main branch, as for any code change.

Open a ticket in Django’s ticket system, set its Component field to Translations, set the “has patch” flag, and include the link to the pull request.

There is also an opportunity to translate the documentation, though this is a huge undertaking to complete entirely (you have been warned!). We use the same Transifex tool. The translations will appear at https://docs.djangoproject.com/<language_code>/ when at least the docs/intro/* files are fully translated in your language.

Once translations are published, updated versions from Transifex will be irregularly ported to the django/django-docs-translations repository and to the documentation website. Only translations for the latest stable Django release are updated.

---

## Reporting bugs and requesting features | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/internals/contributing/bugs-and-features/

**Contents:**
- Reporting bugs and requesting features¶
- Reporting bugs¶
  - Reporting user interface bugs¶
- Requesting features¶
- Requesting performance optimizations¶
- How we make decisions¶
- How to test pre-release versions of Django¶
  - Prerequisites¶
  - Testing your project¶
  - Reporting issues¶

Please report security issues only to security@djangoproject.com. This is a private list only open to long-time, highly trusted Django developers, and its archives are not public. For further details, please see our security policies.

Before reporting a bug on the ticket tracker consider these points:

Check that someone hasn’t already filed the bug report by searching or running custom queries in the ticket tracker.

Don’t use the ticket system to ask support questions. Use the Django Forum or the Django Discord server for that.

Don’t reopen issues that have been marked “wontfix” without finding consensus to do so on the Django Forum.

Don’t reopen issues that have been marked “needsnewfeatureprocess” without shepherding an issue through the new feature ideas GitHub project.

Don’t use the ticket tracker for lengthy discussions, because they’re likely to get lost. If a particular ticket is controversial, please move the discussion to the Django Forum.

Well-written bug reports are incredibly helpful. However, there’s a certain amount of overhead involved in working with any bug tracking system so your help in keeping our ticket tracker as useful as possible is appreciated. In particular:

Do read the FAQ to see if your issue might be a well-known question.

Do ask on Django Forum or the Django Discord server first if you’re not sure if what you’re seeing is a bug.

Do write complete, reproducible, specific bug reports. You must include a clear, concise description of the problem, and a set of instructions for replicating it. Add as much debug information as you can: code snippets, test cases, exception backtraces, screenshots, etc. A nice small test case is the best way to report a bug, as it gives us a helpful way to confirm the bug quickly.

Don’t post to Django Forum only to announce that you have filed a bug report. All the tickets are mailed to another list, django-updates, which is tracked by developers and interested community members; we see them as they are filed.

To understand the lifecycle of your ticket once you have created it, refer to Triage workflow.

If your bug impacts anything visual in nature, there are a few additional guidelines to follow:

Include screenshots in your ticket which are the visual equivalent of a minimal test case. Show off the issue, not the crazy customizations you’ve made to your browser.

If the issue is difficult to show off using a still image, consider capturing a brief screencast. If your software permits it, capture only the relevant area of the screen.

If you’re offering a patch that changes the look or behavior of Django’s UI, you must attach before and after screenshots/screencasts. Tickets lacking these are difficult for triagers to assess quickly.

Screenshots don’t absolve you of other good reporting practices. Make sure to include URLs, code snippets, and step-by-step instructions on how to reproduce the behavior visible in the screenshots.

Make sure to set the UI/UX flag on the ticket so interested parties can find your ticket.

If the issue relates to accessibility, please link to the relevant accessibility standard if applicable.

We’re always trying to make Django better, and your feature requests are a key part of that. Here are some tips on how to make a request most effectively:

Evaluate whether the feature idea requires changes in Django’s core. If your idea can be developed as an independent application or module — for instance, you want to support another database engine — we’ll probably suggest that you develop it independently. Then, if your project gathers sufficient community support, we may consider it for inclusion in Django.

Propose the feature in the new feature ideas GitHub project (not in the ticket tracker) by creating a new item in the Idea column. This is where the community and the Steering Council evaluate new ideas for the Django ecosystem. This step is especially important for large or complex proposals. We prefer to discuss any significant changes to Django’s core before any development begins. In some cases, a feature may be better suited as a third-party package, where it can evolve independently of Django’s release cycle.

Describe clearly and concisely what the missing feature is and how you’d like to see it implemented. Include example code (non-functional is OK) if possible.

Explain why you’d like the feature. Explaining a minimal use case will help others understand where it fits in, and if there are already other ways of achieving the same thing.

See also: Documenting new features.

Reports of a performance regression, or suggested performance optimizations, should provide benchmarks and commands for the ticket triager to reproduce.

See the django-asv benchmarks for more details of Django’s existing benchmarks.

Whenever possible, we aim for rough consensus. Emoji reactions are used on issues within the new feature ideas GitHub project to track community feedback. The following meanings are assigned to each reaction:

👍: I support this feature and would use it

👎: I oppose this feature or believe it would cause issues for me or Django

😕: I have no strong opinion on this feature

🎉: This feature seems like a straightforward and beneficial addition

The Steering Council will regularly review the ideas in the project, moving those with community support through the following stages:

Approved - Idea refinement - Team creation

Working solution - Review - Feedback

Needs maintainer (Django only)

Occasionally, discussions on feature ideas or the direction of Django may take place on the Django Forum. These discussions may include informal votes, which follow the voting style invented by Apache and used on Python itself, where votes are given as +1, +0, -0, or -1. Roughly translated, these votes mean:

+1: “I love the idea and I’m strongly committed to it.”

+0: “Sounds OK to me.”

-0: “I’m not thrilled, but I won’t stand in the way.”

-1: “I strongly disagree and would be very unhappy to see the idea turn into reality.”

Although these votes are informal, they’ll be taken very seriously. After a suitable voting period, if an obvious consensus arises we’ll follow the votes.

Testing pre-releases is a great way to contribute to Django. Early testers help catch bugs before the final release, ensuring a smoother upgrade experience for everyone.

Before testing a pre-release, it is important that your project is running smoothly on the latest stable release of Django. That way, any regressions can be attributed to the pre-release. See the How to upgrade Django to a newer version guide for instructions on getting up to date.

To ensure your project is ready, you should also:

Read the release notes: Review the Release notes for the upcoming version to learn about upgrade paths for deprecated features or about minor backward-incompatible changes.

Resolve deprecation warnings: Run your tests with deprecation warnings enabled to become aware of required follow-up actions:

You can install the latest pre-release using pip:

Once installed, run your project’s test suite. Rather than just checking if tests pass, try the following:

Check dependency support: Determine whether major dependencies support the new version by checking Django version classifiers on PyPI. Since those projects also value early bug reports, don’t let a lack of support prevent you from testing.

Monitor performance: You can run your tests with the test --durations flag to identify potential performance regressions.

Automate tests in CI: Consider running your Continuous Integration (CI) pipeline with the pre-release version.

Test manually: While automated tests are great, manually testing your application’s main workflows is an important part of verifying compatibility with a new release.

If you discover a bug, please report it via the Django issue tracker so it can be fixed before the final release. When creating the ticket, be sure to set the Django version field to the exact pre-release version you are testing.

If you suspect a regression, it’s helpful to report the specific commit that caused it. See Bisecting a regression for instructions.

You can also discuss any issues or share feedback in the Pre-releases category on the Django Forum.

---

## Submitting contributions | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/internals/contributing/writing-code/submitting-patches/

**Contents:**
- Submitting contributions¶
- Typo fixes and trivial documentation changes¶
- “Claiming” tickets¶
  - Ticket claimers’ responsibility¶
  - Which tickets should be claimed?¶
- Contribution style¶
- Contributions which require community feedback¶
  - The new feature ideas tracker¶
  - The Django Forum¶
  - Third party package¶

We’re always grateful for contributions to Django’s code. Indeed, bug reports with associated contributions will get fixed far more quickly than those without a solution.

If you are fixing a really trivial issue, for example changing a word in the documentation, the preferred way to provide the patch is using GitHub pull requests without a Trac ticket.

See the Working with Git and GitHub for more details on how to use pull requests.

In an open-source project with hundreds of contributors around the world, it’s important to manage communication efficiently so that work doesn’t get duplicated and contributors can be as effective as possible.

Hence, our policy is for contributors to “claim” tickets in order to let other developers know that a particular bug or feature is being worked on.

If you have identified a contribution you want to make and you’re capable of fixing it (as measured by your coding ability, knowledge of Django internals and time availability), claim it by following these steps:

Login using your GitHub account or create an account in our ticket system. If you have an account but have forgotten your password, you can reset it using the password reset page.

If a ticket for this issue doesn’t exist yet, create one in our ticket tracker. Remember that proposals for new features should follow the process for suggesting new features.

If a ticket for this issue already exists and has been accepted, make sure nobody else has claimed it. To do this, look at the “Owned by” section of the ticket. If it’s assigned to “nobody,” then it’s available to be claimed. Otherwise, somebody else may be working on this ticket. Either find another bug/feature to work on, or contact the developer working on the ticket to offer your help. If a ticket has been assigned for weeks or months without any activity, it’s probably safe to reassign it to yourself. If a ticket hasn’t been approved yet, join the conversation.

Log into your account, if you haven’t already, by clicking “GitHub Login” or “DjangoProject Login” in the upper left of the ticket page. Once logged in, you can then click the “Modify Ticket” button near the bottom of the page.

Claim the ticket by clicking the “assign to” radio button in the “Action” section. Your username will be filled in the text box by default.

Finally click the “Submit changes” button at the bottom to save.

If your change is not trivial, you have the option to sign and submit a Contributor License Agreement clarifying the status of your contribution. This ensures that the Django Software Foundation has clear license to your contribution.

Once you’ve claimed a ticket, you have a responsibility to work on that ticket in a reasonably timely fashion. If you don’t have time to work on it, either unclaim it or don’t claim it in the first place!

If there’s no sign of progress on a particular claimed ticket for a week or two, another developer may ask you to relinquish the ticket claim so that it’s no longer monopolized and somebody else can claim it.

If you’ve claimed a ticket and it’s taking a long time (days or weeks) to code, keep everybody updated by posting comments on the ticket. If you don’t provide regular updates, and you don’t respond to a request for a progress report, your claim on the ticket may be revoked.

As always, more communication is better than less communication!

Going through the steps of claiming tickets is overkill in some cases.

In the case of small changes, such as typos in the documentation or small bugs that will only take a few minutes to fix, you don’t need to jump through the hoops of claiming tickets. Submit your changes directly and you’re done!

It is always acceptable, regardless whether someone has claimed it or not, to link proposals to a ticket if you happen to have the changes ready.

Make sure that any contribution you do fulfills at least the following requirements:

The code required to fix a problem or add a feature is an essential part of a solution, but it is not the only part. A good fix should also include a regression test to validate the behavior that has been fixed and to prevent the problem from arising again. Also, if some tickets are relevant to the code that you’ve written, mention the ticket numbers in some comments in the test so that one can easily trace back the relevant discussions after your patch gets committed, and the tickets get closed.

If the code adds a new feature, or modifies the behavior of an existing feature, the change should also contain documentation.

When you think your work is ready to be reviewed, send a GitHub pull request. If you can’t send a pull request for some reason, you can also use patches in Trac. When using this style, follow these guidelines.

Submit patches in the format returned by the git diff command.

Attach patches to a ticket in the ticket tracker, using the “attach file” button. Please don’t put the patch in the ticket description or comment unless it’s a single line patch.

Name the patch file with a .diff extension; this will let the ticket tracker apply correct syntax highlighting, which is quite helpful.

Regardless of the way you submit your work, follow these steps.

Make sure your code fulfills the requirements in our contribution checklist.

Check the “Has patch” box on the ticket and make sure the “Needs documentation”, “Needs tests”, and “Patch needs improvement” boxes aren’t checked. This makes the ticket appear in the “Patches needing review” queue on the Development dashboard.

A wider community discussion is required when a patch introduces new Django functionality and makes some sort of design decision. This is especially important if the approach involves a deprecation or introduces breaking changes.

The following are different approaches for gaining feedback from the community.

If you have an idea for a new feature, please create a new proposal (or join an existing discussion) following the process for suggesting new features. You should explain the need for the change, go into details of the approach and discuss alternatives.

You can propose a change (that is not a new feature idea) on the Django Forum. You should explain the need for the change, go into details of the approach and discuss alternatives.

Please include a link to such discussions in your contributions.

Django does not accept experimental features. All features must follow our deprecation policy. Hence, it can take months or years for Django to iterate on an API design.

If you need user feedback on a public interface, it is better to create a third-party package first. You can iterate on the public API much faster, while also validating the need for the feature.

Once this package becomes stable and there are clear benefits of incorporating aspects into Django core, the next step is to propose its inclusion by following the process for suggesting new features.

Similar to Python’s PEPs, Django has Django Enhancement Proposals or DEPs. A DEP is a design document which provides information to the Django community, or describes a new feature or process for Django. They provide concise technical specifications of features, along with rationales. DEPs are also the primary mechanism for proposing and collecting community input on major new features.

Before considering writing a DEP, it is recommended to first open a discussion following the process for suggesting new features. This allows the community to provide feedback and helps refine the proposal. Once the DEP is ready the Steering Council votes on whether to accept it.

Some examples of DEPs that have been approved and fully implemented:

DEP 181: ORM Expressions

DEP 182: Multiple Template Engines

DEP 201: Simplified routing syntax

There are a couple of reasons that code in Django might be deprecated:

If a feature has been improved or modified in a backwards-incompatible way, the old feature or behavior will be deprecated.

Sometimes Django will include a backport of a Python library that’s not included in a version of Python that Django currently supports. When Django no longer needs to support the older version of Python that doesn’t include the library, the library will be deprecated in Django.

As the deprecation policy describes, the first release of Django that deprecates a feature (A.B) should raise a RemovedInDjangoXXWarning (where XX is the Django version where the feature will be removed) when the deprecated feature is invoked. Assuming we have good test coverage, these warnings are converted to errors when running the test suite with warnings enabled: python -Wa runtests.py. Thus, when adding a RemovedInDjangoXXWarning you need to eliminate or silence any warnings generated when running the tests.

The first step is to remove any use of the deprecated behavior by Django itself. Next you can silence warnings in tests that actually test the deprecated behavior by using the ignore_warnings decorator, either at the test or class level:

In a particular test:

For an entire test case:

You should also add a test for the deprecation warning:

It’s important to include a RemovedInDjangoXXWarning comment above code which has no warning reference, but will need to be changed or removed when the deprecation ends. This could include hooks which have been added to keep the previous behavior, or standalone items that are unnecessary or unused when the deprecation ends. For example:

Finally, there are a couple of updates to Django’s documentation to make:

If the existing feature is documented, mark it deprecated in documentation using the .. deprecated:: A.B annotation. Include a short description and a note about the upgrade path if applicable.

Add a description of the deprecated behavior, and the upgrade path if applicable, to the current release notes (docs/releases/A.B.txt) under the “Features deprecated in A.B” heading.

Add an entry in the deprecation timeline (docs/internals/deprecation.txt) under the appropriate version describing what code will be removed.

Once you have completed these steps, you are finished with the deprecation. In each feature release, all RemovedInDjangoXXWarnings matching the new version are removed.

The django.utils.deprecation module provides some helpful deprecation utilities, such as a @deprecate_posargs decorator to assist with converting positional-or-keyword arguments to keyword-only. See the inline documentation in the module source.

It’s important to test local changes using a Django project. This allows ensuring that the changes behave as expected in a real environment, especially for user-facing features such as templates, forms, or the admin.

Create a virtual environment and install the cloned copy of Django in editable mode.

Set up a Django project outside the source tree (you can use the first part of the tutorial for guidance).

With this setup, any changes made to the Django checkout will take effect immediately in the test project, allowing manual testing of contributions against a new or existing app.

For information on JavaScript contributions, see the JavaScript patches documentation.

Patches aiming to deliver a performance improvement should provide benchmarks showing the before and after impact of the patch and sharing the commands for reviewers to reproduce.

django-asv monitors the performance of Django code over time. These benchmarks can be run on a pull request by labeling the pull request with benchmark. Adding to these benchmarks is highly encouraged.

Use this checklist to review a pull request. If this contribution would not be considered trivial, first ensure it has an accepted ticket before proceeding with the review.

If the pull request passes all the criteria below and is not your own, please set the “Triage Stage” on the corresponding Trac ticket to “Ready for checkin”. If you’ve left comments for improvement on the pull request, please tick the appropriate flags on the Trac ticket based on the results of your review: “Patch needs improvement”, “Needs documentation”, and/or “Needs tests”. As time and interest permits, mergers do final reviews of “Ready for checkin” tickets and will either commit the changes or bump it back to “Accepted” if further work needs to be done.

If you’re looking to become a member of the triage & review team, doing thorough reviews of contributions is a great way to earn trust.

Looking for a patch to review? Check out the “Patches needing review” section of the Django Development Dashboard.

Looking to get your pull request reviewed? Ensure the Trac flags on the ticket are set so that the ticket appears in that queue.

Does the documentation build without any errors (make html, or make.bat html on Windows, from the docs directory)?

Does the documentation follow the writing style guidelines in Writing documentation?

Are there any spelling errors?

Is there a proper regression test (the test should fail before the fix is applied)?

If it’s a bug that qualifies for a backport to the stable version of Django, is there a release note in docs/releases/A.B.C.txt? Bug fixes that will be applied only to the main branch don’t need a release note.

Are there tests to “exercise” all of the new code?

Is there a release note in docs/releases/A.B.txt?

Is there documentation for the feature and is it annotated appropriately with .. versionadded:: A.B or .. versionchanged:: A.B?

See the Deprecating a feature guide.

Does the coding style conform to our guidelines? Are there any black, blacken-docs, flake8, isort, or zizmor errors? You can install the pre-commit hooks to automatically catch these errors.

If the change is backwards incompatible in any way, is there a note in the release notes (docs/releases/A.B.txt)?

Is Django’s test suite passing?

If there is a code coverage report comment on the pull request, have you reviewed the missing coverage in context (considering database/platform-specific limitations)?

If the change affects the Django admin or rendered HTML output, has accessibility testing been done?

Is the pull request a single squashed commit with a message that follows our commit message format?

Are you the patch author and a new contributor? Please add yourself to the AUTHORS file. At your option, submit a Contributor License Agreement.

Does this have an accepted ticket on Trac? All contributions require a ticket unless the change is considered trivial.

---

## Triaging tickets | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/internals/contributing/triaging-tickets/

**Contents:**
- Triaging tickets¶
- Triage workflow¶
- Triage stages¶
  - Unreviewed¶
  - Accepted¶
  - Ready For Checkin¶
  - Someday/Maybe¶
- Other triage attributes¶
  - Has patch¶
  - Needs documentation¶

Django uses Trac for managing the work on the code base. Trac is a community-tended garden of the bugs people have found and the features Django has decided to add. As in any garden, sometimes there are weeds to be pulled and sometimes there are flowers and vegetables that need picking. We need your help to sort out one from the other, and in the end, we all benefit together.

Like all gardens, we can aspire to perfection, but in reality there’s no such thing. Even in the most pristine garden there are still snails and insects. In a community garden there are also helpful people who – with the best of intentions – fertilize the weeds and poison the roses. It’s the job of the community as a whole to self-manage, keep the problems to a minimum, and educate those coming into the community so that they can become valuable contributing members.

Similarly, while we aim for Trac to be a perfect representation of the state of Django’s progress, we acknowledge that this will not happen. By distributing the load of Trac maintenance to the community, we accept that there will be mistakes. Trac is “mostly accurate”, and we give allowances for the fact that sometimes it will be wrong. That’s okay. We’re perfectionists with deadlines.

We rely on the community to keep participating, keep tickets as accurate as possible, and raise issues for discussion on the Django Forum when there is confusion or disagreement.

Django is a community project, and every contribution helps. We can’t do this without you!

Unfortunately, not all reports in the ticket tracker provide all the required details. A number of tickets have proposed solutions, but those don’t necessarily meet all the requirements adhering to the guidelines for contributing.

One way to help out is to triage tickets that have been created by other users.

Most of the workflow is based around the concept of a ticket’s triage stages. Each stage describes where in its lifetime a given ticket is at any time. Along with a handful of flags, this attribute easily tells us what and who each ticket is waiting on.

Since a picture is worth a thousand words, let’s start there:

We have four roles in this diagram. Maintainers (also known as Fellows) usually take part in all of them, but anyone in the Django community can participate in any role except merger. The merger role is granted by a vote of the Steering Council.

Triagers: anyone can take on this role by checking whether a ticket describes a real issue and keeping the tracker organized.

Bug fixers: anyone can contribute by opening a pull request and working on a solution for a ticket.

Reviewers: anyone can review pull requests and suggest improvements.

Mergers: people with commit access who make the final decision to merge a change.

Our Trac system is intentionally open to the public, and anyone can help by working on tickets. Django is a community project, and we encourage triage and collaboration by the community. This could be you!

For example, here’s the typical lifecycle of a ticket:

Alice creates a ticket and opens an incomplete pull request (missing tests, incorrect implementation).

Bob reviews the pull request, marks the ticket as “Accepted”, sets the flags “needs tests” and “patch needs improvement”, and leaves a comment explaining how Alice can improve the patch. This puts the ticket automatically into the “waiting on author” queue within the “accepted” stage.

Alice updates the pull request, adding tests (but not yet fixing the implementation), and removes the two flags. The ticket moves into the “needs PR review” queue.

Charlie reviews the pull request, sets the “patch needs improvement” flag again, and leaves another comment suggesting changes to the implementation. The ticket moves back to the “waiting on author” queue.

Alice updates the pull request again, this time fixing the implementation, and removes the “patch needs improvement” flag. The ticket moves once more into the “needs PR review” queue.

Daisy reviews the pull request and marks the ticket as “Ready for checkin”.

Jacob, a merger, reviews and merges the pull request.

Some tickets move through these steps quickly, while others take more time and discussion. Each contribution helps Django improve.

Below we describe in more detail the various stages that a ticket may flow through during its lifetime.

The ticket has not been reviewed by anyone who felt qualified to make a judgment about whether the ticket contained a valid issue or ought to be closed for any reasons. Unreviewed tickets appear in the “triage” queue.

Unreviewed tickets may receive additional refinement before being accepted. Unless you are both the author of the ticket and intending to submit a patch, unreviewed tickets should not be claimed.

The absolute meaning of “accepted” is that the issue described in the ticket is valid and actionable. It is broken out into three queues:

Needs Patch (Accepted + No Flags)

The ticket is valid, but no one has submitted a patch for it yet. Often this means you could safely start writing a fix for it. This is generally more true for the case of accepted bugs than accepted features. A ticket for a bug that has been accepted means that the issue has been verified by at least one triager as a legitimate bug - and should probably be fixed if possible.

For new features, accepted tickets should only exist after the idea has gone through the appropriate process for suggesting new features and received community and Steering Council approval, or been accepted in a DEP.

Needs PR Review (Accepted + Has Patch)

The ticket is waiting for people to review the supplied solution. This means downloading the patch and trying it out, verifying that it contains tests and docs, running the test suite with the included patch, and leaving feedback on the ticket.

Waiting On Author (Accepted + Has Patch + Needs fixes)

This means the ticket has been reviewed, and has been found to need further work. “Needs tests” and “Needs documentation” are self-explanatory. “Patch needs improvement” will generally be accompanied by a comment on the ticket explaining what is needed to improve the code.

The ticket was reviewed by any member of the community other than the person who supplied the patch and found to meet all the requirements for a commit-ready contribution. A merger now needs to give a final review prior to being committed.

There are a lot of pull requests. It can take a while for your patch to get reviewed. See the contributing code FAQ for some ideas here.

This stage isn’t shown on the diagram. It’s used sparingly to keep track of long-term changes.

These tickets are uncommon and overall less useful since they don’t describe concrete actionable issues.

A number of flags, appearing as checkboxes in Trac, can be set on a ticket:

This means the ticket has an associated solution. These will be reviewed to ensure they adhere to the documented guidelines.

The following three fields (Needs documentation, Needs tests, Patch needs improvement) apply only if a patch has been supplied.

This flag is used for tickets with patches that need associated documentation. Complete documentation of features is a prerequisite before we can check them into the codebase.

This flags the patch as needing associated unit tests. Again, this is a required part of a valid contribution.

This flag means that although the ticket has a solution, it’s not quite ready for checkin. This could mean the patch no longer applies cleanly, there is a flaw in the implementation, or that the code doesn’t meet our standards.

Tickets that would require small, easy, changes.

Tickets should be categorized by type between:

For adding something new.

For when an existing thing is broken or not behaving as expected.

For when nothing is broken but something could be made cleaner, better, faster, stronger.

Tickets should be classified into components indicating which area of the Django codebase they belong to. This makes tickets better organized and easier to find.

The severity attribute is used to identify blockers, that is, issues that should get fixed before releasing the next version of Django. Typically those issues are bugs causing regressions from earlier versions or potentially causing severe data losses. This attribute is quite rarely used and the vast majority of tickets have a severity of “Normal”.

The version attribute indicates the earliest version in which the bug was reproduced. During triage, this field can be updated, but there is no need to make further updates when that version goes out of support. The field should not be reset to “dev” to show the issue still exists: instead, the tested commit hash can be noted in a comment.

This flag is used for tickets that relate to User Interface and User Experiences questions. For example, this flag would be appropriate for user-facing features in forms or the admin interface.

You may add your username or email address to this field to be notified when new contributions are made to the ticket.

With this field you may label a ticket with multiple keywords. This can be useful, for example, to group several tickets on the same theme. Keywords can either be comma or space separated. Keyword search finds the keyword string anywhere in the keywords. For example, clicking on a ticket with the keyword “form” will yield similar tickets tagged with keywords containing strings such as “formset”, “modelformset”, and “ManagementForm”.

When a ticket has completed its useful lifecycle, it’s time for it to be closed. Closing a ticket is a big responsibility, though. You have to be sure that the issue is really resolved, and you need to keep in mind that the reporter of the ticket may not be happy to have their ticket closed (unless it’s fixed!). If you’re not certain about closing a ticket, leave a comment with your thoughts instead.

If you do close a ticket, you should always make sure of the following:

Be certain that the issue is resolved.

Leave a comment explaining the decision to close the ticket.

If there is a way they can improve the ticket to reopen it, let them know.

If the ticket is a duplicate, reference the original ticket. Also cross-reference the closed ticket by leaving a comment in the original one – this allows to access more related information about the reported bug or requested feature.

Be polite. No one likes having their ticket closed. It can be frustrating or even discouraging. The best way to avoid turning people off from contributing to Django is to be polite and friendly and to offer suggestions for how they could improve this ticket and other tickets in the future.

A ticket can be resolved in a number of ways:

Used once a patch has been rolled into Django and the issue is fixed.

Used if the ticket is found to be incorrect. This means that the issue in the ticket is actually the result of a user error, or describes a problem with something other than Django, or isn’t a bug report or feature request at all (for example, some new users submit support queries as tickets).

Used when someone decides that the request isn’t appropriate for consideration in Django. Sometimes a ticket is closed as “wontfix” with a request for the reporter to start a discussion on the Django Forum if they feel differently from the rationale provided by the person who closed the ticket. Other times, a discussion precedes the decision to close a ticket. Always use the forum to get a consensus before reopening tickets closed as “wontfix”.

Used when the ticket merits a new feature, which will need to get community input and support. See the process for suggesting new features.

Used when another ticket covers the same issue. By closing duplicate tickets, we keep all the discussion in one place, which helps everyone.

Used when the ticket doesn’t contain enough detail to replicate the original bug.

Used when the ticket does not contain enough information to replicate the reported issue but is potentially still valid. The ticket should be reopened when more information is supplied.

If you believe that the ticket was closed in error – because you’re still having the issue, or it’s popped up somewhere else, or the triagers have made a mistake – please reopen the ticket and provide further information. Again, please do not reopen tickets that have been marked as “wontfix” or “needsnewfeatureprocess”. For “wontfix” tickets, bring the issue to the Django Forum instead. For “needsnewfeatureprocess” tickets, propose the feature through the new features process.

The development process is primarily driven by community members. Really, ANYONE can help.

To get involved, start by creating an account on Trac. If you have an account but have forgotten your password, you can reset it using the password reset page.

Then, you can help out by:

Closing “Unreviewed” tickets as “invalid”, “worksforme”, “duplicate”, “wontfix”, or “needsnewfeatureprocess”.

Closing “Unreviewed” tickets as “needsinfo” when the description is too sparse to be actionable.

Correcting the “Needs tests”, “Needs documentation”, or “Has patch” flags for tickets where they are incorrectly set.

Setting the “Easy pickings” flag for tickets that are small and relatively straightforward.

Set the type of tickets that are still uncategorized.

Checking that old tickets are still valid. If a ticket hasn’t seen any activity in a long time, it’s possible that the problem has been fixed but the ticket hasn’t yet been closed.

Identifying trends and themes in the tickets. If there are a lot of bug reports about a particular part of Django, it may indicate we should consider refactoring that part of the code. If a trend is emerging, you should raise it for discussion (referencing the relevant tickets) on the Django Forum.

Verify if solutions submitted by others are correct. If they are correct and also contain appropriate documentation and tests then move them to the “Ready for Checkin” stage. If they are not correct then leave a comment to explain why and set the corresponding flags (“Patch needs improvement”, “Needs tests” etc.).

The Reports page contains links to many useful Trac queries, including several that are useful for triaging tickets and reviewing proposals as suggested above.

You can also find more Advice for new contributors.

However, we do ask the following of all general community members working in the ticket database:

Please don’t promote your own tickets to “Accepted”. Another community member should review the report and set this stage after reproducing and confirming the issue.

Please don’t promote your own tickets to “Ready for checkin”. You may mark other people’s tickets that you’ve reviewed as “Ready for checkin”, but you should get at minimum one other community member to review a patch that you submit.

Please don’t reverse a decision without posting a message to the Django Forum to find consensus.

If you’re unsure if you should be making a change, don’t make the change but instead leave a comment with your concerns on the ticket, or post a message to the Django Forum. It’s okay to be unsure, but your input is still valuable.

A regression is a bug that’s present in some newer version of Django but not in an older one. An extremely helpful piece of information is the commit that introduced the regression. Knowing the commit that caused the change in behavior helps identify if the change was intentional or if it was an inadvertent side-effect. Here’s how you can determine this.

Begin by writing a regression test for Django’s test suite for the issue. For example, we’ll pretend we’re debugging a regression in migrations. After you’ve written the test and confirmed that it fails on the latest main branch, put it in a separate file that you can run standalone. For our example, we’ll pretend we created tests/migrations/test_regression.py, which can be run with:

Next, we mark the current point in history as being “bad” since the test fails:

Now, we need to find a point in git history before the regression was introduced (i.e. a point where the test passes). Use something like git checkout HEAD~100 to check out an earlier revision (100 commits earlier, in this case). Check if the test fails. If so, mark that point as “bad” (git bisect bad), then check out an earlier revision and recheck. Once you find a revision where your test passes, mark it as “good”:

Now we’re ready for the fun part: using git bisect run to automate the rest of the process:

You should see git bisect use a binary search to automatically checkout revisions between the good and bad commits until it finds the first “bad” commit where the test fails.

Now, report your results on the Trac ticket, and please include the regression test as an attachment. When someone writes a fix for the bug, they’ll already have your test as a starting point.

---

## Unit tests | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/internals/contributing/writing-code/unit-tests/

**Contents:**
- Unit tests¶
- Running the unit tests¶
  - Quickstart¶
  - Running tests using tox¶
    - Testing other Python versions and database backends¶
    - Running the JavaScript tests¶
  - Running tests using django-docker-box¶
  - Using another settings module¶
  - Running only some of the tests¶
  - Running the Selenium tests¶

Django comes with a test suite of its own, in the tests directory of the code base. It’s our policy to make sure all tests pass at all times.

We appreciate any and all contributions to the test suite!

The Django tests all use the testing infrastructure that ships with Django for testing applications. See Writing and running tests for an explanation of how to write new tests.

First, fork Django on GitHub.

Second, create and activate a virtual environment. If you’re not familiar with how to do that, read our contributing tutorial.

Next, clone your fork, install some requirements, and run the tests:

Installing the requirements will likely require some operating system packages that your computer doesn’t have installed. You can usually figure out which package to install by doing a web search for the last line or so of the error message. Try adding your operating system to the search query if needed.

If you have trouble installing the requirements, you can skip that step. See Running all the tests for details on installing the optional test dependencies. If you don’t have an optional dependency installed, the tests that require it will be skipped.

Running the tests requires a Django settings module that defines the databases to use. To help you get started, Django provides and uses a sample settings module that uses the SQLite database. See Using another settings module to learn how to use a different settings module to run the tests with a different database.

Having problems? See Troubleshooting for some common issues.

Tox is a tool for running tests in different virtual environments. Django includes a basic tox.ini that automates some checks that our build server performs on pull requests. To run the unit tests and other checks (such as import sorting, the documentation spelling checker, and code formatting), install and run the tox command from any place in the Django source tree:

By default, tox runs the test suite with the bundled test settings file for SQLite, black, blacken-docs, flake8, isort, lint-docs, zizmor, and the documentation spelling checker. In addition to the system dependencies noted elsewhere in this documentation, the command python3 must be on your path and linked to the appropriate version of Python. A list of default environments can be seen as follows:

In addition to the default environments, tox supports running unit tests for other versions of Python and other database backends. Since Django’s test suite doesn’t bundle a settings file for database backends other than SQLite, however, you must create and provide your own test settings. For example, to run the tests on Python 3.12 using PostgreSQL:

This command sets up a Python 3.12 virtual environment, installs Django’s test suite dependencies (including those for PostgreSQL), and calls runtests.py with the supplied arguments (in this case, --settings=my_postgres_settings).

The remainder of this documentation shows commands for running tests without tox, however, any option passed to runtests.py can also be passed to tox by prefixing the argument list with --, as above.

Tox also respects the DJANGO_SETTINGS_MODULE environment variable, if set. For example, the following is equivalent to the command above:

Windows users should use:

Django includes a set of JavaScript unit tests for functions in certain contrib apps. The JavaScript tests aren’t run by default using tox because they require Node.js to be installed and aren’t necessary for the majority of patches. To run the JavaScript tests using tox:

This command runs npm install to ensure test requirements are up to date and then runs npm test.

django-docker-box allows you to run the Django’s test suite across all supported databases and python versions. See the django-docker-box project page for installation and usage instructions.

The included settings module (tests/test_sqlite.py) allows you to run the test suite using SQLite. If you want to run the tests using a different database, you’ll need to define your own settings file. Some tests, such as those for contrib.postgres, are specific to a particular database backend and will be skipped if run with a different backend. Some tests are skipped or expected failures on a particular database backend (see DatabaseFeatures.django_test_skips and DatabaseFeatures.django_test_expected_failures on each backend).

To run the tests with different settings, ensure that the module is on your PYTHONPATH and pass the module with --settings.

The DATABASES setting in any test settings module needs to define two databases:

A default database. This database should use the backend that you want to use for primary testing.

A database with the alias other. The other database is used to test that queries can be directed to different databases. This database should use the same backend as the default, and it must have a different name.

If you’re using a backend that isn’t SQLite, you will need to provide other details for each database:

The USER option needs to specify an existing user account for the database. That user needs permission to execute CREATE DATABASE so that the test database can be created.

The PASSWORD option needs to provide the password for the USER that has been specified.

Test databases get their names by prepending test_ to the value of the NAME settings for the databases defined in DATABASES. These test databases are deleted when the tests are finished.

You will also need to ensure that your database uses UTF-8 as the default character set. If your database server doesn’t use UTF-8 as a default charset, you will need to include a value for CHARSET in the test settings dictionary for the applicable database.

Django’s entire test suite takes a while to run, and running every single test could be redundant if, say, you just added a test to Django that you want to run quickly without running everything else. You can run a subset of the unit tests by appending the names of the test modules to runtests.py on the command line.

For example, if you’d like to run tests only for generic relations and internationalization, type:

How do you find out the names of individual tests? Look in tests/ — each directory name there is the name of a test.

If you want to run only a particular class of tests, you can specify a list of paths to individual test classes. For example, to run the TranslationTests of the i18n module, type:

Going beyond that, you can specify an individual test method like this:

You can run tests starting at a specified top-level module with --start-at option. For example:

You can also run tests starting after a specified top-level module with --start-after option. For example:

Note that the --reverse option doesn’t impact on --start-at or --start-after options. Moreover these options cannot be used with test labels.

Some tests require Selenium and a web browser. To run these tests, you must install the selenium package and run the tests with the --selenium=<BROWSERS> option. For example, if you have Firefox and Google Chrome installed:

See the selenium.webdriver package for the list of available browsers.

Specifying --selenium automatically sets --tags=selenium to run only the tests that require selenium.

Some browsers (e.g. Chrome or Firefox) support headless testing, which can be faster and more stable. Add the --headless option to enable this mode.

For testing changes to the admin UI, the selenium tests can be run with the --screenshots option enabled. Screenshots will be saved to the tests/screenshots/ directory.

To define when screenshots should be taken during a selenium test, the test class must use the @django.test.selenium.screenshot_cases decorator with a list of supported screenshot types ("desktop_size", "mobile_size", "small_screen_size", "rtl", "dark", and "high_contrast"). It can then call self.take_screenshot("unique-screenshot-name") at the desired point to generate the screenshots. For example:

This generates multiple screenshots of the login page - one for a desktop screen, one for a mobile screen, one for right-to-left languages on desktop, one for the dark mode on desktop, and one for high contrast mode on desktop when using chrome.

If you want to run the full suite of tests, you’ll need to install a number of dependencies:

asgiref 3.9.1+ (required)

pymemcache, plus a supported Python binding

gettext (gettext on Windows)

sqlparse 0.5.0+ (required)

You can find these dependencies in pip requirements files inside the tests/requirements directory of the Django source tree and install them like so:

If you encounter an error during the installation, your system might be missing a dependency for one or more of the Python packages. Consult the failing package’s documentation or search the web with the error message that you encounter.

You can also install the database adapter(s) of your choice using oracle.txt, mysql.txt, or postgres.txt.

If you want to test the memcached or Redis cache backends, you’ll also need to define a CACHES setting that points at your memcached or Redis instance respectively.

To run the GeoDjango tests, you will need to set up a spatial database and install the Geospatial libraries.

Each of these dependencies is optional. If you’re missing any of them, the associated tests will be skipped.

To run some of the autoreload tests, you’ll need to install the Watchman service.

Contributors are encouraged to run coverage on the test suite to identify areas that need additional tests. The coverage tool installation and use is described in testing code coverage.

To run coverage on the Django test suite using the standard test settings:

After running coverage, combine all coverage statistics by running:

After that generate the html report by running:

When running coverage for the Django tests, the included .coveragerc settings file defines coverage_html as the output directory for the report and also excludes several directories not relevant to the results (test code or external code included in Django).

Django’s continuous integration (CI) system automatically runs code coverage analysis on pull requests and posts a comment with a diff coverage report. This helps reviewers see which lines in the changed code are covered by tests.

What the coverage report shows:

The coverage report posted on pull requests uses diff-cover to analyze only the lines that were changed or added in the PR. It shows:

Lines that are covered by tests (✓)

Lines that are not covered by tests (✗)

Lines that cannot be covered (e.g., comments, blank lines)

Important limitations:

When reviewing coverage reports on pull requests, keep these limitations in mind:

Database-specific code: The CI coverage job runs tests using SQLite on Windows. Code paths specific to other databases (PostgreSQL, MySQL, Oracle) will appear as “not covered” even if database-specific tests exist. This is expected and acceptable.

Platform-specific code: Similarly, code that only runs on certain operating systems (Linux, macOS) will appear as not covered when run on Windows.

Coverage doesn’t equal quality: A line being “covered” only means it was executed during tests. It doesn’t guarantee the line is well-tested or that all edge cases are handled. During review, assess test quality beyond just coverage numbers.

Missing coverage should be considered a warning rather than a blocker and should be evaluated in context.

Tests for contrib apps can be found in the tests/ directory, typically under <app_name>_tests. For example, tests for contrib.auth are located in tests/auth_tests.

Ensure you have the latest point release of a supported Python version, since there are often bugs in earlier versions that may cause the test suite to fail or hang.

On macOS (High Sierra and newer versions), you might see this message logged, after which the tests hang:

To avoid this set a OBJC_DISABLE_INITIALIZE_FORK_SAFETY environment variable, for example:

Or add export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES to your shell’s startup file (e.g. ~/.profile).

If the locales package is not installed, some tests will fail with a UnicodeEncodeError.

You can resolve this on Debian-based systems, for example, by running:

You can resolve this for macOS systems by configuring your shell’s locale:

Run the locale command to confirm the change. Optionally, add those export commands to your shell’s startup file (e.g. ~/.bashrc for Bash) to avoid having to retype them.

In case a test passes when run in isolation but fails within the whole suite, we have some tools to help analyze the problem.

The --bisect option of runtests.py will run the failing test while halving the test set it is run together with on each iteration, often making it possible to identify a small number of tests that may be related to the failure.

For example, suppose that the failing test that works on its own is ModelTest.test_eq, then using:

will try to determine a test that interferes with the given one. First, the test is run with the first half of the test suite. If a failure occurs, the first half of the test suite is split in two groups and each group is then run with the specified test. If there is no failure with the first half of the test suite, the second half of the test suite is run with the specified test and split appropriately as described earlier. The process repeats until the set of failing tests is minimized.

The --pair option runs the given test alongside every other test from the suite, letting you check if another test has side-effects that cause the failure. So:

will pair test_eq with every test label.

With both --bisect and --pair, if you already suspect which cases might be responsible for the failure, you may limit tests to be cross-analyzed by specifying further test labels after the first one:

You can also try running any set of tests in a random or reverse order using the --shuffle and --reverse options. This can help verify that executing tests in a different order does not cause any trouble:

If you wish to examine the SQL being run in failing tests, you can turn on SQL logging using the --debug-sql option. If you combine this with --verbosity=2, all SQL queries will be output:

By default tests are run in parallel with one process per core. When the tests are run in parallel, however, you’ll only see a truncated traceback for any test failures. You can adjust this behavior with the --parallel option:

You can also use the DJANGO_TEST_PROCESSES environment variable for this purpose.

To avoid polluting the global apps registry and prevent unnecessary table creation, models defined in a test method should be bound to a temporary Apps instance. To do this, use the isolate_apps() decorator:

Models defined in a test method with no explicit app_label are automatically assigned the label of the app in which their test class is located.

In order to make sure the models defined within the context of isolate_apps() instances are correctly installed, you should pass the set of targeted app_label as arguments:

---

## Working with Git and GitHub | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/internals/contributing/writing-code/working-with-git/

**Contents:**
- Working with Git and GitHub¶
- Installing Git¶
- Setting up local repository¶
- Working on a ticket¶
  - Publishing work¶
  - Editing commit messages¶
  - Rebasing branches¶
  - After upstream has changed¶
  - After review¶
- Working on a patch¶

This section explains how the community can contribute code to Django via pull requests. If you’re interested in how mergers handle them, see Handling pull requests.

Below, we are going to show how to create a GitHub pull request containing the changes for Trac ticket #xxxxx. By creating a fully-ready pull request, you will make the reviewer’s job easier, meaning that your work is more likely to be merged into Django.

You could also upload a traditional patch to Trac, but it’s less practical for reviews.

Django uses Git for its source control. You can download Git, but it’s often easier to install with your operating system’s package manager.

Django’s Git repository is hosted on GitHub, and it is recommended that you also work using GitHub.

After installing Git, the first thing you should do is set up your name and email:

Note that user.name should be your real name, not your GitHub nick. GitHub should know the email you use in the user.email field, as this will be used to associate your commits with your GitHub account.

When you have created your GitHub account, with the nick “GitHub_nick”, and forked Django’s repository, create a local copy of your fork:

This will create a new directory “django”, containing a clone of your GitHub repository. The rest of the git commands on this page need to be run within the cloned directory, so switch to it now:

Your GitHub repository will be called “origin” in Git.

You should also set up django/django as an “upstream” remote (that is, tell git that the reference Django repository was the source of your fork of it):

You can add other remotes similarly, for example:

When working on a ticket, create a new branch for the work, and base that work on upstream/main:

The -b flag creates a new branch for you locally. Don’t hesitate to create new branches even for the smallest things - that’s what they are there for.

If instead you were working for a fix on the 1.4 branch, you would do:

Assume the work is carried on the ticket_xxxxx branch. Make some changes and commit them:

When writing the commit message, follow the commit message guidelines to ease the work of the merger. If you’re uncomfortable with English, try at least to describe precisely what the commit does.

If you need to do additional work on your branch, commit as often as necessary:

You can publish your work on GitHub by running:

When you go to your GitHub page, you will notice a new branch has been created.

If you are working on a Trac ticket, you should mention in the ticket that your work is available from branch ticket_xxxxx of your GitHub repo. Include a link to your branch.

Note that the above branch is called a “topic branch” in Git parlance. You are free to rewrite the history of this branch, by using git rebase for example. Other people shouldn’t base their work on such a branch, because their clone would become corrupt when you edit commits.

There are also “public branches”. These are branches other people are supposed to fork, so the history of these branches should never change. Good examples of public branches are the main and stable/A.B.x branches in the django/django repository.

When you think your work is ready to be pulled into Django, you should create a pull request at GitHub. A good pull request means:

commits with one logical change in each, following the coding style,

well-formed messages for each commit: a summary line and then paragraphs wrapped at 72 characters thereafter – see the committing guidelines for more details,

documentation and tests, if needed – actually tests are always needed, except for documentation changes.

The test suite must pass and the documentation must build without warnings.

Once you have created your pull request, you should add a comment in the related Trac ticket explaining what you’ve done. In particular, you should note the environment in which you ran the tests, for instance: “all tests pass under SQLite and MySQL”.

Pull requests at GitHub have only two states: open and closed. The merger who will deal with your pull request has only two options: merge it or close it. For this reason, it isn’t useful to make a pull request until the code is ready for merging – or sufficiently close that a merger will finish it themselves.

To change the message of the most recent commit, run:

This opens an editor with the current commit message. Edit it, save, and close to update the commit.

To change the message of an earlier commit, use the “reword” option in interactive rebase. For example, to reword one of the last three commits:

This opens an editor listing the three commits, each prefixed with the word “pick”. Change “pick” to “reword” (or “r”) on the line of the commit you want to change, then save and close. A new editor will open for each commit marked as “reword”, allowing you to update the message.

See Committing guidelines for the required commit message format.

After rewriting a commit that has already been pushed to GitHub, you will need to force-push your branch:

In the example above, you created two commits, the “Fixed #xxxxx – …” commit and the “Added two more tests …” commit.

We do not want to have the entire history of your working process in your repository. Your commit “Added two more tests” would be unhelpful noise. Instead, we would rather only have one commit containing all your work.

To rework the history of your branch you can squash the commits into one by using interactive rebase:

The HEAD~2 above is shorthand for two latest commits. The above command will open an editor showing the two commits, prefixed with the word “pick”.

Change “pick” on the second line to “squash” instead. This will keep the first commit, and squash the second commit into the first one. Save and quit the editor. A second editor window should open, so you can reword the commit message for the commit now that it includes both your steps.

You can also use the “edit” option in rebase. This way you can change a single commit, for example to fix a typo in a docstring:

If your topic branch is already published at GitHub, for example if you’re making minor changes to take into account a review, you will need to force-push the changes:

Note that this will rewrite history of ticket_xxxxx - if you check the commit hashes before and after the operation at GitHub you will notice that the commit hashes do not match anymore. This is acceptable, as the branch is a topic branch, and nobody should be basing their work on it.

When upstream (django/django) has changed, you should rebase your work. To do this, use:

The work is automatically rebased using the branch you forked on, in the example case using upstream/main.

The rebase command removes all your local commits temporarily, applies the upstream commits, and then applies your local commits again on the work.

If there are merge conflicts, you will need to resolve them and then use git rebase --continue. At any point you can use git rebase --abort to return to the original state.

Note that you want to rebase on upstream, not merge the upstream.

The reason for this is that by rebasing, your commits will always be on top of the upstream’s work, not mixed in with the changes in the upstream. This way your branch will contain only commits related to its topic, which makes squashing easier.

It is unusual to get any non-trivial amount of code into core without changes requested by reviewers. In this case, it is often a good idea to add the changes as one incremental commit to your work. This allows the reviewer to easily check what changes you have done.

In this case, do the changes required by the reviewer. Commit as often as necessary. Before publishing the changes, rebase your work. If you added two commits, you would run:

Squash the second commit into the first. Write a commit message along the lines of:

Finally, push your work back to your GitHub repository. Since you didn’t touch the public commits during the rebase, you should not need to force-push:

Your pull request should now contain the new commit too.

Note that the merger is likely to squash the review commit into the previous commit when committing the code.

One of the ways that developers can contribute to Django is by reviewing patches. Those patches will typically exist as pull requests on GitHub and can be easily integrated into your local repository:

This will create a new branch and then apply the changes from the pull request to it. At this point you can run the tests or do anything else you need to do to investigate the quality of the patch.

For more detail on working with pull requests see the guidelines for mergers.

Work on GitHub if you can.

Announce your work on the Trac ticket by linking to your GitHub branch.

When you have something ready, make a pull request.

Make your pull requests as good as you can.

When doing fixes to your work, use git rebase -i to squash the commits.

When upstream has changed, do git fetch upstream; git rebase.

---

## Writing documentation | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/internals/contributing/writing-documentation/

**Contents:**
- Writing documentation¶
- The Django documentation process¶
- How the documentation is organized¶
- How to start contributing documentation¶
  - Clone the Django repository to your local machine¶
  - Set up a virtual environment and install dependencies¶
  - Build the documentation locally¶
  - Making edits to the documentation¶
  - Documentation quality checks¶
    - Spelling check¶

We place high importance on the consistency and readability of documentation. After all, Django was created in a journalism environment! So we treat our documentation like we treat our code: we aim to improve it as often as possible.

Documentation changes generally come in two forms:

General improvements: typo corrections, error fixes and better explanations through clearer writing and more examples.

New features: documentation of features that have been added to the framework since the last release.

This section explains how writers can craft their documentation changes in the most useful and least error-prone ways.

Though Django’s documentation is intended to be read as HTML at https://docs.djangoproject.com/, we edit it as a collection of plain text files written in the reStructuredText markup language for maximum flexibility.

We work from the development version of the repository because it has the latest-and-greatest documentation, just as it has the latest-and-greatest code.

We also backport documentation fixes and improvements, at the discretion of the merger, to the last release branch. This is because it’s advantageous to have the docs for the last release be up-to-date and correct (see Differences between versions).

Django’s documentation uses the Sphinx documentation system, which in turn is based on docutils. The basic idea is that lightly-formatted plain-text documentation is transformed into HTML, PDF, and any other output format.

Sphinx includes a sphinx-build command for turning reStructuredText into other formats, e.g., HTML and PDF. This command is configurable, but the Django documentation includes a Makefile that provides a shorter make html command.

The documentation is organized into several categories:

Tutorials take the reader by the hand through a series of steps to create something.

The important thing in a tutorial is to help the reader achieve something useful, preferably as early as possible, in order to give them confidence.

Explain the nature of the problem we’re solving, so that the reader understands what we’re trying to achieve. Don’t feel that you need to begin with explanations of how things work - what matters is what the reader does, not what you explain. It can be helpful to refer back to what you’ve done and explain afterward.

Topic guides aim to explain a concept or subject at a fairly high level.

Link to reference material rather than repeat it. Use examples and don’t be reluctant to explain things that seem very basic to you - it might be the explanation someone else needs.

Providing background context helps a newcomer connect the topic to things that they already know.

Reference guides contain technical references for APIs. They describe the functioning of Django’s internal machinery and instruct in its use.

Keep reference material tightly focused on the subject. Assume that the reader already understands the basic concepts involved but needs to know or be reminded of how Django does it.

Reference guides aren’t the place for general explanation. If you find yourself explaining basic concepts, you may want to move that material to a topic guide.

How-to guides are recipes that take the reader through steps in key subjects.

What matters most in a how-to guide is what a user wants to achieve. A how-to should always be result-oriented rather than focused on internal details of how Django implements whatever is being discussed.

These guides are more advanced than tutorials and assume some knowledge about how Django works. Assume that the reader has followed the tutorials and don’t hesitate to refer the reader back to the appropriate tutorial rather than repeat the same material.

If you’d like to start contributing to our docs, get the development version of Django from the source code repository (see Installing the development version):

If you’re planning to submit these changes, you might find it useful to make a fork of the Django repository and clone this fork instead.

Create and activate a virtual environment, then install the dependencies:

We can build HTML output from the docs directory:

Your locally-built documentation will be accessible at _build/html/index.html and it can be viewed in any web browser, though it will be themed differently than the documentation at docs.djangoproject.com. This is OK! If your changes look good on your local machine, they’ll look good on the website.

The source files are .txt files located in the docs/ directory.

These files are written in the reStructuredText markup language. To learn the markup, see the reStructuredText reference.

To edit this page, for example, we would edit the file docs/internals/contributing/writing-documentation.txt and rebuild the HTML with make html.

Several checks help maintain Django’s documentation quality, including spelling, code block formatting, and documentation style.

These checks are run automatically in CI and must pass before documentation changes can be merged. They can also be run locally with a single command:

This command runs all current checks and will include any new checks added in the future.

Before you commit your docs, it’s a good idea to run the spelling checker. You’ll need to install sphinxcontrib-spelling first. Then from the docs directory, run:

Wrong words (if any) along with the file and line number where they occur will be saved to _build/spelling/output.txt.

If you encounter false-positives (error output that actually is correct), do one of the following:

Surround inline code or brand/technology names with double grave accents (``)

Find synonyms that the spell checker recognizes.

If, and only if, you are sure the word you are using is correct - add it to docs/spelling_wordlist (please keep the list in alphabetical order).

All Python code blocks should be formatted using the blacken-docs auto-formatter. This is automatically run by the pre-commit hook if configured.

The check can also be run manually: provided that blacken-docs is installed, run the following command from the docs directory:

The formatter will report any issues by printing them to the terminal and will reformat code blocks where possible.

Django’s documentation is checked for reStructuredText style and formal issues using sphinx-lint. This helps catch problems like stray tabs, trailing whitespace, excessive line length, and similar formatting problems.

Once sphinx-lint is installed, the check can be run with the following command from the docs directory:

The command prints any violations to the terminal in the form path:line: message. If problems are encountered:

Read the message and fix the indicated issue (for example, remove trailing whitespace, adjust backticks, or replace tabs with spaces).

For long lines consider wrapping text onto new lines or breaking long inline links into named references. The custom line length check should already skip common false positives such as headings, tables and long links.

Links in documentation can become broken or changed such that they are no longer the canonical link. Sphinx provides a builder that can check whether the links in the documentation are working. From the docs directory, run:

Output is printed to the terminal, but can also be found in _build/linkcheck/output.txt and _build/linkcheck/output.json.

The execution of the command requires an internet connection and takes several minutes to complete, because the command tests all the links that are found in the documentation.

Entries that have a status of “working” are fine, those that are “unchecked” or “ignored” have been skipped because they either cannot be checked or have matched ignore rules in the configuration.

Entries that have a status of “broken” need to be fixed. Those that have a status of “redirected” may need to be updated to point to the canonical location, e.g. the scheme has changed http:// → https://. In certain cases, we do not want to update a “redirected” link, e.g. a rewrite to always point to the latest or stable version of the documentation, e.g. /en/stable/ → /en/3.2/.

When using pronouns in reference to a hypothetical person, such as “a user with a session cookie”, gender-neutral pronouns (they/their/them) should be used. Instead of:

him or her… use them.

his or her… use their.

his or hers… use theirs.

himself or herself… use themselves.

Try to avoid using words that minimize the difficulty involved in a task or operation, such as “easily”, “simply”, “just”, “merely”, “straightforward”, and so on. People’s experience may not match your expectations, and they may become frustrated when they do not find a step as “straightforward” or “simple” as it is implied to be.

Here are some style guidelines on commonly used terms throughout the documentation:

Django – when referring to the framework, capitalize Django. It is lowercase only in Python code and in the djangoproject.com logo.

HTTP – the expected pronunciation is “Aitch Tee Tee Pee” and therefore should be preceded by “an” and not “a”.

MySQL, PostgreSQL, SQLite

SQL – when referring to SQL, the expected pronunciation should be “Ess Queue Ell” and not “sequel”. Thus in a phrase like “Returns an SQL expression”, “SQL” should be preceded by “an” and not “a”.

Python – when referring to the language, capitalize Python.

realize, customize, initialize, etc. – use the American “ize” suffix, not “ise.”

subclass – it’s a single word without a hyphen, both as a verb (“subclass that model”) and as a noun (“create a subclass”).

the web, web framework – it’s not capitalized.

website – use one word, without capitalization.

model – it’s not capitalized.

template – it’s not capitalized.

URLconf – use three capitalized letters, with no space before “conf.”

view – it’s not capitalized.

These guidelines regulate the format of our reST (reStructuredText) documentation:

In section titles, capitalize only initial words and proper nouns.

Wrap the documentation at 80 characters wide, unless a code example is significantly less readable when split over two lines, or for another good reason.

The main thing to keep in mind as you write and edit docs is that the more semantic markup you can add the better. So:

Isn’t nearly as helpful as:

This is because Sphinx will generate proper links for the latter, which greatly helps readers.

You can prefix the target with a ~ (that’s a tilde) to get only the “last bit” of that path. So :mod:`~django.contrib.auth` will display a link with the title “auth”.

Use intersphinx to reference Python’s and Sphinx’ documentation.

Add .. code-block:: <lang> to literal blocks so that they get highlighted. Prefer relying on automatic highlighting using :: (two colons). This has the benefit that if the code contains some invalid syntax, it won’t be highlighted. Adding .. code-block:: python, for example, will force highlighting despite invalid syntax.

To improve readability, use .. admonition:: Descriptive title rather than .. note::. Use these boxes sparingly.

Use these heading styles:

Use :rfc: to reference a Request for Comments (RFC) and try to link to the relevant section if possible. For example, use :rfc:`2324#section-2.3.2` or :rfc:`Custom link text <2324#section-2.3.2>`.

Use :pep: to reference a Python Enhancement Proposal (PEP) and try to link to the relevant section if possible. For example, use :pep:`20#easter-egg` or :pep:`Easter Egg <20#easter-egg>`.

Use :mimetype: to refer to a MIME Type unless the value is quoted for a code example.

Use :envvar: to refer to an environment variable. You may also need to define a reference to the documentation for that environment variable using .. envvar::.

Use :cve: to reference a Common Vulnerabilities and Exposures (CVE) identifier. For example, use :cve:`2019-14232`.

When documenting Python objects (classes, methods, attributes, etc.) using Sphinx directives such as .. class::, .. method::, and .. attribute::, all content must be properly indented to ensure correct rendering and to support features like automatic table of contents generation.

The directive itself remains flush with the left margin (no indentation).

All descriptive text under the directive must be indented by 4 spaces.

Multi-line descriptions must keep the same indentation level.

Nested directives (for example, methods inside a class) require an additional 4 spaces of indentation to maintain hierarchy.

Field lists (such as :param:, :returns:, etc.) must align with the directive’s content level.

Besides Sphinx’s built-in markup, Django’s docs define some extra description units:

To link to a setting, use :setting:`INSTALLED_APPS`.

To link, use :ttag:`regroup`.

To link, use :tfilter:`linebreaksbr`.

Field lookups (i.e. Foo.objects.filter(bar__exact=whatever)):

To link, use :lookup:`exact`.

django-admin commands:

To link, use :djadmin:`migrate`.

django-admin command-line options:

To link, use :option:`command_name --traceback` (or omit command_name for the options shared by all commands like --verbosity).

Links to Trac tickets (typically reserved for patch release notes):

Django’s documentation uses a custom console directive for documenting command-line examples involving django-admin, manage.py, python, etc.). In the HTML documentation, it renders a two-tab UI, with one tab showing a Unix-style command prompt and a second tab showing a Windows prompt.

For example, you can replace this fragment:

You usually will replace occurrences of the .. code-block:: console directive.

You don’t need to change the actual content of the code example. You still write it assuming a Unix-y environment (i.e. a '$' prompt symbol, '/' as filesystem path components separator, etc.)

The example above will render a code example block with two tabs. The first one will show:

(No changes from what .. code-block:: console would have rendered).

The second one will show:

Our policy for new features is:

All documentation of new features should be written in a way that clearly designates the features that are only available in the Django development version. Assume documentation readers are using the latest release, not the development version.

Our preferred way for marking new features is by prefacing the features’ documentation with: “.. versionadded:: X.Y”, followed by a mandatory blank line and an optional description (indented).

General improvements or other changes to the APIs that should be emphasized should use the “.. versionchanged:: X.Y” directive (with the same format as the versionadded mentioned above.

These versionadded and versionchanged blocks should be “self-contained.” In other words, since we only keep these annotations around for two releases, it’s nice to be able to remove the annotation and its contents without having to reflow, reindent, or edit the surrounding text. For example, instead of putting the entire description of a new or changed feature in a block, do something like this:

Put the changed annotation notes at the bottom of a section, not the top.

Also, avoid referring to a specific version of Django outside a versionadded or versionchanged block. Even inside a block, it’s often redundant to do so as these annotations render as “New in Django A.B:” and “Changed in Django A.B”, respectively.

If a function, attribute, etc. is added, it’s also okay to use a versionadded annotation like this:

We can remove the .. versionadded:: A.B annotation without any indentation changes when the time comes.

Optimize image compression where possible. For PNG files, use OptiPNG and AdvanceCOMP’s advpng:

This is based on OptiPNG version 0.7.5. Older versions may complain about the -strip all option being lossy.

For a quick example of how it all fits together, consider this hypothetical example:

First, the ref/settings.txt document could have an overall layout like this:

Next, the topics/settings.txt document could contain something like this:

We use the Sphinx doc cross-reference element when we want to link to another document as a whole and the ref element when we want to link to an arbitrary location in a document.

Next, notice how the settings are annotated:

This marks up the following header as the “canonical” target for the setting ADMINS. This means any time I talk about ADMINS, I can reference it using :setting:`ADMINS`.

That’s basically how everything fits together.

See Localizing the Django documentation if you’d like to help translate the documentation into another language.

Sphinx can generate a manual page for the django-admin command. This is configured in docs/conf.py. Unlike other documentation output, this man page should be included in the Django repository and the releases as docs/man/django-admin.1. There isn’t a need to update this file when updating the documentation, as it’s updated once as part of the release process.

To generate an updated version of the man page, in the docs directory, run:

The new man page will be written in docs/_build/man/django-admin.1.

---

## Writing your first contribution for Django | Django documentation | Django

**URL:** https://docs.djangoproject.com/en/stable/intro/contributing/

**Contents:**
- Writing your first contribution for Django¶
- Introduction¶
  - Who’s this tutorial for?¶
  - What does this tutorial cover?¶
- Code of Conduct¶
- Installing Git¶
- Getting a copy of Django’s development version¶
- Running Django’s test suite for the first time¶
- Working on an approved new feature¶
- Creating a branch¶

Interested in giving back to the community a little? Maybe you’ve found a bug in Django that you’d like to see fixed, or maybe there’s a small feature you want added (but remember that proposals for new features should follow the process for suggesting new features).

Contributing back to Django itself is the best way to see your own concerns addressed. This may seem daunting at first, but it’s a well-traveled path with documentation, tooling, and a community to support you. We’ll walk you through the entire process, so you can learn by example.

If you are looking for a reference on the details of making code contributions, see the Contributing code documentation.

For this tutorial, we expect that you have at least a basic understanding of how Django works. This means you should be comfortable going through the existing tutorials on writing your first Django app. In addition, you should have a good understanding of Python itself. But if you don’t, Dive Into Python is a fantastic (and free) online book for beginning Python programmers.

Those of you who are unfamiliar with version control systems and Trac will find that this tutorial and its links include just enough information to get started. However, you’ll probably want to read some more about these different tools if you plan on contributing to Django regularly.

For the most part though, this tutorial tries to explain as much as possible, so that it can be of use to the widest audience.

If you’re having trouble going through this tutorial, please post a message on the Django Forum or drop by the Django Discord server to chat with other Django users who might be able to help.

We’ll be walking you through contributing to Django for the first time. By the end of this tutorial, you should have a basic understanding of both the tools and the processes involved. Specifically, we’ll be covering the following:

Downloading a copy of Django’s development version.

Running Django’s test suite.

Writing a test for your changes.

Writing the code for your changes.

Testing your changes.

Submitting a pull request.

Where to look for more information.

Once you’re done with the tutorial, you can look through the rest of Django’s documentation on contributing. It contains lots of great information and is a must read for anyone who’d like to become a regular contributor to Django. If you’ve got questions, it’s probably got the answers.

The current version of Django doesn’t support Python 2.7. Get Python 3 at Python’s download page or with your operating system’s package manager.

See Install Python on Windows docs for additional guidance.

As a contributor, you can help us keep the Django community open and inclusive. Please read and follow our Code of Conduct.

For this tutorial, you’ll need Git installed to download the current development version of Django and to generate a branch for the changes you make.

To check whether or not you have Git installed, enter git into the command line. If you get messages saying that this command could not be found, you’ll have to download and install it, see Git’s download page.

If you’re not that familiar with Git, you can always find out more about its commands (once it’s installed) by typing git help into the command line.

The first step to contributing to Django is to get a copy of the source code. First, fork Django on GitHub. Then, from the command line, use the cd command to navigate to the directory where you’ll want your local copy of Django to live.

Download the Django source code repository using the following command:

Low bandwidth connection?

You can add the --depth 1 argument to git clone to skip downloading all of Django’s commit history, which reduces data transfer from ~250 MB to ~70 MB.

Now that you have a local copy of Django, you can install it just like you would install any package using pip. The most convenient way to do so is by using a virtual environment, which is a feature built into Python that allows you to keep a separate directory of installed packages for each of your projects so that they don’t interfere with each other.

It’s a good idea to keep all your virtual environments in one place, for example in .virtualenvs/ in your home directory.

Create a new virtual environment by running:

The path is where the new environment will be saved on your computer.

The final step in setting up your virtual environment is to activate it:

If the source command is not available, you can try using a dot instead:

You have to activate the virtual environment whenever you open a new terminal window.

To activate your virtual environment on Windows, run:

The name of the currently activated virtual environment is displayed on the command line to help you keep track of which one you are using. Anything you install through pip while this name is displayed will be installed in that virtual environment, isolated from other environments and system-wide packages.

Go ahead and install the previously cloned copy of Django:

The installed version of Django is now pointing at your local copy by installing in editable mode. You will immediately see any changes you make to it, which is of great help when testing your first contribution.

When contributing to Django it’s very important that your code changes don’t introduce bugs into other areas of Django. One way to check that Django still works after you make your changes is by running Django’s test suite. If all the tests still pass, then you can be reasonably sure that your changes work and haven’t broken other parts of Django. If you’ve never run Django’s test suite before, it’s a good idea to run it once beforehand to get familiar with its output.

Before running the test suite, enter the Django tests/ directory using the cd tests command, and install test dependencies by running:

If you encounter an error during the installation, your system might be missing a dependency for one or more of the Python packages. Consult the failing package’s documentation or search the web with the error message that you encounter.

Now we are ready to run the test suite:

Now sit back and relax. Django’s entire test suite has thousands of tests, and it takes at least a few minutes to run, depending on the speed of your computer.

While Django’s test suite is running, you’ll see a stream of characters representing the status of each test as it completes. E indicates that an error was raised during a test, and F indicates that a test’s assertions failed. Both of these are considered to be test failures. Meanwhile, x and s indicate expected failures and skipped tests, respectively. Dots indicate passing tests.

Skipped tests are typically due to missing external libraries required to run the test; see Running all the tests for a list of dependencies and be sure to install any for tests related to the changes you are making (we won’t need any for this tutorial). Some tests are specific to a particular database backend and will be skipped if not testing with that backend. SQLite is the database backend for the default settings. To run the tests using a different backend, see Using another settings module.

Once the tests complete, you should be greeted with a message informing you whether the test suite passed or failed. Since you haven’t yet made any changes to Django’s code, the entire test suite should pass. If you get failures or errors make sure you’ve followed all of the previous steps properly. See Running the unit tests for more information.

Note that the latest Django “main” branch may not always be stable. When developing against “main”, you can check Django’s continuous integration builds to determine if the failures are specific to your machine or if they are also present in Django’s official builds. If you click to view a particular build, you can view the “Configuration Matrix” which shows failures broken down by Python version and database backend.

For this tutorial and the ticket we’re working on, testing against SQLite is sufficient, however, it’s possible (and sometimes necessary) to run the tests using a different database. When making UI changes, you will need to run the Selenium tests.

For this tutorial, we’ll work on a “fake accepted ticket” as a case study. Here are the imaginary details:

Ticket #99999 – Allow making toast

Django should provide a function django.shortcuts.make_toast() that returns 'toast'.

We’ll now implement this feature and associated tests.

Before making any changes, create a new branch for the ticket:

You can choose any name that you want for the branch, “ticket_99999” is an example. All changes made in this branch will be specific to the ticket and won’t affect the main copy of the code that we cloned earlier.

In most cases, for a contribution to be accepted into Django it has to include tests. For bug fix contributions, this means writing a regression test to ensure that the bug is never reintroduced into Django later on. A regression test should be written in such a way that it will fail while the bug still exists and pass once the bug has been fixed. For contributions containing new features, you’ll need to include tests which ensure that the new features are working correctly. They too should fail when the new feature is not present, and then pass once it has been implemented.

A good way to do this is to write your new tests first, before making any changes to the code. This style of development is called test-driven development and can be applied to both entire projects and single changes. After writing your tests, you then run them to make sure that they do indeed fail (since you haven’t fixed that bug or added that feature yet). If your new tests don’t fail, you’ll need to fix them so that they do. After all, a regression test that passes regardless of whether a bug is present is not very helpful at preventing that bug from reoccurring down the road.

Now for our hands-on example.

In order to resolve this ticket, we’ll add a make_toast() function to the django.shortcuts module. First we are going to write a test that tries to use the function and check that its output looks correct.

Navigate to Django’s tests/shortcuts/ folder and create a new file test_make_toast.py. Add the following code:

This test checks that the make_toast() returns 'toast'.

But this testing thing looks kinda hard…

If you’ve never had to deal with tests before, they can look a little hard to write at first glance. Fortunately, testing is a very big subject in computer programming, so there’s lots of information out there:

A good first look at writing tests for Django can be found in the documentation on Writing and running tests.

Dive Into Python (a free online book for beginning Python developers) includes a great introduction to Unit Testing.

After reading those, if you want something a little meatier to sink your teeth into, there’s always the Python unittest documentation.

Since we haven’t made any modifications to django.shortcuts yet, our test should fail. Let’s run all the tests in the shortcuts folder to make sure that’s really what happens. cd to the Django tests/ directory and run:

If the tests ran correctly, you should see one failure corresponding to the test method we added, with this error:

If all of the tests passed, then you’ll want to make sure that you added the new test shown above to the appropriate folder and file name.

Next we’ll be adding the make_toast() function.

Navigate to the django/ folder and open the shortcuts.py file. At the bottom, add:

Now we need to make sure that the test we wrote earlier passes, so we can see whether the code we added is working correctly. Again, navigate to the Django tests/ directory and run:

Everything should pass. If it doesn’t, make sure you correctly added the function to the correct file.

Once you’ve verified that your changes and test are working correctly, it’s a good idea to run the entire Django test suite to verify that your change hasn’t introduced any bugs into other areas of Django. While successfully passing the entire test suite doesn’t guarantee your code is bug free, it does help identify many bugs and regressions that might otherwise go unnoticed.

To run the entire Django test suite, cd into the Django tests/ directory and run:

This is a new feature, so it should be documented. Open the file docs/topics/http/shortcuts.txt and add the following at the end of the file:

Since this new feature will be in an upcoming release it is also added to the release notes for the next version of Django. Open the release notes for the latest version in docs/releases/, which at time of writing is 2.2.txt. Add a note under the “Minor Features” header:

For more information on writing documentation, including an explanation of what the versionadded bit is all about, see Writing documentation. That page also includes an explanation of how to build a copy of the documentation locally, so you can preview the HTML that will be generated.

Now it’s time to review the changes made in the branch. To stage all the changes ready for commit, run:

Then display the differences between your current copy of Django (with your changes) and the revision that you initially checked out earlier in the tutorial with:

Use the arrow keys to move up and down.

When you’re done previewing the changes, hit the q key to return to the command line. If the diff looked okay, it’s time to commit the changes.

To commit the changes:

This opens up a text editor to type the commit message. Follow the commit message guidelines and write a message like:

After committing the changes, send it to your fork on GitHub (substitute “ticket_99999” with the name of your branch if it’s different):

You can create a pull request by visiting the Django GitHub page. You’ll see your branch under “Your recently pushed branches”. Click “Compare & pull request” next to it.

Please don’t do it for this tutorial, but on the next page that displays a preview of the changes, you would click “Create pull request”.

Congratulations, you’ve learned how to make a pull request to Django! Details of more advanced techniques you may need are in Working with Git and GitHub.

Now you can put those skills to good use by helping to improve Django’s codebase.

Before you get too into contributing to Django, there’s a little more information on contributing that you should probably take a look at:

You should make sure to read Django’s documentation on claiming tickets and submitting pull requests. It covers Trac etiquette, how to claim tickets for yourself, expected coding style (both for code and docs), and many other important details.

First time contributors should also read Django’s documentation for first time contributors. It has lots of good advice for those of us who are new to helping out with Django.

After those, if you’re still hungry for more information about contributing, you can always browse through the rest of Django’s documentation on contributing. It contains a ton of useful information and should be your first source for answering any questions you might have.

Once you’ve looked through some of that information, you’ll be ready to go out and find a ticket of your own to contribute to. Pay special attention to tickets with the “easy pickings” criterion. These tickets are often much simpler in nature and are great for first time contributors. Once you’re familiar with contributing to Django, you can start working on more difficult and complicated tickets.

If you just want to get started already (and nobody would blame you!), try taking a look at the list of easy tickets without a branch and the easy tickets that have branches which need improvement. If you’re familiar with writing tests, you can also look at the list of easy tickets that need tests. Remember to follow the guidelines about claiming tickets that were mentioned in the link to Django’s documentation on claiming tickets and submitting branches.

After a ticket has a branch, it needs to be reviewed by a second set of eyes. After submitting a pull request, update the ticket metadata by setting the flags on the ticket to say “has patch”, “doesn’t need tests”, etc, so others can find it for review. Contributing doesn’t necessarily always mean writing code from scratch. Reviewing open pull requests is also a very helpful contribution. See Triaging tickets for details.

---
