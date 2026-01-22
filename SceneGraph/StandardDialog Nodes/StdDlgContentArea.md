StdDlgContentArea
Extends StdDlgAreaBase

The StdDlgContentArea node contains the main body of the dialog. It is positioned between the title area and the button area.

It contains zero or more child nodes that extend StdDlgItemBase (for example, StdDlgTextItem, StdDlgProgressItem, StdDlgGraphicItem, and other dialog building blocks). The layout and position of the StdDlgItemBase nodes are based on the dialog's width; the nodes are arranged vertically from top to bottom in the content area based on the order in which they are listed. The content area should contain only StdDlgItemBase nodes; otherwise, its layout and rendering are undefined.

roku815px - content-area

Fields
The StdDlgContentArea node does not have any fields.
