# msaSDK.feature

msaSDK.feature is feature switch management library. It allows users to create
feature switches and setup conditions those switches will be enabled
for. Once configured, switches can then be checked against inputs
(requests, user objects, etc) to see if the switches are active.

## Table of Contents

-   [Configuration](#configuration)
-   [Setup](#setup)
-   [Switches](#switches)
-   [Conditions](#conditions)
-   [Checking Switches as Active](#checking-switches-as-active)
-   [Signals](#signals)
-   [Namespaces](#namespaces)
-   [Templates]()
-   [Decorators](#decorators)
-   [Testing Utilities]()

## Configuration

msaSDK.feature requires a small bit of configuration before usage.

### Choosing Storage

Switches are persisted in a `storage` object, which is a
``msaSDK.storagedict`` or any object which provides the `types.MappingType`
interface (`__setitem__` and `__getitem__` methods). By default,
`msaSDK.feature` uses an instance of ``msaSDK.storagedict.MSAMemoryDict``. This
engine **does not persist data once the process ends** so a more
persistent data store should be used for production, something like redis.

### Autocreate

`msaSDK.feature` can also `autocreate` switches. If `autocreate` is enabled,
and `msaSDK.feature` is asked if the switch is active but the switch has not
been created yet, `msaSDK.feature` will create the switch automatically. When
autocreated, a switch's state is set to `disabled.`

This behavior is off by default, but can be enabled through a setting.
More on `settings` below.

### Configuring Settings

To change the `storage` and/or `autocreate` settings, simply import the
settings module and set the appropriate variables:

``` {.python}
from msaSDK.feature.base.settings import get_msa_feature_settings
from msaSDK.feature.base.maneger import MSAManager
from msaSDK.storagedict import MSARedisDict
from redis import RedisClient

settings = get_msa_feature_settings()
settings.storage_engine = MSARedisDict('msaSDK.feature', RedisClient()))
settings.autocreate = True

myManager = MSAManager(settings=settings)

```

In this case, we are changing the engine to msaSDK.storagedict `MSARedisDict`
and turning on `autocreate` and creating a MSAManager instance from those settings.

`myManager` object, is now your main interface.

## Setup

At this point the `MSAManager` object is an instance of the `MSAManager` class,
which holds all methods to register switches and check if they are
active. 


## Mappings

The first step in your usage of `msaSDK.feature` should be to define your
mappings (Pydantic/SQLModel classes) that you will be checking switches against. An `mapping` is
an object which understands the business logic and object in your system
(users, requests, etc) and knows how to validate, transform and extract
variables from those business objects for `MSASwitch` conditions. For
instance, your system may have a `User` object that has properties like
`is_admin`, `date_joined`, etc. To switch against it, you would then
create mappings for each of those values.

Since constructing mappings that simply reference an attribute on
`self.input` is so common, if you pass a string as the first argument of
`mapping()`, when the argument is accessed, it will simply return that
property from `self.input`. You must also pass a `Variable` to the
`variable=` kwarg so msaSDK.feature know what Variable to wrap your value in.

```python
from typing import Optional
from sqlmodel import SQLModel
from msaSDK.admin.utils.fields import Field
from msaSDK.feature.base.condition import MSACondition
from msaSDK.feature.base.manager import MSAManager
from msaSDK.feature.base.settings import get_msa_feature_settings
from msaSDK.feature.base.switch import MSASwitch
from msaSDK.feature.operators.compare import MoreThan


class TestCategory(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    title: str = Field(title="ArticleTitle", max_length=200)
    description: Optional[str] = Field(
        default="", title="ArticleDescription", max_length=400
    )
    status: bool = Field(None, title="status")
    content: str = Field(title="ArticleContent")
    age: int = Field(default=35, title="Age")


settings_features = get_msa_feature_settings()
settings_features.autocreate = True
myManager = MSAManager(settings=settings_features)
switch = MSASwitch('my feature', state=MSASwitch.states.CONDITIONAL)
condition = MSACondition(mapping=TestCategory, attribute='age', operator=MoreThan(15))
switch.conditions.append(condition)
myManager.register(switch)

print("active: ", myManager.active('my feature'))
```

## Switches

Switches encapsulate the concept of an item that is either \'on\' or
\'off\' depending on the input. The swich determines its on/off status
by checking each of its `conditions` and seeing if it applies to a
certain input.

Switches are constructed with only one required argument, a `name`:

``` {.python}
from msaSDK.feature.base.switch import MSASwitch

switch = MSASwitch('my feature')
```

Switches can be in 3 core states: `PERMANENT`, `DISABLED` and `CONDITIONAL`.
In the `PERMANENT` state, the Switch is enabled for every input no matter
what. `DISABLED` Switches are **disabled** for any input, no matter
what. `CONDITIONAL` Switches enabled based on their conditions.

Switches can be constructed in a certain state or the property can be
changed later:

``` {.python}
switch = MSASwitch('new feature', state=MSASwitch.states.DISABLED)
another_switch = MSASwitch('new feature')
another_switch.state = MSASwitch.states.DISABLED
```

### Interlinked

When in the `CONDITIONAL` state, normally only one condition needs be true
for the Switch to be enabled for a particular input. If
`switch.interlinked` is set to `True`, then **all** of the switches
conditions need to be true in order to be enabled:

    switch = Switch('require alll conditions', interlinked=True)

### Heriarchical Switches

You can create switches using a specific hierarchical naming scheme.
Switch namespaces are divided by the colon character (`:`), and
hierarchies of switches can be constructed in this fashion:

``` {.python}
parent = MSASwitch('movies')
child1 = MSASwitch('movies:star_wars')
child2 = MSASwitch('movies:die_hard')
grandchild = MSASwitch('movies:star_wars:a_new_hope')
```

In the above example, the `child1` switch is a child of the `"movies"`
switch because it has `movies:` as a prefix to the switch name. Both
`child1` and `child2` are `children of the parent `parent` switch. And
`grandchild` is a child of the `child1` switch, but *not* the `child2`
switch.

### Concent

By default, each switch makes its `am I active?` decision independent
of other switches in the MSAManager (including its parent), and only
consults its own conditions to check if it is enabled for the input.
However, this is not always what you want. Perhaps you have a new
feature that is only available to a certain class of user. And of
*those* users, you want 10% to be be exposed to a different user
interface to see how they behave vs the other 90%.

`msaSDK.feature` allows you to set a `concent` flag on a switch that instructs
it to check its parental switch first, before checking itself. If it
checks its parent and it is not enabled for the same input, the switch
immediately returns `False`. If its parent *is* enabled for the input,
then the switch will continue and check its own conditions, returning as
it would normally.

For example:

``` {.python}
parent = MSASwitch('new_feature')
child = MSASwitch('new_feature:new_ui', concent=True)
```

For example, because `child` was constructed with `concent=True`, even
if `child` is enabled for an input, it will only return `True` if
`parent` is **also** enabled for that same input.

??? note
    Even switches in a `PERMANENT` or `DISABLED` state (see
    `MSASwitch` section above) still consent their parent before checking
    themselves. That means that even if a particular switch is `PERMANENT`, if
    it has `concent` set to `True` and its parent is **not** enabled for the
    input, the switch itself will return `False`.

### Registering a Switch

Once your `MSASwitch` is constructed with the right conditions, you need to
register it with a `MSAManager` instance to preserve it for future use.
Otherwise it will only exist in memory for the current process. Register
a switch via the `register` method on a `MSAManager` instance:

``` {.python}
myManager.register(switch)
```

The Switch is now stored in the MSAManager's storage and can be checked if
active through `myManager.active(switch)`.

### Updating a Switch

If you need to update your Switch, simply make the changes to the
`MSASwitch` object, then call the `MSAManager`'s `update()` method with the
switch to tell it to update the switch with the new object:

``` {.python}
switch = MSASwitch('my switch')
myManager.register(switch)

switch.name = 'even better switch'  # Switch has not been updated in manager yet

myManager.update(switch)  # Switch is now updated in the manager
```

Since this is a common pattern (retrieve switch from the manager, then
update it), msaSDK.feature provides a shorthand API in which you ask the manager
for a switch by name, and then call `save()` on the **switch** to update
it in the `MSAManager` it was retreived from:

``` {.python}
switch = myManager.switch('existing switch')
switch.name = 'a new name'  # Switch is not updated in manager yet
switch.save()  # Same as calling myManager.update(switch)
```

### Unregistering a Switch

Existing switches may be removed from the MSAManager by calling
`unregister()` with the switch name or switch instance:

``` {.python}
myManager.unregister('deprecated switch')
myManager.unregister(a_switch_instance)
```

**Note:** If the switch is part of a hierarchy and has children switches
(see the `Hierarchical Switches` section above), all descendent
switches (children, grandchildren, etc) will also be unregistered and
deleted.

## Conditions

Each Switch can have 0+ conditions, which describe the conditions under
which that switch is active. `MSACondition` objects are constructed with
three values: a `mapping`, `attribute` and `operator`.

An `mapping` is any `Pydantic` or `SQLModel` class, like the one you defined earlier.
From the previous example, `UserPydanticClass` is an Pydantic object.
`attribute` is the attribute on a mapping instance that you want this
condition to check. `operator` is some sort of check applied against
that attribute. For instance, is the `UserPydanticClass.age` greater than
some value? Equal to some value? Within a range of values? Etc.

Let's say you wanted a `MSACondition` that checks if the user's age is \>
65 years old? You would construct a MSACondition that way:

``` {.python}
from msaSDK.feature.base.operators.comparable import MoreThan

condition = MSACondition(mapping=UserPydanticClass, attribute='age', operator=MoreThan(65))
```

This MSACondition will be true if any input instance has an `age` that is
more than `65`.

Please see the `msaSDK.feature.operators` for a list of available operators.

Conditions can also be constructed with a `negative` argument, which
negates the condition. For example:

``` {.python}
from msaSDK.feature.base.operators.comparable import MoreThan

condition = MSACondition(mapping=UserPydanticClass, attribute='age', operator=MoreThan(65), negative=True)
```

This Condition is now `True` if the condition evaluates to `False`. In
this case if the user's `age` is **not** more than `65`.

Conditions then need to be appended to a switch instance like so:

``` {.python}
switch.conditions.append(condition)
```

You can append as many conditions as you would like to a switch, there
is no limit.

## Checking Switches as Active

As stated before, switches are checked against input objects. To do
this, you would call the switch's `enabled_for()` method with a `User`
instance, for instance. You may call `enabled_for()` with any input
object, it will ignore inputs for which it knows nothing about. If the
`MSASwitch` is active for your input, `enabled_for` will return `True`.
Otherwise, it will return `False`.

### `MSAmanager.active()` API

A common use case of msaSDK.feature is to use it during the processing of a web
request. During execution of code, different code paths are taken
depending on if certain switches are active or not. Often times there
are multiple switches in existence at any one time and they all need to
be checked against multiple mappings. To handle this use case, msaSDK.feature
provides a higher-level API.

To check if a `MSASwitch` is active, simply call `msaSDK.feature.active()` with the
Switch name:

``` {.python}
myManager.active('my feature')
>>> True
```

The switch is checked against some number of input objects. Inputs can
be added to the `active()` check one of two ways: locally, passed in to
the `active()` call or globally, configured ahead of time.

To check against local inputs, `active()` takes any number of input
objects after the switch name to check the switch against. In this
example, the switch named `'my feature'` is checked against input
objects `input1` and `input2`:

``` {.python}
myManager.active('my feature', input1, input2)
>>> True
```

If you have global input objects you would like to use for every check,
you can set them up by calling the MSAManager's `input()` method:

``` {.python}
myManager.input(input1, input2)
```

Now, `input1` and `input2` are checked against for every `active` call.
For example, assuming `input1` and `input2` are configured as above,
this `active()` call would check if the Switch was enabled for inputs
`input1`, `input2` and `input3` in that order:

    myManager.active('my feature', input3)

Once you\'re doing using global inputs, perhaps at the end of a request,
you should call the MSAManager's `flush()` method to remove all the
inputs:

``` {.python}
myManager.flush()
```

The MSAManager is now setup and ready for its next set of inputs.

When calling `active()` with a local inputs, you can skip checking the
`MSASwitch` against the global inputs and **only** check against your
locally passed in inputs by passing `exclusive=True` as a keyword
argument to `active()`:

``` {.python}
myManager.input(input1, input2)
myManager.active('my feature', input3, exclusive=True)
```

In the above example, since `exclusive=True` is passed, the switch named
`'my feature'` is **only** checked against `input3`, and not
`input1` or `input2`. The `exclusive=True` argument is not persistent,
so the next call to `active()` without `exclusive=True` will again use
the globally defined inputs.

## Signals

msaSDK.feature provides 4 total signals to connect to: 3 about changes to
Switches, and 1 about errors applying Conditions. They are all available
from the `msaSDK.feature.base.signal` module

### Switch Signals

There are 3 signals related to Switch changes:

1.  `switch_registered` - Called when a new switch is registered with
    the MSAManager.
2.  `switch_unregistered` - Called when a switch is unregistered with
    the MSAManager.
3.  `switch_updated` - Called with a switch was updated.


There are 2 signals related to Switch events:

1.  `switch_checked` - Called when a switch is checked enabled_for with
    the MSAManager.
2.  `switch_active` - Called when a switch is checked enabled_for and is enabled with
    the MSAManager.


To use a signal, simply call the signal's `connect()` method and pass
in a callable object. When the signal is fired, it will call your
callable with the switch that is being register/unregistered/updated.
I.e.:

``` {.python}
from msaSDK.feature.base.signal import switch_updated

def log_switch_update(switch):
    Syslog.log("Switch %s updated" % switch.name)

switch_updated.connect(log_switch_updated)
```

### Understanding Switch Changes

The `switch_updated` signal can be connected to in order to be notified
when a switch has been changed. To know *what* changed in the switch,
you can consult its `changes` property:

``` {.python}
>>> from msaSDK.feature.base.switch import MSASwitch
>>> switch = MSASwitch('test')
>>> switch.concent
True
>>> switch.concent = False
>>> switch.name = 'new name'
>>> switch.changes
{'concent': {'current': False, 'previous': True}, 'name': {'current': 'new name', 'previous': 'test'}}
```

As you can see, when we changed the Switch's `concent` setting and
`name`, `switch.changes` reflects that in a dictionary of changed
properties. You can also simply ask the switch if anything has changed
with the `changed` property. It returns `True` or `False` if the switch
has any changes as all.

You can use these values inside your signal callback to make decisions
based on what changed. I.e., email out a diff only if the changes
include changed conditions.

### Condition Application Error Signal

When a `MSASwitch` checks an input object against its conditions, there is
a good possibility that the `Mapping` value may be some sort of
unexpected value, and can cause an exception. Whenever there is an
exception raised during `Condition` checking itself against an input,
the `Condition` will catch that exception and return `False`.

While catching all exceptions is generally bad form and hides error,
most of the time you do not want to fail an application request just
because there was an error checking a switch condition, *especially* if
there was an error during checking a `Condition` for which a user would
not have applied in the first place.

That said, you would still probably want to know if there was an error
checking a Condition. To accomplish this, `msaSDK.feature`-client provides a
`condition_apply_error` signal which is called when there was an error
checking a `Condition`. The signal is called with an instance of the
condition, the input which caused the error and the instance of the
Exception class itself:

``` {.python}
msaSDK.features.base.signal.condition_apply_error.call(condition, inpt, error)
```

In your connected callback, you can do whatever you would like: log the
error, report the exception, etc.

## Namespaces

`msaSDK.feature` allows the use of `namespaces` to group switches under a
single umbrella, while both not letting one namespace see the switches
of another namespace, but allowing them to share the same storage
instance, operators and other configuration.

Given an existing vanilla `MSAManager` instance, you can create a
namespaced manager by calling the `namespaced()` method:

``` {.python}
notifications = myManager.namespaced('notifications')
```

At this point, `notifications` is a copy of `myManager`, inheriting all of
its:

-   storage
-   `autocreate` setting
-   Global inputs
-   Operators

It does **not**, however, share the same switches. Newly constructed
`MSAManager` instances are in the `default` namespace. When `namespaced()`
is called, `myManager` changes the manager's namespace to `notifications`.
Any switches in the previous `default` namespace are not visible in the
`notifications` namespace, and vice versa.

This allows you to have separate namespaced `views` of switches,
possibly named the exact same name, and not have them conflict with each
other.

## Decorators

msaSDK.feature features a `@switch_active` decorator you can use to decorate
your Django views. When decorated, if the switch named as the first
argument of the `@switch_decorated` decorator is False, a `Http404`
exception is raised. However, if you also pass a `redirect_to=` kwarg,
the decorator will return a `HttpResponseRedirect` instance, redirecting
to that location. If the switch is active, then the view runs as normal.

For example, here is a view decorated with `@switch_active`:

``` {.python}
from msaSDK.feature.base.decorators import switch_active

@switch_active('my_feature')
def my_view(request):
    return 'foo'
```

As stated above, if the `my_feature` switch is inactive, this view
will raise a `starlette.exceptions.HttpException` exception with ``status_code=404, detail='MSASwitch %s not active' % name``.

If, however, the decorator was constructed with a `redirect_to=` kwarg:

``` {.python}
@switch_active('my_feature', redirect_to=reverse('upsell-page'))
```

Then a `starlette.responses.RedirectResponse` instance will be returned, redirecting to
`reverse('upsell-page')`.

