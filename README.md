# Who-is-Who Scraper

## Problem

Problem Description:

The task is to create a program that processes a collection of over 1000 text files containing short biographies of Swedish individuals. The biographies are digitized from a book called "Who Is Who?", with each text file representing one page containing between 4 and 8 biographies. The goal is to break up the text into individual biographies, stitch together any biographies that span multiple pages, and ultimately create one file for each biography.

Key points to consider:

1. Biographies start with the surname, followed by a comma, the first name, and then the biographical information.
2. Each biography starts on a new line.
3. An index is available, providing the starting letter of surnames on each page and some specific surnames.
4. Biographies may span multiple pages, meaning the first words on a page might be the end of a biography from the previous page.
5. The program should use regex to identify and separate the biographies, taking into account the starting letter of the surnames.

The solution should be able to process the text files, identify and separate the individual biographies, and stitch together any biographies that span multiple pages. The final output should be a set of files, each containing a single biography.