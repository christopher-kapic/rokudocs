StdDlgProgressItem
Extends StdDlgItemBase
The StdDlgProgressItem node is used to display a spinning progress indicator in the dialog's content area. It provides the status of a task that takes an indeterminate amount of time. It should only be used as a child of a StdDlgContentArea node.
Fields
Field	Type	Default	Access Permission	Description
text	string	""	READ_WRITE	Specifies the text to be displayed next to the progress graphic. If the text width does not fit within the width of the content area, the text will wrap onto multiple lines.

Sample app
You can download and install a sample app that demonstrates how to create a custom dialog that uses the progress item.