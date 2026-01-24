ifFontRegistry
Implemented by
Name	Description
roFontRegistry	The roFontRegistry object allows you to create roFont objects, either using the default font or using fonts in TrueType or OpenType files packaged with your application

Supported methods
Register(path as String) as Boolean
Description
Registers a font file (.ttf or .otf format). Each font file defines one or more font families (usually one).
Parameters
Return Value
A flag indicating whether the fonts in the specified file were successfully installed.
GetFamilies() as Object
Description
Returns the names of the font families that have been registered via the Register() method. Each name can be passed as the first parameter to the GetFont() method.
Return Value
An roArray of strings that represent the names of the font families that have been registered.
GetFont(family as String, size as Integer, bold as Boolean, italic as Boolean) as Object
Description
Returns a font from the specified family, selected from the fonts previously registered via the Register() method.
Parameters
Name	Type	Description
family	String	The font family name.
size	Integer	The requested font size, in pixels, not points.
bold	Boolean	"bold" specifies a font variant that may be (but is not always) supported by the font file.
italic	Boolean	"italic" specifies a font variant that may be (but is not always) supported by the font file.

Return Value
An roFont object representing a font from the specified family.
GetDefaultFont() as Object
Description
Returns the system font at its default size. Calling this method is the same as calling the GetDefaultFont() method with the following syntax: reg.GetDefaultFont(reg.GetDefaultFontSize(), false, false) .
Return Value
The system font as its default size.
GetDefaultFont(size as Integer, bold as Boolean, italic as Boolean) as Object
Description
Returns the system font. The system font is always available, even if the Register() method has not been called
Parameters
Name	Type	Description
size	Integer	The requested font size, in pixels, not points.
bold	Boolean	"bold" specifies a font variant that may be (but is not always) supported by the font file.
italic	Boolean	"italic" specifies a font variant that may be (but is not always) supported by the font file.

Return Value
An roFont object representing the system font.
GetDefaultFontSize() as Integer
Description
Returns the default font size.
Return Value
The default font size.
Get(family as String, size as Integer, bold as Boolean, italic as Boolean) as String
Description
Returns a valid font string.
Parameters
Name	Type	Description
family	String	The font family name.
size	Integer	The requested font size, in pixels, not points.
bold	Boolean	"bold" specifies a font variant that may be (but is not always) supported by the font file.
italic	Boolean	"italic" specifies a font variant that may be (but is not always) supported by the font file.

Return Value
A valid font string.