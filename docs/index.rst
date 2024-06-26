Configuration Container
=======================

.. autoclass:: enhomie.config.Config
   :members:
   :show-inheritance:
   :noindex:

Parameters Container
====================

.. autopydantic_model:: enhomie.config.Params
   :members:
   :show-inheritance:
   :noindex:

Homie Automate
==============

.. autoclass:: enhomie.homie.Homie
   :members:
   :show-inheritance:
   :noindex:

Homie Desired State
===================

.. autoclass:: enhomie.homie.HomieDesire
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enhomie.homie.HomieDesireParams
   :members:
   :show-inheritance:
   :noindex:

Homie Universal Group
=====================

.. autoclass:: enhomie.homie.HomieGroup
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enhomie.homie.HomieGroupParams
   :members:
   :show-inheritance:
   :noindex:

Homie Universal Scene
=====================

.. autoclass:: enhomie.homie.HomieScene
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enhomie.homie.HomieSceneParams
   :members:
   :show-inheritance:
   :noindex:

Philips Hue Bridge
==================

.. autoclass:: enhomie.philipshue.PhueBridge
   :members:
   :show-inheritance:
   :noindex:

Philips Hue Device
==================

.. autoclass:: enhomie.philipshue.PhueDevice
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enhomie.philipshue.PhueDeviceParams
   :members:
   :show-inheritance:
   :noindex:

Ubiquiti Router
===============

.. autoclass:: enhomie.ubiquiti.UbiqRouter
   :members:
   :show-inheritance:
   :noindex:

Ubiquiti Client
===============

.. autoclass:: enhomie.ubiquiti.UbiqClient
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enhomie.ubiquiti.UbiqClientParams
   :members:
   :show-inheritance:
   :noindex:

Conditional Parameters
======================

.. autoclass:: enhomie.homie.HomieWhen
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enhomie.homie.HomieWhenParams
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enhomie.builtins.WhenTimePeriodParams
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enhomie.philipshue.WhenPhueChangeParams
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enhomie.philipshue.WhenPhueSceneParams
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enhomie.ubiquiti.WhenUbiqClientParams
   :members:
   :show-inheritance:
   :noindex:

Conditional Helpers
===================

.. autofunction:: enhomie.builtins.chck_time_period
   :noindex:

.. autofunction:: enhomie.builtins.when_time_period
   :noindex:

.. autofunction:: enhomie.philipshue.chck_phue_change
   :noindex:

.. autofunction:: enhomie.philipshue.when_phue_change
   :noindex:

.. autofunction:: enhomie.philipshue.chck_phue_scene
   :noindex:

.. autofunction:: enhomie.philipshue.when_phue_scene
   :noindex:

.. autofunction:: enhomie.ubiquiti.chck_ubiq_client
   :noindex:

.. autofunction:: enhomie.ubiquiti.when_ubiq_client
   :noindex:

Operational Parameters
======================

.. autoclass:: enhomie.homie.HomieWhat
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enhomie.homie.HomieWhatParams
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enhomie.philipshue.WhatPhueMotionParams
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enhomie.philipshue.WhatPhueButtonParams
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enhomie.philipshue.WhatPhueContactParams
   :members:
   :show-inheritance:
   :noindex:

Operational Helpers
===================

.. autofunction:: enhomie.philipshue.chck_phue_motion
   :noindex:

.. autofunction:: enhomie.philipshue.what_phue_motion
   :noindex:

.. autofunction:: enhomie.philipshue.chck_phue_button
   :noindex:

.. autofunction:: enhomie.philipshue.what_phue_button
   :noindex:

.. autofunction:: enhomie.philipshue.chck_phue_contact
   :noindex:

.. autofunction:: enhomie.philipshue.what_phue_contact
   :noindex:
