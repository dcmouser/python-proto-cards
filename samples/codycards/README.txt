//---------------------------------------------------------------------------
// This is a sample card game built with images from clipart.com
//---------------------------------------------------------------------------


//---------------------------------------------------------------------------
// You will see 3 scripts here:
//
// 1MakeParts.py
//  This script scans all of the images in the cards/srcimages directory
//   and creates (or updates) .pieces files in cards/pieces
//  The .pieces data is human+machine readable data files which describe
//   each card and image filenames.
//  The subdirectories in srcimages are used for card "categories"
//   which determine border color; filenames for this game are
//   "# title"
//
// 2MakeImages.py
//  This script parses the .pieces data files created by the first script
//   and creates images of cards in outimages/ folder
//
// 3MakePages_FullBleed.py
//  This script finds all image files in the outimages/ directory and
//  lays them out on 4x2 pages in the outimages/pages directory.
//---------------------------------------------------------------------------
