# wiki_matcher

Scaricare cartella dei file e il risultato si trova nel file dict_company_keylist.json
Le parole hanno subìto processo di stemming, quindi le vedete troncate, ma c'è modo di risalire alla parola originale.

Problemi riscontrati:
- se cerco azienda "Apple" scritta così non trovo Apple azienda ma Apple frutta (senza che venga sollevata una eccezione di disambiguazione, quindi non ho modo di accorgermene). POSSIBILE SOLUZIONE: estraggo sia da wiki eng che da wiki ita, e confronto le due pagine. Se sono uguali, ho più probabilità di aver preso la pagina di interesse. Se sono diverse e non ho modo automatico di dire quale è la pagina giusta, scarto (meglio scartare piuttosto che compilare un record sbagliato).


- Se il nome della lista ha una formattazione leggermente diversa da quella che permette alla API di Wikipedia di identificare la parola precisa, rischio di non trovare la pagina ed avere un record vuoto.

- Ci basta usare riassunto (che credo sia la parte introduttiva della pagina (secondo me no, perché le info delle news spesso riguardano caratteristiche di una azienda che non sempre sono riportate nell'introduzione. Ad esempio: news che parla del tasto like di facebook, non trova match perché nell'introduzione di facebook pagina non si trova questa parola)). Conviene prendere pagina intera che ha più info, ma rischio di prendere parole troppo frequenti (tipo sezioni "external links" ecc) che mi sballano l'estrazione di keywords, quindi conviene scaricare intera pagina TODO TROVA SOLUZIONE.

- forse conviene fare multi tokenization solo per i nomi di persone e organizzazione




