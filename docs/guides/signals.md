# msaSDK.signals

Signals/Events for MSAApp/FastAPI. Run background task without blocking the function that creates the signal. 
msaSDK.signals tries to stay as a background task runner.

# Usage - MSASignalMiddleware
!!! note
    Only one signal per function, must take request object as arg

### Add middleware
```python
from msaSDK.signals import MSASignalMiddleware, signal
app = MSAApp()
app.add_midleware(MSASignalMiddleware, handler=signal)

# OR enable MSASetting for this feature (settings.signal_middleware)
```
### Add handler
Specify how the fired signal should work.
```python
from msaSDK.signals import signal
import asyncio

@signal.register
async def handler(**kwargs):
    await asyncio.sleep(5)
    print(kwargs)
    print('Works!')
```
### Fire signal in function
!!! note
    Only one signal call is allowed using background task.

```python
from msaSDK.signals import initiate_signal
@app.get("/")
async def endpoint(request: Request):
    await initiate_signal(request, 'handler',some_data="test value")
    return {"status":"Success"}
```
# Usage - MSATaskMiddleware
Any number of tasks, no request object needed.
### Add middleware
```python
from msaSDK.signals import MSATaskMiddleware
app = MSAApp()
app.add_midleware(MSATaskMiddleware)

# OR enable MSASetting for this feature (settings.task_middleware)
```
### Write handler
Specify how the fired task should work.
```python
async def handler():
    await asyncio.sleep(5)
    print('Works!')
```
### Fire task in function
```python
from msaSDK.signals import initiate_task
@app.get("/")
async def endpoint():
    await initiate_task(handler,some_data="test value")
    return {"status":"Success"}
```