CREATE TABLE "movimientos" (
	"ID"	INTEGER UNIQUE,
	"Fecha"	TEXT,
	"Hora"	TEXT,
	"Moneda_from"	TEXT,
	"Cantidad_from"	NUMERIC,
	"Moneda_to"	TEXT,
	"Cantidad_to"	NUMERIC,
	PRIMARY KEY("ID" AUTOINCREMENT)
)