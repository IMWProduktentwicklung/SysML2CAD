# Deklaration der verwendeten Bibiotheken
import XML_Funktionen as XML

if __name__ == '__main__':

    File = 'Daten/drehschiebeverdichter_v18.xml'

    # XML -> CAD

    Projekt_Drehschieber = XML.SysML_Schnittstelle()
    Projekt_Drehschieber.XML_Lade(File)     # Initialbefehl
    # Projekt_Drehschieber.STEPErstellen()

    # CAD -> XML
    Hohlzylinder = XML.SysML_Bauteil() # Überlegen

    STEP_File = "BauteileXMI/Hohlzylinder.stp"
    Hohlzylinder.LesenStepAnforderungen(STEP_File)
    Projekt_Drehschieber.ManipuliereAnforderungSysML(Hohlzylinder)

    print("Auslesung beendet")


# TODO Anforderungen in den STEPs benötiigen XMI.ID der Anforderung

# Alte TODOs
# TODO Fahrwerk ist kein Bauteil!! Hier muss eine Überprüfung stattfinden
# TODO Direktanforderungen & Anfoderungsverknüpfung reichen vorerst aus / Hinweg zu Bauteilen / Rückweg zu SysMl
# Integration in die CAD Umgebung | SysML Dokumentation der Elemente
# TODO ID Values von den Anforderungen auslesen
# TODO Rückweg aufbauen zu SysML - Bidirektional
