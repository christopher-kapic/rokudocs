Roku Advertising Framework overview
The Roku Advertising Framework (RAF) enables the seamless integration of video advertising into your apps. The RAF library, which is built directly into the Roku SDK, includes the following features that make it easy to provide a consistent ad experience across apps:
Parsing of ads in VAST2 , VAST3 , VMAP , and FreeWheel's SmartXML formats (see the table below for details).

Built-in solution for displaying client-side (CSAI) video ads that works with Google Ad Manager (formerly known as DFP), FreeWheel, SpotX, and other 3rd-party servers.

Playback control for server-stitched ads.

Client-side handling of tracking events that is aligned with the IAB/MRC's impression measurement guidelines .

Audience measurement via Nielsen DAR / DCR , Comscore vCE , and other platforms.

Per Roku's certification requirements , all ad measurement beacons must be fired directly by RAF client-side (they may not be wrapped). This is required to apply the Roku Advertising Watermark to the beacons.
Interactive ads through Innovid, BrightLine, and Roku.

Client-side solutions to minimize buffering between ads and content.

Samples for implementing server-side ad insertion (SSAI) with Verizon Media Services, Adobe, Brightcove, Yospace, AWS Elemental MediaTailor servers, and Google Ad Manager Dynamic Ad Insertion (DAI).

Certification requirement
Per Roku's certification criteria , all apps that monetize advertising must integrate RAF to pass certification.
Getting started
To get started with your RAF integration, do the following:
If you don't have an ad server, contact adsupport@roku.com for recommendations or alternative ad serving solutions.

Read monetizing an app with video advertisements for monetization options.

Read the certification requirements for ad-supported apps .

Review the RAF integration guide .

Supported features of popular ad formats
VAST 2.0 Feature	Supported
Linear Ads	Yes
Wrapper and Inline Ads	Yes
Tracking Events	Yes
ClickThrough (interactive ads)	Yes
Companion Ads	apiFramework handled: "innovid" "brightline" "brightline_RSG"
MediaFile type	"video/mp4" "video/x-mp4" "video/mp4-h264" "application/x-mpegurl" "application/vnd.apple.mpegurl" "application/json"
Extension elements	DFP waterfall TrueX
Non-Linear Ads	No
VAST 3.0 Feature	Supported
Ad pods via sequence attribute	Yes
Extended error tracking	Yes
VAST tracking macros	Yes
Ad “buffet” selection	Yes
Skippable linear ads	No
OBA industry icon	No
VMAP Feature	Supported
Ad pods playlists	Yes
Tracking events	Yes
‘repeatAfter’ AdBreak attribute	No
Extension elements	No

RAF video lesson
You can learn how to implement RAF in order to display video ads in your app by watching the Displaying video ads video lesson in Roku's SceneGraph: Build a channel online video course .
This lesson describes how to implement RAF in order to seamlessly insert video ads into content. It highlights the different client and server-side ad insertion and stitching solutions provided by RAF, and explains how to get started with RAF in order to display video ads in your app.