from OFS.SimpleItem import SimpleItem
from Products.CMFPlone.utils import safe_unicode
from collective.contentrules.runscript import runscriptMessageFactory as _
from collective.contentrules.runscript.actions.interfaces import \
    IRunScriptAction
from plone.app.contentrules.browser.formhelper import AddForm
from plone.app.contentrules.browser.formhelper import EditForm
from plone.contentrules.rule.interfaces import IRuleElementData, IExecutable
from zope.component import adapts
from zope.formlib import form
from zope.interface import Interface, implements


class ScriptNotFound(Exception):
    def __init__(self, script, obj_url):
        self.script = script
        self.obj_url = obj_url

    def __str__(self):
        return 'Could not traverse from "%s" to "%s".' % (self.obj_url, self.script)


class RunScriptAction(SimpleItem):
    """
    The persistent implementation of the action defined in IRunScriptAction
    """
    implements(IRunScriptAction, IRuleElementData)

    script = '' #unicode paths are not allowed
    fail_on_script_not_found = True
    restricted_traverse = False
    parameters = {}

    element = 'collective.contentrules.runscript.ApplyRunScript'

    @property
    def summary(self):
        return _(u"Run script '${script}' on the object.", mapping=dict(script=self.script))


class RunScriptActionExecutor(object):
    """The executor for this action.
    """
    implements(IExecutable)
    adapts(Interface, IRunScriptAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):

        obj = self.event.object
        event_title = safe_unicode(obj.Title())
        event_url = obj.absolute_url()

        if self.element.restricted_traverse:
            getScript = obj.restrictedTraverse
        else:
            getScript = obj.unrestrictedTraverse

        try:
            script = getScript(str(self.element.script))
        except AttributeError:
            if self.element.fail_on_script_not_found:
                raise ScriptNotFound(self.element.script, event_url)
                return False
            else:
                return True
        params = dict([(str(p.name), p.value) for p in self.element.parameters])
        script(**params)

        return True


class RunScriptAddForm(AddForm):
    """
    An add form for the RunScript action
    """
    form_fields = form.FormFields(IRunScriptAction)
    schema = IRunScriptAction
    label = _(u"Add RunScript Action")
    description = _(u"An action that can run a script on the object")
    form_name = _(u"Run Script")

    def create(self, data):
        a = RunScriptAction()
        form.applyChanges(a, self.form_fields, data)
        return a


class RunScriptEditForm(EditForm):
    """
    An edit form for the RunScript action
    """
    schema = IRunScriptAction
    label = _(u"Edit RunScript Action")
    description = _(u"An action that can run a script on the object")
    form_name = _(u"Configure element")



