# Simple CRM

### World's simplest, fastest, most usable CRM — via Alfred

**The problem with most CRMs...**

✘  Hassle to load an app  
✘  Too long to log in online  
✘  Too slow to add new contacts  
✘  Too cumbersome to find existing ones  
✘  And more features than most users need

**But with Simple CRM...** 

**✓**  Load immediately, thanks to Alfred  
**✓**  Add new contacts — blazingly simple & fast  
**✓**  Find them — even faster  
**✓**  Use tags to filter in infinite ways  
**✓**  Use your favorite editor for all contacts file  
**✓**  Save any search using the `enter` key  
**✓**  Smart Icons for lead status & more *(completely configurable)*

**More...**

**Simple CRM is a (super) lightweight, workflow built around files**. You open & edit these files with your favorite editor. This workflow makes it easy & fast to define, add, tag, find &  view contacts. And has tools to import, export & backup all your contacts. 

Simple CRM is built for power users, freelancers & anyone wanting less — to do more.

Give it a shot. Tell me what ya like. And what sucks. I'll make it un-suck.

## Usage

### Set up

Got existing contacts in your current CRM? Cool. Import them into Simple CRM.

- Export contacts to a .csv file
- Define your fields in Simple CRM via `Configure Workflow`
- Set  `CRM path` for all contact files
- Set the `import` & `export` paths & `export` fields
- Select `Import contacts` from Simple CRM `utilities` 

Voila. A new file created for each contact.

### Tags

**Tags provide mucho power to categorize your leads.** They save you from having to create & complete too many fields too. And making search *real* easy. And fast! [See more about tags & icons](#tags--icons).

## Main workflows

![](assets/crm.png)  

### ▸ Add new contact

Adding contacts is as simple as it gets. Start typing to add a new contact, using a subset of fields defined in `Configure Workflow`. And informing you which field you're currently entering *(in CAPs)*. Fill in any or all fields.


![](assets/crma.png) 

<kbd>↵</kbd>  To create new contact file in your CRM folder

<kbd>⌘</kbd><kbd>↵</kbd> To create new contact file — then open for further editing

### ▸ List & Search contacts

Imagine finding *any contact* in seconds. And finding *a set of contacts* in few seconds more. Simple CRM was built for this.

#### List Contacts

List all contacts, ready for filtering.

![](assets/crml.png)   

<kbd>↵</kbd> To open selected contact in your editor

#### Search contacts

Combine tags or any search fields *(as defined in `Configure Workflow`)* to filter rows — using basic AND/OR logic. This is the most powerful feature in Simple CRM. [See more filtering examples & rules](#Search-Filter-Rules).

![](assets/crml1.png)   

![](assets/crml2.png)   

![](assets/crml3.png)   

#### For 1st row

<kbd>↵</kbd> To save currently applied filtering as a `saved search`

<kbd>⌘</kbd><kbd>↵</kbd> To perform bulk update for all filtered contacts

<kbd>⌘</kbd><kbd>⌥</kbd> To open contact files for all filtered contacts

#### For all contact rows

<kbd>↵</kbd> To open contact file for currently select contact

#### Universal Actions

Key Universal actions include: 

**For 1st row:** 

`Search in Finder` - Show all currently filtered contacts in Finder

**For all contact rows**

`View in Alfred` | `Open`  | `Reveal in Finder`  | `Delete`

### ▸ Run a saved search

Save any filtered contacts from above to a saved search.

![](assets/crmss.png)  

<kbd>↵</kbd> To run this search

<kbd>⌘</kbd><kbd>↵</kbd> To remove this search

### ▸ List recent contacts

List the most recently opened contact files.

![](assets/crmr.png)    

<kbd>↵</kbd> To open selected contact file

---

### Tags & Icons

**Symbols allow for quick recognition for all contact rows.** I created out-of-the-box icons below for the specified tags. This is completely configurable by adding or changing icons in the `/icons` folder. The workflow will automatically assign tags with icons *(if they exist)*, for example: `@meeting` will display `meeting.png`.

**Combine tags to tell the story for each contact:**  ex. `@hot @lead` ***Note:** The 1st tag listed determines the icon to be used in the field `Tags:`.* Use any tag you think of as you go — there are no limitations.

**A list of tags & associated icons below** —with more coming!

 `@active` `@awaitingpayment` `@cold` `@deciding` `@followup` `@hot` `@lead` `@loss` `@meeting` `@past` `@meh` `@pause` `@ping` `@reminder` `@waiting` `@won`

![](assets/icons.png)  

❗**Note:** You must define the field, `Tags:` in `Configure Workflow`  to display these or any custom icons for contacts.

### Search Filter Rules

**AND by default**  
 `@lead @followup @active` → matches items with all 3 tags

**OR logic**  
 `@hot OR @cold OR @pause` → matches any of the tags

**NOT logic**  
 `@ping OR @waiting !@past` → matches ping or waiting, but excludes past  
 `@lead -@loss` → matches @lead but excludes @loss

**Phrases**  
 `"awaiting payment" OR @reminder` → matches the exact phrase or @reminder

All searches are case-insensitive.

### Utilities

Some useful tools to manage your contact files. And to peek into your data and workflow folders.

![](assets/crmu.png)    



