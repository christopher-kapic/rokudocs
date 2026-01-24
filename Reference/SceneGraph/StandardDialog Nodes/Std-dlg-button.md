StdDlgButton
Extends Group
StdDlgButton is the class used for each button in the button area . The buttons are displayed in the order in which they are listed as children of the StdDlgButtonArea node . The size and layout of each button are controlled by the StandardDialog layout algorithm. StdDlgButton nodes should only be used as children of a StdDlgButtonArea node.
Fields
Field	Type	Default	Access Permission	Description
text	string	""	READ_WRITE	The text to be displayed on the button
disabled	boolean	false	READ_WRITE	Specifies whether the button can receive focus. If this field is set to true, the button has an inactive appearance and is unable to receive focus.