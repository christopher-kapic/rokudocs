StdDlgBulletTextItem
Extends StdDlgItemBase

The StdDlgBulletTextItem node is used to display a bulleted list of text in the dialog's content area. It should only be used as a child of a StdDlgContentArea node.

roku815px - StdDlgBulletTextItem

Fields
Field	Type	Default	Access Permission	Description
bulletText	array of strings	[ ]	READ_WRITE	An array of strings displayed as a bulleted or numbered list. The list is displayed in the content area below the message and above the bottom message.
bulletType	string	"bullet"	READ_WRITE	Specifies the type of list item delimiter, which may be one of the following:
"bullet"
"numbered"
"lettered"
Sample app
You can download and install a sample app that demonstrates how to create a custom dialog that uses the bullet text item.
