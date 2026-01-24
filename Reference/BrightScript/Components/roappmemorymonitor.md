roAppMemoryMonitor
The roAppMemoryMonitor component is used to subscribe apps to low-memory notifications. When an app is subscribed, it receives a roAppMemoryNotificationEvent when it reaches a specific percentage of the per-app memory limit (80%).
The roAppMemoryMonitor functions are supported on all current and updatable device models , except for Liberty, Austin, Mustang and Littlefield.
Supported interfaces
ifAppMemoryMonitor

Supported events
roAppMemoryNotificationEvent
ifSetMessagePort
ifGetMessagePort