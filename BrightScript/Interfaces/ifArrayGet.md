ifArrayGet
The ifArrayGet interface supports the array indexing operator [ ]

(See Array Operator)

Implemented by
Name	Description
roArray	An array stores an indexed collection of BrightScript objects. Each entry of an array can be a different type, or they may all of the same type
roByteArray	The byte array component is used to contain and manipulate an arbitrary array of bytes
roList	The list object implements the interfaces: ifList, ifArray, ifEnum and therefore can behave like an array that can dynamically add members
roXMLList	Contains a list of roXML objects
Supported methods
GetEntry(index As Integer) As Dynamic
Description
Returns an array entry based on the provided index.

Parameters
Name	Type	Description
index	Integer	The index of the array entry to be returned.
Return Value
The array entry corresponding to the provided index, or invalid if the entry has not been set.
