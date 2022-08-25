# Deklaration der verwendeten Bibiotheken
from xml.dom import minidom
import xml.etree.ElementTree as ET
import shutil



class SysML_Schnittstelle:

    #XML File
    XML_File = []

    #Import
    xmldoc = []
    Baugruppe = []
    Beziehungen = []
    Anforderungen = []
    Actions = []
    AnforderungenBauteil = []
    AnforderungenBauteil = []

    #Export
    xmlMinidoc = []
    xmlETdoc = []
    xmlroot = []

    def XML_Lade(self, File):
        """
        Liest die XML Datei aus und speichert alle definierten Informationen ab
        """
        self.XML_File = File
        self.xmldoc = minidom.parse(File)
        self.BaugruppenAuslesenXMI()
        self.AnforderungAuslesenXMI()
        self.ActionAuslesenXMI()
        self.VerknuepfungenAuslesenXMI()
        self.BeziehungenAuslesenXMI()
        self.ZuweisungAnforderungBauteil()
        self.AnforderungenDirekt()
        self.Bauteil2Anforderung()

    def STEP2XML(self, File):
        """
        Liest die Informationen der zu manipulierende XML Datei aus
        """
        self.XML_File = File
        self.xmldoc = minidom.parse(File)

    #STEP 2 XML
    def ManipuliereAnforderungSysML(self,SysML_Bauteil):

        File = self.XML_File
        BauteilName = SysML_Bauteil.Bauteil

        #Definition der List
        NeueAnforderungen = SysML_Bauteil.InhaltAnforderungBauteil

        #Liest das alte XMI File
        with open(File, "r+") as fs:
            ContentXML = fs.readlines()
            fs.close()

        InhaltAnforderung = []
        IDName = []

        for elemente in NeueAnforderungen:
            GesplitteterInhalt = elemente.split("//")
            InhaltAnforderung.append(GesplitteterInhalt[0])
            IDName.append(GesplitteterInhalt[1])

        Bool_Inside = 0
        Bool_Documentation = 0
        Bool_Status = 0

        Position=0
        for line in ContentXML:
            for ID in IDName:
                if ID in line and "UML:ClassifierRole" in line:
                     # Ermittelt die aktuelle Position im *.txt File
                    Index = IDName.index(ID)
                    Bool_Inside = 1
            if Bool_Inside == 1 and "status" in line:
                Bool_Status = 1
                NeueAnfoderung = self.XMLFormatStr(line, "Implemented",3)  # Erstellt im XMI Layout die neue Anforderung
                ContentXML[Position] = NeueAnfoderung  # Speichert die neue Anfoderung i
            if Bool_Inside == 1 and "documentation" in line:
                Bool_Documentation = 1
                NeueAnfoderung = self.XMLFormatStr(line, InhaltAnforderung[Index],3)  # Erstellt im XMI Layout die neue Anforderung
                ContentXML[Position] = NeueAnfoderung   # Speichert die neue Anfoderung in den XMI File ab
            if Bool_Inside == 1 and "style" in line and Bool_Documentation == 1 and Bool_Status == 1:
                Style = "BackColor=-1;BorderColor=8036607;BorderWidth=1;FontColor=-1;VSwimLanes=1;HSwimLanes=1;BorderStyle=0;"
                NeuerStyle = self.XMLFormatStr(line, Style,3)  # Erstellt im XMI Layout die neue Anforderung
                ContentXML[Position] = NeuerStyle  # Speichert die neue Anfoderung in den XMI File ab
                Bool_Inside = 0
                Bool_Documentation = 0
                Bool_Status = 0
            Position = Position+1

        #Schreibt das neue XMI File
        with open(File, "w+") as fsN:
            fsN.writelines(ContentXML)
            fsN.close()

        return

    def XMLFormatStr(self, XMLCode, ValueWertXMLCode, ID):
        """
        Analysiert den XML-Code für die Anforderungen und speichert den neuen Inhalt in dem alten Format ab
        :param XMLCode: str :beinhaltet den gesamten String aus der xml Datei
        :param ValueWertXMLCode: str :Neue Anforderungen
        :return: str :Neuer string mit den neuen Inhalten aus den Anforderungen im xmi Format
        """
        NewLineSysML = "&#xA;"
        GesplitteterString = XMLCode.split("\"")
        GesplitteterString[ID] = ValueWertXMLCode
        XMILayoutAnforderung = "\"".join(GesplitteterString)

        return XMILayoutAnforderung

    #       SysML to STEP
    ####################################################################################################################

    # Begin XMI Auslesen
    ####################################################################################################################

    def BaugruppenAuslesenXMI(self):
        # Liest die Bauteile aus dem xml Dokument aus
        BaugruppenZwischenSpeicher = []
        BaugruppenSpeicher = []

        # Ausgabe der Komponente und Anforderung
        for element in self.xmldoc.getElementsByTagName("UML:Class"):
            Ausgabe1 = element.getAttribute('name')
            BaugruppenZwischenSpeicher.append(Ausgabe1)

            # Überüft die Eigenschaften des Bauteils
            for Classifier in element.getElementsByTagName("UML:TaggedValue"):

                # Überprüft ob das Bauteil einen Bauteil einer Baugruppe ist
                # if Classifier.getAttribute('tag') == "owner" or Classifier.getAttribute('value') == "port": alt
                if Classifier.getAttribute('tag') == "package_name":

                    # Speichert die Baugruppenzugehörigkeit in einen Zwischenspeicher
                    BaugruppenIdentifikation = Classifier.getAttribute('value')

                    # Überpüft ob das Bauteil selbst eine
                    if BaugruppenIdentifikation == Ausgabe1:
                        break

                    else:
                        # Geht alle Bauteile des XMI Files durch
                        for Baugruppe in self.xmldoc.getElementsByTagName("UML:Package"):

                            # Überprüft ob die ermittelte Baugruppenzugehörigkeit zu einer Baugruppe übereinstimmt
                            if Baugruppe.getAttribute('name') == BaugruppenIdentifikation:
                                BaugruppenZugehoerigkeit = Baugruppe.getAttribute('name')
                                BaugruppenZwischenSpeicher.append(BaugruppenZugehoerigkeit)
                                break
                        break

            BaugruppenSpeicher.append(BaugruppenZwischenSpeicher)
            BaugruppenZwischenSpeicher = []

        self.Baugruppe = BaugruppenSpeicher

        return

    def AnforderungAuslesenXMI(self):
        Anforderungstitel = []
        Anforderungsbeschreibung = []
        AnforderuungsID = []

        for ClassifierRole in self.xmldoc.getElementsByTagName("UML:ClassifierRole"):
            Bool_Requirment = 0
            for element in ClassifierRole.getElementsByTagName("UML:Stereotype"):
                if element.getAttribute("name") == "requirement": #überpüft ob es sich bei dem Element um eine Anforderung handelt
                    Bool_Requirment = 1
                    break
            if Bool_Requirment == 1:
                Anforderungstitel.append(ClassifierRole.getAttribute("name"))
                AnforderuungsID.append(ClassifierRole.getAttribute("xmi.id"))
                Bool_Documentation = 0
                for TaggedValue in ClassifierRole.getElementsByTagName("UML:TaggedValue"):
                    if TaggedValue.getAttribute("tag") == "documentation":
                        Anforderungsbeschreibung.append(TaggedValue.getAttribute("value"))
                        Bool_Documentation = 1
                        break
                if Bool_Documentation == 0:
                    Anforderungsbeschreibung.append("None")

        self.Anforderungen = [Anforderungsbeschreibung, Anforderungstitel, AnforderuungsID]

        return

    def BeziehungenAuslesenXMI(self):
        """ Ausgabe aller Dependencies des xml Dokument in der Form Dep1 zu Dep2,
        zwingend notwendig ist ein Dokument der Enterprise Architect Umgebung

        :param  xmldoc: class document xml

        :return:    list[   Beziehung_One: str                  Dependency 1
                            Beziehung_Two: str                  Dependency 2
                            ]
        """

        # Hier wird die Beziehung zwischen den Bauteil bzw. Baugruppe, Aktion oder UseCase ungefiltert aufgezeigt
        Beziehung_One = []
        Beziehung_Two = []
        Name = []

        # Auslesen der jeweiligen Aktionen mit der xmi.id
        for dependency in self.xmldoc.getElementsByTagName('UML:Dependency'):
            BauteilSet = 0
            AnforderungSet = 0
            for depvalue in dependency.getElementsByTagName('UML:TaggedValue'):
                if depvalue.getAttribute('tag') == 'ea_sourceName':
                    Beziehung_One.append(depvalue.getAttribute('value'))
                    BauteilSet = 1
                elif depvalue.getAttribute('tag') == 'ea_targetName':
                    Beziehung_Two.append(depvalue.getAttribute('value'))
                    AnforderungSet = 1
            if BauteilSet == 1 and AnforderungSet == 0:
                Beziehung_Two.append('None')
            elif AnforderungSet == 1 and BauteilSet == 0:
                Beziehung_One.append('None')

        self.Beziehungen = [Beziehung_One, Beziehung_Two]

        return

    def VerknuepfungenAuslesenXMI(self):
        """ Liest die Associationen aus dem xml-file aus, entsprechen normalen Verknüpfungen
        zwischen verschiedenen Bauteilen/Action/UseCase u.s.w

        :param  xmldoc: class document xml

        :return:    list[   Source: str                     Hirarchie darunter 1
                            Target: str                     Hirarchie darüber 2
                            ]
        """

        Source = []
        Target = []

        for element in self.xmldoc.getElementsByTagName('UML:Association'):
            Source_bool = 0
            Target_bool = 0
            for value in element.getElementsByTagName('UML:TaggedValue'):
                if value.getAttribute('tag') == 'ea_sourceName':
                    Source.append(value.getAttribute('value'))
                    Source_bool = 1
                elif value.getAttribute('tag') == 'ea_targetName':
                    Target.append(value.getAttribute('value'))
                    Target_bool = 1
            if Source_bool == 0:
                Source.append('none')
            if Target_bool == 0:
                Target.append('none')

        self.Verknuepfungen = [Source, Target]

        return

    def ActionAuslesenXMI(self):

        Action = []
        Bauteil = []
        ID_Action = []
        ID_Bauteil = []

        for element in self.xmldoc.getElementsByTagName('UML:ActionState'):
            Action.append(element.getAttribute('name'))
            ID_Action.append(element.getAttribute('xmi.id'))
            Check = 0
            for value in element.getElementsByTagName('UML:TaggedValue'):
                if value.getAttribute('tag') == 'owner':
                    for element2 in self.xmldoc.getElementsByTagName('UML:ActionState'):
                        if element2.getAttribute('xmi.id') == value.getAttribute('value'):
                            Bauteil.append(element2.getAttribute('name'))
                            ID_Bauteil.append(element2.getAttribute('xmi.id'))
                            Check = 1

            if Check == 0:
                Bauteil.append('None')

        self.Actions = [Action, Bauteil, ID_Action, ID_Bauteil]

        return

    def AnforderungenDirekt(self):

        Class = []
        Class_ID = []
        Anforderung_ID = []
        Bauteil_IDs = []
        Bauteil = []
        Anforderung = []
        Dependency_ID = []
        Anforderungs_ID_Neu = []

        for element in self.xmldoc.getElementsByTagName('UML:Class'):
            Class.append(element.getAttribute('name'))
            Class_ID.append(element.getAttribute('xmi.id'))

        for element in self.xmldoc.getElementsByTagName('UML:Dependency'):
            if element.getAttribute('client') in Class_ID:
                for TaggedValue in element.getElementsByTagName('UML:TaggedValue'):
                    if TaggedValue.getAttribute('value') == 'Requirement':
                        Anforderung_ID.append(element.getAttribute('supplier'))
                        Bauteil_IDs.append(element.getAttribute('client'))
                        Dependency_ID.append(element.getAttribute('xmi.id'))
                        break

        for element in self.xmldoc.getElementsByTagName('UML:Class'):
            if element.getAttribute('xmi.id') in Bauteil_IDs:
                index = [i for i, x in enumerate(Bauteil_IDs) if x == element.getAttribute('xmi.id')]
                for i in index:
                    Bauteil.append(element.getAttribute('name'))
                    for AnforderungElement in self.xmldoc.getElementsByTagName('UML:ClassifierRole'):
                        if AnforderungElement.getAttribute('xmi.id') == Anforderung_ID[i]:
                            for taggedValue in AnforderungElement.getElementsByTagName('UML:TaggedValue'):
                                if taggedValue.getAttribute('tag') == 'documentation':
                                    Anforderungs_ID_Neu.append(Anforderung_ID[i])
                                    Anforderung.append(taggedValue.getAttribute('value'))
                                    break
                            break

        self.Bauteil_ID_Anforderung_ID = [Bauteil_IDs, Anforderung_ID]
        self.Bauteil_Anforderung = [Bauteil, Anforderung, Anforderungs_ID_Neu]

        return

    # End XMI Auslesen
    ####################################################################################################################

    # Begin Datenverarbeitung
    ####################################################################################################################

    def ZuweisungAnforderungBauteil(self):
        """
        Vergleicht die "Anforderungen" mit den "BeziehungAnforderungen" und weist den Gegenständen (Aktionen, UseCases usw.)
        die "Anforderungen" zu. Sodass

        :param Anforderungen: list[Anforderungsbeschreibung,Anforderungsbezeichnung]
        :param BeziehungAnforderungen: list[Beziehungsgegenstand_1, Beziehungsgegenstand_2]
        :return: list[Beziehungsgegenstand, Anforderung]
        """
        Actions = self.Actions
        Dependencies = self.Beziehungen

        Bauteil = []
        Anforderung = []

        i = 0 # Zähler Actions

        for Action in Actions[0]:
            j = 0 # Zähler Dependencies
            if Action in Dependencies[0]:
                for Dependency in Dependencies[0]:
                    if Action == Dependency:
                        Bauteil.append(Actions[1][i])
                        Anforderung.append(Dependencies[1][j])
                    j = j+1
            i=i+1

        self.AnforderungenBauteil = [Anforderung, Bauteil]

        return

    def Bauteil2Anforderung(self):
        """ Ordnet direkt die Anforderungen zu den Bauteilen zu - Direktzuweisung

        :param Beziehungen: list[[str], [str], [str]]
        :param Anforderungen: list[[str], [str], [str]]
        :param Bauteile: list[str]
        :param StrangIndexAnforderungen: list[int]

        :return:
        """

        # Bauteile = self.AnforderungenBauteil[1]
        # AnforderungenBauteil = self.AnforderungenBauteil[0]
        # Anforderungsliste = self.Anforderungen
        # BauteileAnforderung = []
        #
        # i = 0
        #
        # for Anforderung in AnforderungenBauteil:
        #
        #     Anfoderungszwischenspeicher = []
        #     Bool_ElementGefunden = 0
        #
        #     if Anforderung in Anforderungsliste[1]:
        #         j = 0
        #
        #         for Element in Anforderungsliste[1]:
        #             if Anforderung == Element:
        #                 Anfoderungszwischenspeicher.append(Anforderungsliste[0][j] + "//" + Anforderungsliste[2][j])
        #                 Bool_ElementGefunden = 1
        #                 break
        #             j = j+1
        #
        #     if Bool_ElementGefunden == 1:
        #         BauteileAnforderung.append([Bauteile[i], Anfoderungszwischenspeicher])
        #
        #     i = i+1

        ZusammengefassteBauteilanforderungen = self.ZusammenfassenBauteilanforderungen(self.Bauteil_Anforderung)

        self.BauteilAnforderungstext = ZusammengefassteBauteilanforderungen

        return

    # End Datenverarbeitung
    ####################################################################################################################

    # Begin STEP Export
    ####################################################################################################################

    def WriteFileTxt(self, Inhalt, str):
        'Schreibt den Inhalt von Listen in den des "str" benannten File'

        str = 'Daten/' + str
        file = open(str, "a")

        file.truncate(0)  # Löscht den Inhalt des txt Files

        file.write("\n/*!!\n")

        i = 0
        for element in Inhalt[0]:
            file.write(
                "* " + Inhalt[2][i] + '1 : ' + Inhalt[0][i] + "\n* " + Inhalt[2][i] + '2 : ' + Inhalt[1][i] + "\n")
            i = i + 1

        file.write("*/!!\n")
        file.write("\n*/ Ende der Ausgabe")
        #
        file.close()

        return

    def WriteFileSTP(self,File,Anforderungen):
        'Schreibt den Inhalt von Listen ab dem zweiten Eintrag in den des "str" benannten File'

        file = open(File, "a")

        file.write("\n/*!!\n")

        for i in range(0, Anforderungen.__len__()):
            file.write("* " + Anforderungen[i] + "\n")

        file.write("*/!!\n")
        file.write("\n*/ Ende der Ausgabe")
        #
        file.close()

        return

    # End STEP Export
    ####################################################################################################################

    def ZusammenfassenBauteilanforderungen(self, BauteileAnforderung):
        """ Fasst die Anforderungen zu einem Bauteil zusammen

        :param BauteileAnforderung:
        :return:
        """

        Bauteile = []
        ZusammengefassteAnforderungen = []

        for element in BauteileAnforderung[0]:
            if element not in Bauteile:
                Bauteile.append(element)

        for Bauteil in Bauteile:
            Zwischenspeicher = []
            # for element in BauteileAnforderung[0]:
            #     if element == Bauteil:
            if Bauteil in BauteileAnforderung[0]:
                index = [i for i, x in enumerate(BauteileAnforderung[0]) if x == Bauteil]
                for i in index:
                    if BauteileAnforderung[1][i] not in Zwischenspeicher:
                        Zwischenspeicher.append(BauteileAnforderung[1][i] + '//' + BauteileAnforderung[2][i])
            ZusammengefassteAnforderungen.append(Zwischenspeicher)

        return [Bauteile, ZusammengefassteAnforderungen]


    def STEPErstellen(self):
        """Liest die Anforderungsliste und schreibt diese in eine BLANKO STEP-File

        """

        FirstDoc = 'Daten/Blank_STEP_Inventor.stp'

        i = 0
        for element in self.BauteilAnforderungstext[0]:
            File = 'BauteileXMI/' + element + '.stp'
            shutil.copyfile(FirstDoc, File)
            self.WriteFileSTP(File, self.BauteilAnforderungstext[1][i])
            i = i+1

        return


class SysML_Bauteil:
    Bauteil = []
    InhaltAnforderungBauteil = []

    def BereinigenStepAnforderungen(self, UnbereinigteAnforderungenStep):
        """
        Bereinigt die Zusatzinhalte "*" und "\n" aus der Liste herraus
        """
        UnbereinigteAnforderungenStep.pop(0)

        BereinigteInhalteAnforderung = []
        for element in UnbereinigteAnforderungenStep:
            str = element.replace("* ", "")
            str = str.replace("\n","")
            if str not in BereinigteInhalteAnforderung:
                BereinigteInhalteAnforderung.append(str)

        return BereinigteInhalteAnforderung

    def LesenStepAnforderungen(self, STEP_File):
        """ Liest alle Anforderungen aus der STEP Datei aus dem Anforderungsbereich
         und gibt diese als list aus.

        :param STEP_File: str von dem Dateipfad "Pfad.step"
        :return: list[Anforderung_1, Anforderung_2...]
        """
        try:

            # Öffnen des STEP Files
            STEP_Datei = open(STEP_File,'r')

            # Abspeichern des aktuellen Bauteils
            SplitBauteil = STEP_File.split("/")
            self.Bauteil = SplitBauteil[-1].replace(".stp", "")

            # Vorbereitungen zum Auslesen aus dem File
            InhaltAnforderungBauteil = [] # Platzhalter für dei Anforderungen
            CheckInside = 0  # Check ob überhaupt Anforderungen abgespeichert worden sind

            # Auslesen des Anforderungsbereiches
            for zeilen in STEP_Datei:
                if zeilen == "/*!!\n" or CheckInside == 1: # Checken ob das erste Element der Anforderungsliste erreicht worden ist
                    CheckInside = 1
                    if zeilen == "*/!!\n": # Check ob das Ende der Anforderungszeilen erreicht worden ist
                        break
                    InhaltAnforderungBauteil.append(zeilen)
            if CheckInside == 0:
                print("Kein Anforderungsbereich in der Datei vorhanden.")

            self.InhaltAnforderungBauteil = self.BereinigenStepAnforderungen(InhaltAnforderungBauteil) # Bereinigt die Anforderungen von doppelten Einträgen

        except ValueError:
            print("Datei konnte nicht gefunden werden.")

        return