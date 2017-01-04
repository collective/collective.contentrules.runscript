# -*- coding: utf-8 -*-
import unittest

from zope.interface import implementer, Interface
from zope.component import getUtility, getMultiAdapter
from zope.component.interfaces import IObjectEvent

from plone import api
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting, FunctionalTesting
from plone.app.testing.bbb import PloneTestCase
from plone.app.testing import TEST_USER_ID, setRoles

from plone.contentrules.rule.interfaces import IRuleAction, IExecutable
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.app.contentrules.rule import Rule

import collective.contentrules.runscript
from .actions.interfaces import IRunScriptAction
from .actions.runscript import RunScriptAction, RunScriptEditFormView



RS_FIXTURE = PloneWithPackageLayer(
    zcml_package=collective.contentrules.runscript,
    zcml_filename="configure.zcml",
    gs_profile_id='collective.contentrules.runscript:default',
    name='RunScript Layer'
)

RS_INTEGRATION_TESTING = IntegrationTesting(bases=(RS_FIXTURE,), name="collective.contentrules.RunScript:Integration")


@implementer(IObjectEvent)
class DummyEvent(object):
    def __init__(self, obj):
        self.object = obj


class TestRunScriptAction(unittest.TestCase):
    layer = RS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        # fix for *** ValueError: No such content type: Folder
        if api.env.plone_version().startswith("5"):
            self.portal.portal_quickinstaller.installProduct("plone.app.contenttypes")

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Document', 'd1')
        setRoles(self.portal, TEST_USER_ID, ['Member'])

    def testRegistered(self):
        element = getUtility(IRuleAction, name='collective.contentrules.RunScriptAction')
        self.assertEqual('collective.contentrules.RunScript.AddFormView', element.addview)
        self.assertEqual('edit', element.editview)
        self.assertEqual(None, element.for_)
        self.assertEqual(IObjectEvent, element.event)

    def testInvokeAddView(self):
        element = getUtility(IRuleAction, name='collective.contentrules.RunScriptAction')
        storage = getUtility(IRuleStorage)
        storage[u'foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')

        adding = getMultiAdapter((rule, self.portal.REQUEST), name='+action')
        addview = getMultiAdapter((adding, self.portal.REQUEST), name=element.addview)

        action = addview.createAndAdd(data={
            'script': 'bar',
            'parameters': [('a', 'b'), ('d','e')],
            'fail_on_script_not_found': True,
            'restricted_traverse': True
        })

        self.assertTrue(action is rule.actions[0])
        self.assertTrue(isinstance(action, RunScriptAction))
        self.assertEqual(action.script, 'bar')

    def testInvokeEditView(self):
        element = getUtility(IRuleAction, name='collective.contentrules.RunScriptAction')
        e = RunScriptAction()
        editview = getMultiAdapter((e, self.portal.REQUEST), name=element.editview)
        self.assertTrue(isinstance(editview, RunScriptEditFormView))

    def testExecute(self):
        a = RunScriptAction()
        a.script = 'foobar'
        a.parameters = ['a', 123]
        a.fail_on_script_not_found = True
        a.restricted_traverse = True
        ex = getMultiAdapter((self.portal, a, DummyEvent(self.portal.d1)), IExecutable)
        self.assertTrue(ex())
