## Script (Python) "set_property"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=name,value,type
##title=Set property
##
#Adds a new property to the context object or just sets an existing one
#Types must be the same in the latter case.

if context.getProperty(name) is None:
    context.manage_addProperty(name,value,type)
else:
    context.manage_changeProperties({name:value})
