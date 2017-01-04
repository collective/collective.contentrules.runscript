Introduction
============

Content rules are a powerfull feature in Plone 3. But create a filesystem product for every single little action
we'd like to perform seems a little overkill. To help those integrators and administrators out there, RunScript 
brings the ability to register a condition that once matched will perform whatever the action you state in a 
script configured in the Rule configuration form.

Just to meet a few use cases, the product brings a some sample scripts that might come in handy:

tag_after_parent

    Adds the parent's title as a tag to the item (appends to the subject field).
    E.g.::
        
        Given the structure: Plone/Folder1/Folder2/Folder3/object
        >> object.Subject()
        ()
        After Plone/Folder1/Folder2/Folder3/object/tag_after_parent
        >> object.Subject()
        ('Folder3',)
        

tag_after_parents
    Conditionally adds parent's title as tags to the item (appends to the subject field).
    Recursively tests whether title_as_tag property is set on each part of the object's parent's path and adds that 
    part's title as a tag on the object.
    E.g.:: 
        
        Given the structure: Plone/Folder1/Folder2/Folder3/object
        Plone.title_as_tag is undefined
        Folder1.title_as_tag is False
        Folder2.title_as_tag is True
        Folder3.title_as_tag is True
        >> object.Subject()
        ()
        After Plone/Folder1/Folder2/Folder3/object/tag_after_parents 
        >> object.Subject()
        ('Folder2','Folder3')

set_property
    Adds a new property to the context object or just sets an existing one.
    Types must be the same in the latter case.
    Parameters are name,value,type.
    E.g.::
        
        Given the structure: Plone/Folder1/Folder2/Folder3
        After Plone/Folder1/Folder2/Folder3/set_property?name=title_as_tag&value=True&type=boolean
        >> Plone.Folder1.Folder2.Folder3.getProperty('title_as_tag') == True
        True
    
others_might_come_in_the_future

    You can give your suggestions.

One could easily write a new script that just needs to be traversable from the object that will trigger 
the condition.


Installation
============

Add collective.contentrules.runscript to your buildout as an egg or
from source. No (generic setup) installation is necessary, the action is 
registered using ZCML. So do add the package to the zcml slug list of your
[instance] section.

If you'd like to use any of the available sample scripts then you should install the product by the 
Addons configlet.


Usage
=====

Go to the Plone Control Panel, select Content Rules and add a new Rule. 
Under 'actions' you now have a new option: Run Script.

In the 'Configure element' form, point to a script that knows how to perform the desired action upon the object 
that will trigger the rule.

If you installed the sample scripts, you could use the 'tag_after_parent' script and have every object matching 
the rule's condition categorized by their parent's title.

If the script you inform at the configuration form is not traversable from the object that triggered the rule 
an exception will or will not be thrown depending on the state of the 'Fail on script not found' flag.

If you set the rule to an 'add to container' event, not finding the script means not fullfilling the add.


Credits
=======

This package has been highly based on collective.contentrules.mailtolocalrole.

