# wiki_matcher

Problemi riscontrati:
- se cerco azienda "Apple" scritta così non trovo Apple azienda ma Apple frutta (senza che venga sollevata una eccezione di disambiguazione, quindi non ho modo di accorgermene).
- Se il nome della lista ha una formattazione leggermente diversa da quella che permette alla API di Wikipedia di identificare la parola precisa, rischio di non trovare la pagina ed avere un record vuoto.


