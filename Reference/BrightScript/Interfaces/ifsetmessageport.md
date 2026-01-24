ifSetMessagePort
Implemented by
Name	Description
roHdmiStatus	The HDMI status component provides an interface to the current HDMI operational status
roScreen	The roScreen component provides a full screen drawing surface that can be stacked and that you can receive input events from
roUrlTransfer	A roUrlTransfer object transfers data to or from remote servers specified by URLs. It can perform mutual authentication with a web server
roTextToSpeech	The roTextToSpeech component provides text to speech capabilities to applications

Supported methods
SetMessagePort(port as Object ) as Void
Description
Sets the roMessagePort to be used for all events from the screen.
Parameters
Name	Type	Description
Port	Object	The roMessagePort to be used for screen events.