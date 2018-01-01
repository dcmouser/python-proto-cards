//---------------------------------------------------------------------------
// PythonProtoCards
// v1.6.1 - 7/15/14
// by mouser@donationcoder.com
// http://www.donationcoder.com/Software/Mouser/pythonprotocards/index.html
//
// This is a very early release of python code to assist in card game design
//  and prototyping.
//
// It includes classes to help quickly create card/piece data, make card
//  images, and lay out these images for printing.
//---------------------------------------------------------------------------

//---------------------------------------------------------------------------
// version history:

//  v1.6.1 - 7/15/14 -- added instructions on using PILLOW instead of PIL
//  v1.5.1 - 9/9/12 -- improved layout of large blocks of text; fixed bug when displaying text with linebreaks
//  v1.4.1 - 4/5/11 -- added corner circle text helper function, and used it from sample CodyCards
//  v1.2.1 - 3/25/11 -- improved transparency effects, improved full page bleed layouts
//  v1.0.1 - 3/13/11 -- first release
//---------------------------------------------------------------------------

//---------------------------------------------------------------------------
// Non-core-python requirements:
//  PIL image library
//---------------------------------------------------------------------------



//---------------------------------------------------------------------------
// The PythonProtoCards functions divide up work into different steps,
//  so that you can manually create and edit game piece data or automatically
//  generate it programmatically.
// The common element is the .piece data file format, which is designed to
//  be very easy for humans to edit, but also parseable by code
// The helper classes for working with .piece file data are able to load the
//  data, modify it, and write out newly modified file, almost like a
//  minimalistic database, which makes it easy to programmatically modify or
//  add to existing data files that will also be hand edited.
//---------------------------------------------------------------------------


//---------------------------------------------------------------------------
// See the samples/codycards directory for a sample card game and scripts
//  to create cards programatically.
//---------------------------------------------------------------------------



//---------------------------------------------------------------------------
Related projects by other coders:

Inkscape Boardgames Extensions by Pelle Nilsson
http://www.lysator.liu.se/~perni/iboardgameexts/

Nandeck
http://www.nand.it/nandeck/
//---------------------------------------------------------------------------











//---------------------------------------------------------------------------
7/15/14
Windows 7 -- Instead of PIL im installing "pip install pillow" which seems to be cleaner install;
minor changes to imports in some files.
//---------------------------------------------------------------------------
