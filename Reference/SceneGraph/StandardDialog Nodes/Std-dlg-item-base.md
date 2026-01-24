StdDlgItemBase
Extends Group
StdDlgItemBase is the base class for all the content area items. It provides the common functionality for all StdDlg[ x ]Item nodes (for example, StdDlgBulletTextItem , StdDlgTextItem , StdDlgKeyboardItem , StdDlgProgressItem , StdDlgGraphicItem , and the other dialog building block nodes).
Fields
Field	Type	Default	Access Permission	Description
scrollable	boolean	false	READ_WRITE	Indicates whether the item can be scrolled vertically by the user. The StandardDialog layout algorithm reduces the height of a scrollable item as needed if the overall height of the dialog is too large to fit on the display.