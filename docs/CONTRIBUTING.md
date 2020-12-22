# Contributing to the RAMS ToolKit (RAMSTK)

Thank you for taking the time to contribute!

The following is a set of guidelines for contributing to RAMSTK, which is hosted in the [RAMSTK repository](https://github.com/ReliaQualAssociates/ramstk) on GitHub.  Feel free to propose changes to this document in a pull request.

[Code of Conduct](#code-of-conduct)

[How Can I Contribute?](#how-can-i-contribute)
  * [For Everyone](#for-everyone)
      * [Reporting Issues](#reporting-issues)
      * [Suggesting Enhancements](#suggesting-enhancements)
  * [For Developers' Eyes Only](#for-developers-eyes-only)
      * [Style Guidelines](#style-guidlines)
      * [Process Guidelines](#process-guidelines)


## Code of Conduct

The fundamental rules are:

* **DON'T be a Gavin Belson.**  You probably are smarter and more successful than everone else, but be humble and helpful.
* **DON'T be a Jian Yang.**  Stealing other people's IP is lower than a snake's belly.
* You *CAN* be a Bertram Gilfoyle, that's fundamentally just being an engineer.
* You *CAN* be a Big Head, but only if you invite me to all your house parties.
* You *CAN* be an Erlich Bachman because the world needs dreamers.
* You *CAN* be a Richard Hendricks, because ethical software is a good thing.
* You *CAN* be a Dinesh Chugtai because every team needs someone to good-heartedly pick on.

See the Code of Conduct file in the root `RAMSTK` directory.

## How Can I Contribute?

## For Everyone

#### Reporting Issues

> The only dumb issue is the unreported issue.

The purpose of an issue (or bug, condition, corrective action, FRACA) tracking system is to document **conditions adverse to quality (CAQ)** and their fixes.  A mispelled word in documentation or a docstring is a condition adverse to quality so *submit an issue*.  This section guides you through submitting an issue report for RAMSTK.  Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.

#### Before Submitting an Issue Report

**Perform a search** to see if the problem has already been reported.  If it has **and the issue is still open**, add a comment to the existing issue instead of opening a new one.

#### How to Submit a Useful Issue Report

Issues are tracked as [GitHub issues](https://github.com/ReliaQualAssociates/ramstk/issues/).

**Use a clear and descriptive title** for the issue to identify the problem.  When you create a new issue, you will be presented with an [issue template](https://github.com/ReliaQualAssociates/.github/ISSUE_TEMPLATE/ISSUE_TEMPLATE.md).  Please use the template to report your issue.  If you choose not to, you may be asked to provide the information requested or your issue may simply be closed with no action taken.

There are four sections in an issue report:

* Expected Behavior
* Actual Behavior
* Steps to Reproduce the Problem
* Operating Environment

In the **Expected Behavior** section, the minimum information needed is to
complete the user story:

    As a <type of RAMSTK stakeholder>, I want <goal> so that <need for goal>.

It is important that the voice of the customer (VOC) be captured up front.  The
VOC statement(s) are converted to engineering requirements.  Engineering
requirements can be tested to verify the code meets the requirement.  A simple
way to capture the VOC is to fill in the following statement.  You may include
multiple, related, user statements in a single issue.

RAMSTK has been a long time in the making and was originally created to bundle
together several small (mostly) Excel-based tools and move data storage to a
database rather than a spreadsheet.  As such, the design process was not very
rigorous and no engineering specifications were ever created; I knew what I
wanted my tool to do for me and didn't need to document that.  You're welcome
to call me lazy, but your user story (stakeholder's input in RAMSTK vernacular)
will be used to develop engineering specifications for RAMSTK.  In fact, you
can submit an issure report as a quality type issue and provide nothing more
than the completed user story (stakeholder input).  Not all users
(stakeholders) are external users of RAMSTK.

If submitting an enhancement type issue, provide a step-by-step description of
the suggested enhancement in as many details as possible.  Explain why this
enhancement would be useful to most RAMSTK users.

In the **Actual Behavior** section, **describe the behavior you observed** and
point out what exactly is the problem with that behavior.  If the problem
wasn't triggered by a specific action, describe what you were doing before the
problem happened.

The **Steps to Reproduce the Problem** section only needs to be completed for
an issue classified as a bug.  Quality, enhancement, and question type issues
by their nature are not reproducible.  When completing this section:

* **Describe the exact steps which reproduce the problem** in as many details as possible; **don't just say what you did, but explain how you did it**. For example, if you moved the cursor to the end of a line, explain if you used the mouse, or a keyboard shortcut.
* **Provide specific examples to demonstrate the steps**. Include links to files or GitHub projects, or copy/pasteable snippets, which you use in those examples.  If you're providing snippets in the issue, use [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* **Include screenshots and animated GIFs** which show you following the described steps and clearly demonstrate the problem.  You can use [this tool](https://www.cockos.com/licecap/) to record GIFs on Windows, and [this tool](https://github.com/colinkeenan/silentcast) or [this tool](https://github.com/GNOME/byzanz) on Linux.

To gather the information required for the **Operating Environment** section, execute something such as the following to get the required run-time package versions for the list.  You will need a copy of the [requirements_run.txt](https://github.com/ReliaQualAssociates/ramstk/requirements_run.txt) file in the repository.

```
for file in $(cat requirements_run.txt | cut -d '=' -f1 | cut -d '>' -f1);
do
    version=$(pip show $file | grep Version: | cut -d ':' -f2 | tr -d '[:space:]');
    echo "  * "$file==$version;
done
```

## For Developers' Eyes Only

As a RAMSTK developer, if you are working on something outside the RAMSTK issue system, you are likely working on the wrong thing.  If an issue doesn't exist, create it *before* you start writing.  The issue system is there to facilitate managing the development program and creating schedules.

### Style Guidelines

Please refer to the RAMSTK [coding conventions](https://github.com/ReliaQualAssociates/ramstk/blob/develop/docs/CODING_STDS.md).

#### Pull Requests

* Do not include issue numbers in the PR title.
* Include screenshots and animated GIFs in your pull request whenever possible.
* Document new engineering specification(s).
* Document new code.
* End all files with a newline.
* Avoid platform-dependent code.

#### Git Commit Messages

There is a commit message template in the root directory for RAMSTK named .gitcommitmessage.txt.  Use this template to build commit messages.

#### Always Add Descriptive Log Messages

Log messages should be understandable to someone who sees only the log. They shouldn't depend on information outside the context of the commit. Try to put the log messages only to those files which are really affected by the change described in the log message.

In particular put all important information which can't be seen from the diff in the log message.

#### Use Issue System Numbers

Add the bug number to the log message. In order to keep the issue tracking system in sync with the git repositories, you should reference the issue report in your commits, and close the fixed issues in the issue tracking system.

This doesn't mean that you don't need an understandable log message.  It should be clear from the log message what has been changed without looking at the issue report.

#### TODO Comments

When working on an issue, pull request, etc., you very well may find a section of code that needs work.  If this section of code is within the scope of your work, make the changes.  If it is out of scope, add a TODO comment using the following format:

    # // TODO: <One-line description of required work.
    # //
    # // Long and detailed description of work to be performed.

The github action, dtinth/todo-actions will find these TODO comments when code is pushed to the develop or master branch and convert them to an issue.  We believe it is more efficient to identify issues and document them in-line while working rather than having to stop and open an issue.  This results in better issue management.

### Process Guidelines

RAMSTK uses:

* SCRUM workflow
* Test driven development
* Continuous integration
* The git-flow branching model

#### Never Write a Test That Doesn't Have an Engineering Specification

It's not necessary to create a user story (stakeholder input) prior to writing an engineering specification, but it is perfectly acceptable to do so.  As a developer, you may simply write the engineering specification.  If working on an issue reported by a stakeholder, convert their user story to an engineering specification.  Communicate with the stakeholder who reported the issue if you need clarification.  This process helps identify epics versus simple user stories and will result in a better product and happier users (developers will be happier too).

A test does not need to be code executable by pytest.  It may be a step by step procedure or checklist.  This would be appropriate for GUI design/layout related specifications where it would be more efficient to simply launch RAMSTK and visually inspect that the specification is met.

#### Never Write Code That Doesn't Have a Test

And make sure the test(s) pass before committing.  If you add functionality to RAMSTK, there should be one or more tests for the new functionality.  There should be a test(s) to ensure the new code works with good inputs.  There should also be test(s) to ensure the code responds properly with bad inputs.

#### Never Commit Code That Doesn't Run

Run the code and correct all errors before committing.  Make sure that newly added files are committed.  If they are missing your local copy will run fine but nobody else will be able to run RAMSTK.  This is not desirable.

#### Always Statically Check Your Code

Statically check every file you edit between commits.  At a minimum, the following static checkers should be used:

* isort
* yapf
* pylint
* pycodestyle
* pydocstyle
* bandit

The RunTests.py file in the tests directory can be used to integrate these checkers with your editor/IDE if needed.  Depending on your editor/IDE and prefered workflow, you might have some or all run automatically as you code.  My preference is code, static check periodically, and fix the errors/warnings raised.  When using pylint, the goal is not to acheive a score of 10/10, it is to create standard, maintainable code.  You are encouraged to aggressively refactor any code.  At a minimum, submit a quality type issue describing the proposed refactoring for you or another developer to work on later.

#### Double Check Before You Create a Pull Request

Do a ```git pull --rebase``` to keep your checkout up-to-date. Invoke ```git diff``` before committing. Take messages from git about conflicts, unknown files, etc. seriously. ```git diff``` will tell you exactly what you will be committing.  Check if that's really what you intended to commit.

#### Code Review by Other Developers

Don't commit changes to the public API of RAMSTK without prior review by other developers.  Requiring a review for these changes is intended to avoid problems for the users of the APIs and to improve the quality of the APIs.  This is ensured by using pull requests when you're ready to commit; the pull request will be merged by a developer with the authority to merge it.

#### Don't Create a Pull Request for Code You Don't Understand

Avoid things like "I don't know why it crashes, but when I do this, it does not crash anymore." or "I'm not completely sure if that's right, but at least it works for me.".

If you don't find a solution to a problem, discuss it with other developers.  Don't create a pull request if other developers disagree  If there are disagreements over code changes, these should be resolved by discussing them.

#### Commit Complete Changesets

git has the ability to commit more than one file at a time. Therefore, please commit all related changes in multiple files, even if they span over multiple directories at the same time in the same commit. This way, you ensure that git stays in a runnable state before and after the commit and that the commit history is more helpful.

Commits should be preferably "atomic" - not splittable. That means that every issuefix, feature, refactoring or reformatting should go into an own commit. This, too, improves the readability of the history.  Additionally, it makes porting changes between branches (cherry-picking) and finding faulty commits (by bisecting) simpler.
