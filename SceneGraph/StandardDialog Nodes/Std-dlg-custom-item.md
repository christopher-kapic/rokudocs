StdDlgCustomItem
Extends StdDlgItemBase
The StdDlgCustomItem node is used to display free-form dialog items in the content area that require a custom layout.
Fields
Field	Type	Default	Access Permission	Description
widthField	float	0	READ_ONLY	The width of the custom item, which is enforced by the content area's layout algorithm.
fixedWidthField	float	0	READ_WRITE	Specifies the desired width of the custom item, which is passed to the content area's layout algorithm. This field is typically specified when the custom item includes a DynamicCustomKeyboard node , which has a width that is determined by the KDF file of the custom keyboard.

To enable a StdDlgCustomItem node to gain focus (for example, if it includes a custom keyboard node), set its focusable field to true (this field is inherited from the base Node class ).
Sample app
You can download and install a sample app that demonstrates how to create a custom dialog that uses a custom item.