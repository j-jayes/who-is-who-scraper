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

## Things to remember

Medl. av  Elektroing :fören. - He is a member of the Swedish Association of Electrical Engineers.' (Dalen, Sten Gunnar)

### List of abbreviations:

FrOPlemér                Franska orden Pour le mérite
<br/>
<br/>FrSvSO                      Franska Svarta Stjärnorden
<br/>
<br/>FS                               Fysiografiska  sällskapet  i  Lund
<br/>
<br/>FS (militärt)             flygspanarutbildning
<br/>
<br/>fs.,   förs.                     församling
<br/>
<br/>FSftjk  (förtjk)         Finska skyddskårernas förtjänstkors
<br/>
<br/>ftjk,  förtjk                 förtjänstkors
<br/>
<br/>ftjt, förtjt                  förtjänsttecken
<br/>
<br/>Fvk                             Fältveterinärkåren
<br/>
<br/>GAA                           Gustav Adolfsakademien för folklivsforskning
<br/>
<br/>GCI                             (genomgått gymnastiklärarkurs vid)  Gymnastiska
<br/>Centralinstitutet
<br/>
<br/>Gci                              genomgått instruktörskurs vid Gymnastiska Centralinstitutet
<br/>
<br/>GD                              gymnastikdirektörs(sjukgymnast-)kurs vid Gymnastiska
<br/>Centralinstitutet
<br/>
<br/>GM                             guldmedalj
<br/>
<br/>Gm                              guldmärke
<br/>
<br/>G.   m.                          gift med
<br/>
<br/>GmbH                        Gesellschaft mit beschränkter Haftung
<br/>
<br/>Gotlnb                        Gotlands  nationalbeväring
<br/>
<br/>GrFenO                      Grekiska Fenixorden
<br/>
<br/>GrFO                          Grekiska Frälsarorden
<br/>
<br/>GrGO                          Grekiska Georg I :s orden
<br/>
<br/>grkkurs                      granatkastarkurs
<br/>
<br/>GSasp (militärt)       generalstabsaspirant
<br/>
<br/>Gt                                guldtecken
<br/>
<br/>GVSbm                      minnesmedalj    med    anledning    av   Kronprins   Gustafs   och
<br/>Kronprinsessan Victorias silverbröllop
<br/>
<br/>GV:sJmt                    minnestecken med anledning av Konung Gustaf V:s 70-årsdag
<br/>
<br/>GV:s01M                   Konung Gustaf V:s olympiska minnesmedalj
<br/>
<br/>GV:sPostJubM       Konung Gustaf V:s postjubileumsmedalj
<br/>
<br/>HA                             Vitterhets-,   historie-   och   antikvitetsakademien
<br/>
<br/>HambHk                    Hamburgs  Hanseaterkors
<br/>
<br/>HavKalO                   Havaiska Kalakauaorden
<br/>
<br/>HavKamO                 Havaiska Kamehamea I :s  orden
<br/>
<br/>HavKrO                     Havaiska Kronorden
<br/>
<br/>h c                              honoris causa
<br/>
<br/>hd                                härad
<br/>
<br/>HedL                          hedersledamot av
<br/>
<br/>HessPhO                   Hessiska Philip den ädelmodiges förtjänstorden
<br/>
<br/>HHS                           Handelshögskolan i Stockholm
<br/>
<br/>Hk                              hederskors
<br/>
<br/>HKS                           Högre konstindustriella skolan i Stockholm
<br/>
<br/>HohHO                      Hohenzollernska husorden
<br/>
<br/>HSB                           Hyresgästernas  Sparkasse-  o.   Byggnadsförening
<br/>
<br/>Ht                               hederstecken
<br/>
<br/>ht                                höstterminen
<br/>
<br/>HushGM                    resp.  hushållningssällskaps  guldmedalj
<br/>
<br/>’liv, hemv                    hemvärn
<br/>
<br/>hvo (bef)                   hemvärnsområde(sbefälhavare)
<br/>
<br/>HVS                           Humanistiska vetenskapssamfundet i Uppsala
<br/>
<br/>Ica                               Inköpscentralernas A-B
<br/>
<br/>Idrm (g, s)               idrottsmärke (guld, silver)
<br/>
<br/>IF                                idrottsförening
<br/>
<br/>IFO                             Isländska Falkens orden
<br/>
<br/>io                                 inskrivningsområde
<br/>
<br/>IOGT                          International Order of Good Templars
<br/>
<br/>IOS                             Infanteriofficersskolan
<br/>
<br/>Iqml                            medaljen Illis quorum meruere labores
<br/>
<br/>IrakRO                       Irakiska Rafidain-orden
<br/>
<br/>9

### What scraping is complete so far??

gota48

skane48

sthlm45

sthlm62

svea64

gotaa65 to page 174

## What do I want to show at CBS?

1. Basic intro to the electricity paper.



What do I think is cool?
ChatGPT is both the thing that helps me code, and the thing which does the NLP - really amazing!