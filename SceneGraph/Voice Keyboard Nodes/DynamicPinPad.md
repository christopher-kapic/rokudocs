DynamicPinPad
Extends DynamicKeyboardBase

The DynamicPinPad node is similar to the legacy PinPad node, but with additional voice entry functionality. It enables text and voice entry of numeric characters. It is typically used for entering short numeric PIN codes.

The key layout is fixed based on the node's pre-built Key Definition File.

roku815px - dynamic-pinpad-voice

Fields
The DynamicPinPad node inherits all its fields from its parent DynamicKeyboardBase node class. See the DynamicKeyboardBase and its base classes (Group and Node) for descriptions of the fields that can be configured.

Default VoiceTextEditBox settings
Field	Type	Default	Description
voiceEntryType	string	"numeric"	The type of characters accepted via voice entry.
voiceEnabled	boolean	true	Specifies whether voice entry is enabled for the text edit box of the dynamic PIN pad.
maxTextLength	integer	4	The maximum number of characters that may be entered into the text edit box of the dynamic pinpad.
Sample app
You can download and install a sample app that demonstrates how to create and configure a dynamic voice-enabled PIN pad.
