## Controller Python Script "tag_after_parents"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Conditionally tags after parent's title
##
#Conditionally adds the parent's title as a tag in the context's subject field.
#Recursively tests whether title_as_tag property is set on each part of the object's parent's
#path and adds that part's title as a tag on the object.

pTags = list(context.Subject())

parent_path = context.aq_parent.absolute_url(True)
ppaths = parent_path.split('/')
for n, p in enumerate(ppaths):
    par = context.restrictedTraverse("/".join(ppaths[:n+1]))
    if par.getProperty('title_as_tag'):
        if par.Title() not in pTags:
            pTags.append(par.Title())

context.setSubject(tuple(pTags))
context.reindexObject(idxs=['subject'])
