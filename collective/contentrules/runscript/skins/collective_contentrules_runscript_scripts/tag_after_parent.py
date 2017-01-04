## Script (Python) "tag_after_parent"
##title=Tag after parent's title
##bind container=container
##bind context=context

#Adds the parent's title as a tag in the context's subject field.

pTag = context.aq_parent.Title()
keys = context.Subject()
if pTag not in keys:
    keys += (pTag,)
    context.setSubject(keys)
    context.reindexObject(idxs=['subject'])