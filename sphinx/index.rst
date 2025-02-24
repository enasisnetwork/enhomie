Enasis Network Homie Automate
=============================

Configuration Container
-----------------------

.. autoclass:: enhomie.homie.HomieConfig
   :members:
   :show-inheritance:
   :noindex:

Parameters Container
--------------------

.. autopydantic_model:: enhomie.homie.params.HomieParams
   :members:
   :show-inheritance:
   :noindex:

Homie Children
--------------

.. autopydantic_model:: enhomie.homie.params.HomieOriginParams
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enhomie.homie.params.HomieDeviceParams
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enhomie.homie.params.HomieGroupParams
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enhomie.homie.params.HomieSceneParams
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enhomie.homie.params.HomieDesireParams
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enhomie.homie.params.HomieAspireParams
   :members:
   :show-inheritance:
   :noindex:

Persistent Defaults
-------------------

.. autopydantic_model:: enhomie.homie.params.HomiePersistParams
   :members:
   :show-inheritance:
   :noindex:

Multithread Service
-------------------

.. autopydantic_model:: enhomie.homie.params.HomieServiceParams
   :members:
   :show-inheritance:
   :noindex:

Hubitat Origin
--------------

.. autopydantic_model:: enhomie.hubitat.params.HubiOriginParams
   :members:
   :show-inheritance:
   :noindex:

Philips Origin
--------------

.. autopydantic_model:: enhomie.philips.params.PhueOriginParams
   :members:
   :show-inheritance:
   :noindex:

Ubiquiti Origin
---------------

.. autopydantic_model:: enhomie.ubiquiti.params.UbiqOriginParams
   :members:
   :show-inheritance:
   :noindex:

Builtin Plugins
---------------

.. autopydantic_model:: enhomie.builtins.params.DriverBltnPeriodParams
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enhomie.builtins.params.DriverBltnRegexpParams
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enhomie.builtins.params.DriverBltnStoreParams
   :members:
   :show-inheritance:
   :noindex:

Philips Plugins
---------------

.. autopydantic_model:: enhomie.philips.params.DriverPhueButtonParams
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enhomie.philips.params.DriverPhueChangeParams
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enhomie.philips.params.DriverPhueContactParams
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enhomie.philips.params.DriverPhueMotionParams
   :members:
   :show-inheritance:
   :noindex:

.. autopydantic_model:: enhomie.philips.params.DriverPhueSceneParams
   :members:
   :show-inheritance:
   :noindex:

Philips Helpers
---------------

.. autofunction:: enhomie.philips.plugins.phue_sensors
   :noindex:

.. autofunction:: enhomie.philips.plugins.phue_changed
   :noindex:

.. autofunction:: enhomie.philips.plugins.phue_current
   :noindex:

Ubiquiti Plugins
----------------

.. autopydantic_model:: enhomie.ubiquiti.params.DriverUbiqClientParams
   :members:
   :show-inheritance:
   :noindex:

Ubiquiti Helpers
----------------

.. autofunction:: enhomie.ubiquiti.plugins.ubiq_latest
   :noindex:
